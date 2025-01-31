#!/usr/bin/env python3
import os
import sys
import logging
import argparse
import re
from typing import List, Dict, Optional, Tuple
from github import Github
from github.PullRequest import PullRequest
from github.Repository import Repository
from github.IssueComment import IssueComment
from dotenv import load_dotenv
import git
from openai import OpenAI

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class PRDiffAnalyzer:
    def __init__(self, github_token: str, openrouter_key: str, model: str = "anthropic/claude-3.5-sonnet"):
        """
        Initialize the PR Diff Analyzer with GitHub and OpenRouter authentication.

        Args:
            github_token (str): GitHub personal access token
            openrouter_key (str): OpenRouter API key
            model (str): OpenRouter model to use (default: anthropic/claude-3.5-sonnet)
        """
        self.model = model
        self.github = Github(github_token)

        # Initialize OpenAI client with OpenRouter configuration
        headers = {
            "HTTP-Referer": "https://github.com/pr-diff-bot",
            "X-Title": "PR Diff Analyzer"
        }
        self.openai_client = OpenAI(api_key=openrouter_key, base_url="https://openrouter.ai/api/v1", default_headers=headers)
        self.bot_signature = "<!-- PR-DIFF-BOT-COMMENT -->"

    def get_pull_request(self, repo_name: str, pr_number: int) -> PullRequest:
        """
        Get a pull request object from GitHub.

        Args:
            repo_name (str): Repository name in format 'owner/repo'
            pr_number (int): Pull request number

        Returns:
            PullRequest: GitHub pull request object
        """
        try:
            repo = self.github.get_repo(repo_name)
            return repo.get_pull(pr_number)
        except Exception as e:
            logger.error(f"Error fetching pull request: {str(e)}")
            raise

    def get_last_analyzed_commit(self, pr: PullRequest) -> Optional[str]:
        """
        Get the SHA of the last commit that was analyzed by the bot.

        Args:
            pr (PullRequest): GitHub pull request object

        Returns:
            Optional[str]: The SHA of the last analyzed commit, or None if not found
        """
        try:
            comments = pr.get_issue_comments()
            for comment in comments.reversed:
                if self.bot_signature in comment.body:
                    # Extract commit SHA from the comment
                    match = re.search(r'Analyzed commit: ([a-f0-9]{40})', comment.body)
                    if match:
                        return match.group(1)
            return None
        except Exception as e:
            logger.error(f"Error getting last analyzed commit: {str(e)}")
            return None

    def should_analyze_pr(self, pr: PullRequest) -> Tuple[bool, str]:
        """
        Determine if the PR should be analyzed based on the last analyzed commit.

        Args:
            pr (PullRequest): GitHub pull request object

        Returns:
            Tuple[bool, str]: (should_analyze, current_commit_sha)
        """
        try:
            current_commit_sha = pr.head.sha
            last_analyzed_sha = self.get_last_analyzed_commit(pr)

            if not last_analyzed_sha:
                logger.info("No previous analysis found. Will analyze PR.")
                return True, current_commit_sha

            if current_commit_sha != last_analyzed_sha:
                logger.info(f"New commits found. Last analyzed: {last_analyzed_sha[:8]}, Current: {current_commit_sha[:8]}")
                return True, current_commit_sha

            logger.info("PR already analyzed for current commit. Skipping analysis.")
            return False, current_commit_sha

        except Exception as e:
            logger.error(f"Error checking PR analysis status: {str(e)}")
            raise

    def analyze_diff(self, pr: PullRequest) -> Dict:
        """
        Analyze the changes in a pull request.

        Args:
            pr (PullRequest): GitHub pull request object

        Returns:
            Dict: Analysis results containing file changes and statistics
        """
        analysis = {
            'files_changed': 0,
            'additions': 0,
            'deletions': 0,
            'file_details': [],
            'summary': [],
            'file_contents': {}
        }

        try:
            files = pr.get_files()

            for file in files:
                analysis['files_changed'] += 1
                analysis['additions'] += file.additions
                analysis['deletions'] += file.deletions

                file_info = {
                    'filename': file.filename,
                    'status': file.status,
                    'additions': file.additions,
                    'deletions': file.deletions,
                    'changes': file.changes,
                    'patch': file.patch if file.patch else ''
                }
                analysis['file_details'].append(file_info)

                if file.status != 'removed':
                    try:
                        content = pr.get_repo().get_contents(file.filename, ref=pr.head.sha)
                        analysis['file_contents'][file.filename] = content.decoded_content.decode('utf-8')
                    except Exception as e:
                        logger.warning(f"Could not fetch content for {file.filename}: {str(e)}")

                if file.changes > 50:
                    analysis['summary'].append(
                        f"Major changes in {file.filename}: +{file.additions}/-{file.deletions} lines"
                    )
                elif file.status == 'removed':
                    analysis['summary'].append(f"Deleted file: {file.filename}")
                elif file.status == 'added':
                    analysis['summary'].append(f"New file: {file.filename}")

            return analysis

        except Exception as e:
            logger.error(f"Error analyzing diff: {str(e)}")
            raise

    def get_ai_response(self, messages: List[Dict]) -> Dict:
        """
        Helper method to get AI response from OpenRouter.

        Args:
            messages: List of message dictionaries

        Returns:
            Dict with analysis and model info
        """
        try:
            response = self.openai_client.chat.completions.create(
                model=self.model,
                messages=messages
            )

            if not response or not hasattr(response, 'choices') or not response.choices:
                raise ValueError("Invalid response from OpenRouter")

            return {
                'content': response.choices[0].message.content if response.choices else "No response generated",
                'model': response.model if hasattr(response, 'model') else self.model
            }
        except Exception as e:
            logger.error(f"Error in AI response: {str(e)}")
            return {
                'content': f"Error getting AI response: {str(e)}",
                'model': "error"
            }

    def get_ai_analysis(self, pr: PullRequest, analysis: Dict) -> Dict:
        """
        Get AI analysis of the changes using OpenRouter.

        Args:
            pr (PullRequest): GitHub pull request object
            analysis (Dict): Analysis results from analyze_diff

        Returns:
            Dict: AI analysis results
        """
        try:
            context = f"""
Pull Request Title: {pr.title}
Description: {pr.body}

Changes Overview:
- Files changed: {analysis['files_changed']}
- Lines added: {analysis['additions']}
- Lines deleted: {analysis['deletions']}

Modified Files:
{chr(10).join(f'- {f["filename"]}: {f["status"]}' for f in analysis['file_details'])}

Key Changes:
{chr(10).join(analysis['summary'])}

Detailed Changes:
"""
            for file in analysis['file_details']:
                if file['patch']:
                    context += f"\n{file['filename']} changes:\n{file['patch']}\n"

            messages = [
                {"role": "system", "content": """
You are a senior software engineer reviewing a pull request. Analyze the changes and provide:
1. Impact assessment on the codebase
2. Potential risks or concerns
3. Suggestions for improvement
4. Documentation updates needed
Keep the analysis concise but comprehensive."""},
                {"role": "user", "content": context}
            ]

            response = self.get_ai_response(messages)

            return {
                'analysis': response['content'],
                'model_used': response['model']
            }

        except Exception as e:
            logger.error(f"Error getting AI analysis: {str(e)}")
            return {
                'analysis': f"Error getting AI analysis: {str(e)}",
                'model_used': "error"
            }

    def update_documentation(self, pr: PullRequest, analysis: Dict) -> str:
        """
        Generate documentation updates based on the changes.

        Args:
            pr (PullRequest): GitHub pull request object
            analysis (Dict): Analysis results

        Returns:
            str: Documentation update suggestions
        """
        try:
            docs_context = f"""
Pull Request: {pr.title}
Changes:
{chr(10).join(analysis['summary'])}

Files changed:
{chr(10).join(f'- {f["filename"]}' for f in analysis['file_details'])}
"""

            messages = [
                {"role": "system", "content": """
Analyze the changes and suggest documentation updates. Consider:
1. What new features or changes need documentation
2. Which existing docs need updating
3. Code examples or usage instructions needed
Provide specific suggestions for documentation changes."""},
                {"role": "user", "content": docs_context}
            ]

            response = self.get_ai_response(messages)
            return response['content']

        except Exception as e:
            logger.error(f"Error generating documentation updates: {str(e)}")
            return f"Error generating documentation suggestions: {str(e)}"

    def create_summary_comment(self, analysis: Dict, ai_analysis: Dict, doc_updates: str, commit_sha: str) -> str:
        """
        Create a formatted summary comment from all analyses.

        Args:
            analysis (Dict): Analysis results from analyze_diff
            ai_analysis (Dict): Results from AI analysis
            doc_updates (str): Documentation update suggestions
            commit_sha (str): The SHA of the commit being analyzed

        Returns:
            str: Formatted comment text
        """
        comment = f"{self.bot_signature}\n"
        comment += f"Analyzed commit: {commit_sha}\n\n"
        comment += "## 🤖 Pull Request Analysis\n\n"

        # Overall statistics
        comment += "### 📊 Statistics\n"
        comment += f"- Files changed: {analysis['files_changed']}\n"
        comment += f"- Lines added: {analysis['additions']}\n"
        comment += f"- Lines deleted: {analysis['deletions']}\n\n"

        # AI Analysis
        comment += "### 🧠 AI Code Review\n"
        comment += f"Analysis by {ai_analysis['model_used']}:\n"
        comment += f"{ai_analysis['analysis']}\n\n"

        # Documentation Updates
        comment += "### 📚 Documentation Updates Needed\n"
        comment += f"{doc_updates}\n\n"

        # Notable changes
        if analysis['summary']:
            comment += "### 🔍 Notable Changes\n"
            for change in analysis['summary']:
                comment += f"- {change}\n"
            comment += "\n"

        # Detailed file changes
        comment += "### 📝 File Details\n"
        for file in analysis['file_details']:
            comment += f"- **{file['filename']}**\n"
            comment += f"  - Status: {file['status']}\n"
            comment += f"  - Changes: +{file['additions']}/-{file['deletions']}\n"

        return comment

    def post_analysis(self, repo_name: str, pr_number: int) -> None:
        """
        Analyze a pull request and post the analysis as a comment.

        Args:
            repo_name (str): Repository name in format 'owner/repo'
            pr_number (int): Pull request number
        """
        try:
            # Get pull request
            pr = self.get_pull_request(repo_name, pr_number)

            # Check if we should analyze this PR
            should_analyze, current_commit = self.should_analyze_pr(pr)

            if not should_analyze:
                logger.info("Skipping analysis as no new commits found.")
                return

            # Analyze the diff
            analysis = self.analyze_diff(pr)

            # Get AI analysis
            ai_analysis = self.get_ai_analysis(pr, analysis)

            # Get documentation update suggestions
            doc_updates = self.update_documentation(pr, analysis)

            # Create and post comment
            comment = self.create_summary_comment(analysis, ai_analysis, doc_updates, current_commit)
            pr.create_issue_comment(comment)

            logger.info(f"Successfully posted analysis to PR #{pr_number} for commit {current_commit[:8]}")

        except Exception as e:
            logger.error(f"Error in post_analysis: {str(e)}")
            raise

def main():
    """Main entry point for the script."""
    # Load environment variables
    load_dotenv()

    # Parse command line arguments
    parser = argparse.ArgumentParser(description='GitHub PR Diff Analyzer')
    parser.add_argument('--repo', required=True, help='Repository name (owner/repo)')
    parser.add_argument('--pr', type=int, required=True, help='Pull request number')
    parser.add_argument('--model', default='anthropic/claude-3.5-sonnet',
                       help='OpenRouter model to use (default: anthropic/claude-3.5-sonnet)')
    args = parser.parse_args()

    # Get required tokens from environment
    github_token = os.getenv('GITHUB_TOKEN')
    openrouter_key = os.getenv('OPENROUTER_API_KEY')

    if not github_token:
        logger.error("GITHUB_TOKEN environment variable is not set")
        sys.exit(1)

    if not openrouter_key:
        logger.error("OPENROUTER_API_KEY environment variable is not set")
        sys.exit(1)

    try:
        # Initialize and run analyzer
        analyzer = PRDiffAnalyzer(github_token, openrouter_key, args.model)
        analyzer.post_analysis(args.repo, args.pr)
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()