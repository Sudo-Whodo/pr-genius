import pytest
from unittest.mock import Mock, patch
from pr_diff_analyzer import PRDiffAnalyzer

@pytest.fixture
def mock_github():
    return Mock()

@pytest.fixture
def mock_openai():
    return Mock()

@pytest.fixture
def analyzer(mock_github, mock_openai):
    with patch('pr_diff_analyzer.Github', return_value=mock_github), \
         patch('pr_diff_analyzer.OpenAI', return_value=mock_openai):
        return PRDiffAnalyzer("test-token", "test-key")

def test_init(analyzer):
    assert analyzer.model == "anthropic/claude-3.5-sonnet"
    assert analyzer.bot_signature == "<!-- PR-DIFF-BOT-COMMENT -->"

def test_get_pull_request(analyzer, mock_github):
    mock_repo = Mock()
    mock_pr = Mock()
    mock_github.get_repo.return_value = mock_repo
    mock_repo.get_pull.return_value = mock_pr

    result = analyzer.get_pull_request("owner/repo", 123)

    mock_github.get_repo.assert_called_once_with("owner/repo")
    mock_repo.get_pull.assert_called_once_with(123)
    assert result == mock_pr

def test_get_last_analyzed_commit(analyzer):
    mock_pr = Mock()
    mock_comments = Mock()
    mock_comment = Mock()
    mock_comment.body = "Analyzed commit: 1234567890abcdef1234567890abcdef12345678"
    mock_comments.reversed = [mock_comment]
    mock_pr.get_issue_comments.return_value = mock_comments

    result = analyzer.get_last_analyzed_commit(mock_pr)

    assert result == "1234567890abcdef1234567890abcdef12345678"

def test_should_analyze_pr_new_pr(analyzer):
    mock_pr = Mock()
    mock_pr.head.sha = "newsha123"

    with patch.object(analyzer, 'get_last_analyzed_commit', return_value=None):
        should_analyze, commit = analyzer.should_analyze_pr(mock_pr)

    assert should_analyze is True
    assert commit == "newsha123"

def test_should_analyze_pr_already_analyzed(analyzer):
    mock_pr = Mock()
    mock_pr.head.sha = "currentsha123"

    with patch.object(analyzer, 'get_last_analyzed_commit', return_value="currentsha123"):
        should_analyze, commit = analyzer.should_analyze_pr(mock_pr)

    assert should_analyze is False
    assert commit == "currentsha123"

def test_analyze_diff(analyzer):
    mock_pr = Mock()
    mock_file = Mock()
    mock_file.filename = "test.py"
    mock_file.status = "modified"
    mock_file.additions = 10
    mock_file.deletions = 5
    mock_file.changes = 15
    mock_file.patch = "@@ -1,5 +1,10 @@"

    mock_pr.get_files.return_value = [mock_file]
    mock_repo = Mock()
    mock_content = Mock()
    mock_content.decoded_content.decode.return_value = "file content"
    mock_repo.get_contents.return_value = mock_content
    mock_pr.get_repo.return_value = mock_repo

    result = analyzer.analyze_diff(mock_pr)

    assert result["files_changed"] == 1
    assert result["additions"] == 10
    assert result["deletions"] == 5
    assert len(result["file_details"]) == 1
    assert result["file_details"][0]["filename"] == "test.py"
    assert result["file_contents"]["test.py"] == "file content"

def test_get_ai_response(analyzer, mock_openai):
    messages = [{"role": "user", "content": "test"}]
    mock_response = Mock()
    mock_response.choices = [Mock(message=Mock(content="AI response"))]
    mock_response.model = "test-model"
    mock_openai.chat.completions.create.return_value = mock_response

    result = analyzer.get_ai_response(messages)

    assert result["content"] == "AI response"
    assert result["model"] == "test-model"

def test_get_ai_analysis(analyzer):
    mock_pr = Mock()
    mock_pr.title = "Test PR"
    mock_pr.body = "Test description"

    analysis = {
        "files_changed": 1,
        "additions": 10,
        "deletions": 5,
        "file_details": [{"filename": "test.py", "status": "modified"}],
        "summary": ["Modified test.py"],
        "file_contents": {}
    }

    with patch.object(analyzer, 'get_ai_response', return_value={"content": "AI analysis", "model": "test-model"}):
        result = analyzer.get_ai_analysis(mock_pr, analysis)

    assert result["analysis"] == "AI analysis"
    assert result["model_used"] == "test-model"

def test_update_documentation(analyzer):
    mock_pr = Mock()
    mock_pr.title = "Test PR"

    analysis = {
        "summary": ["Modified test.py"],
        "file_details": [{"filename": "test.py"}]
    }

    with patch.object(analyzer, 'get_ai_response', return_value={"content": "Doc updates needed"}):
        result = analyzer.update_documentation(mock_pr, analysis)

    assert result == "Doc updates needed"

def test_create_summary_comment(analyzer):
    analysis = {
        "files_changed": 1,
        "additions": 10,
        "deletions": 5,
        "summary": ["Modified test.py"],
        "file_details": [{
            "filename": "test.py",
            "status": "modified",
            "additions": 10,
            "deletions": 5
        }]
    }

    ai_analysis = {
        "analysis": "AI review",
        "model_used": "test-model"
    }

    doc_updates = "Update docs"
    commit_sha = "testsha123"

    result = analyzer.create_summary_comment(analysis, ai_analysis, doc_updates, commit_sha)

    assert "PR Analysis" in result
    assert "Statistics" in result
    assert "AI Code Review" in result
    assert "Documentation Updates" in result