from collections import namedtuple
from examples.github_pull_request import GitHubPullRequest

User = namedtuple("User", "name github_id is_admin")


def test_approved_pr_can_be_merged():
    # Arrange
    github_pr = GitHubPullRequest()
    github_pr.approve()
    assert github_pr.state == "opened"
    user = User(name="Aly Sivji", github_id="alysivji", is_admin=False)

    # Act
    github_pr.merge_pull_request(user)

    # Assert
    assert github_pr.state == "merged"


def test_pr_with_no_approvals_can_be_merged_by_admin():
    # Arrange
    github_pr = GitHubPullRequest()
    assert github_pr.state == "opened"
    user = User(name="Aly Sivji", github_id="alysivji", is_admin=True)

    # Act
    github_pr.merge_pull_request(user)

    # Assert
    assert github_pr.state == "merged"


def test_request_approval():
    # Arrange
    github_pr = GitHubPullRequest()
    assert github_pr.state == "opened"

    # Act
    github_pr.request_changes()

    # Assert
    assert github_pr.state == "opened"


def test_close_pull_request():
    # Arrange
    github_pr = GitHubPullRequest()
    assert github_pr.state == "opened"

    # Act
    github_pr.close_pull_request()

    # Assert
    assert github_pr.state == "closed"
