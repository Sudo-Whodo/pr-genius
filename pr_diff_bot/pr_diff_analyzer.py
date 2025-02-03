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
import sys
import os
from pr_diff_bot.llm_clients import get_llm_client

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class PRDiffAnalyzer:
    def __init__(self, github_token: str, model: str = None):
        """
        Initialize the PR Diff Analyzer with GitHub authentication.

        Args:
            github_token (str): GitHub personal access token
            model (str): Model to use (default: anthropic/claude-3.5-sonnet)
        """
        self.model = model  # Will be set by the LLM client's default if None
        self.github = Github(github_token)
        self.llm_client = get_llm_client()  # Uses environment variables for configuration
        self.bot_signature = "<!-- PR-DIFF-BOT-COMMENT -->"

        # Load system prompts
        self.default_system_content = """
You are a senior software engineer reviewing a pull request. Analyze the changes and provide:
1. Impact assessment on the codebase
2. Potential risks or concerns
3. Suggestions for improvement
4. Documentation updates needed
Keep the analysis concise but comprehensive."""

        self.default_docs_system_content = """
Analyze the changes and suggest documentation updates. Consider:
1. What new features or changes need documentation
2. Which existing docs need updating
3. Code examples or usage instructions needed
Provide specific suggestions for documentation changes."""

        # Get system prompts from environment variables
        self.system_content = os.getenv('PR_REVIEW_SYSTEM_CONTENT', self.default_system_content)
        self.docs_system_content = os.getenv('PR_REVIEW_DOCS_SYSTEM_CONTENT', self.default_docs_system_content)

        # Log the prompts being used
        logger.info("Using code review prompt:")
        logger.info(self.system_content)
        logger.info("Using documentation review prompt:")
        logger.info(self.docs_system_content)

    def get_pull_request(self, repo_name: str, pr_number: int) -> Tuple[Repository, PullRequest]:
        """
        Get a pull request object and its repository from GitHub.

        Args:
            repo_name (str): Repository name in format 'owner/repo'
            pr_number (int): Pull request number

        Returns:
            Tuple[Repository, PullRequest]: GitHub repository and pull request objects
        """
        try:
            repo = self.github.get_repo(repo_name)
            pr = repo.get_pull(pr_number)
            return repo, pr
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

    def analyze_diff(self, repo: Repository, pr: PullRequest) -> Dict:
        """
        Analyze the changes in a pull request.

        Args:
            repo (Repository): GitHub repository object
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
                        content = repo.get_contents(file.filename, ref=pr.head.sha)
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
        Helper method to get AI response using configured LLM client.

        Args:
            messages: List of message dictionaries

        Returns:
            Dict with analysis and model info
        """
        try:
            return self.llm_client.get_completion(messages, self.model)
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
                {"role": "system", "content": self.system_content},
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
                {"role": "system", "content": self.docs_system_content},
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
            # Get pull request and repository
            repo, pr = self.get_pull_request(repo_name, pr_number)

            # Check if we should analyze this PR
            should_analyze, current_commit = self.should_analyze_pr(pr)

            if not should_analyze:
                logger.info("Skipping analysis as no new commits found.")
                return

            # Analyze the diff
            analysis = self.analyze_diff(repo, pr)

            # Get AI analysis
            ai_analysis = self.get_ai_analysis(pr, analysis)

            # Get documentation update suggestions
            doc_updates = self.update_documentation(pr, analysis)

            # Create comment
            comment = self.create_summary_comment(analysis, ai_analysis, doc_updates, current_commit)

            # Check if we're in dry-run mode
            if os.getenv('DRY_RUN', '').lower() == 'true':
                logger.info("DRY RUN: Would post the following comment:")
                print("\n" + "="*80)
                print(comment)
                print("="*80 + "\n")
                logger.info(f"Skipping comment creation for PR #{pr_number} (dry run)")
            else:
                # Post comment to PR
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
    parser.add_argument('--provider', default='openrouter',
                       choices=['openrouter', 'ollama', 'bedrock'],
                       help='LLM provider to use (default: openrouter)')
    parser.add_argument('--model',
                       help='Model to use (if not specified, uses provider defaults)')
    args = parser.parse_args()

    # Get required tokens from environment
    github_token = os.getenv('GITHUB_TOKEN')
    if not github_token:
        logger.error("GITHUB_TOKEN environment variable is not set")
        sys.exit(1)

    # Set the LLM provider
    os.environ['LLM_PROVIDER'] = args.provider

    # Validate provider-specific requirements
    if args.provider == 'openrouter' and not os.getenv('OPENROUTER_API_KEY'):
        logger.error("OPENROUTER_API_KEY environment variable is required for OpenRouter")
        sys.exit(1)
    elif args.provider == 'bedrock':
        if not os.getenv('AWS_ACCESS_KEY_ID') or not os.getenv('AWS_SECRET_ACCESS_KEY'):
            logger.error("AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY are required for Bedrock")
            sys.exit(1)

    try:
        # Initialize and run analyzer
        analyzer = PRDiffAnalyzer(github_token, args.model)
        if args.model:
            logger.info(f"Using specified model: {args.model}")
        else:
            logger.info("Using provider's default model")
        analyzer.post_analysis(args.repo, args.pr)
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
