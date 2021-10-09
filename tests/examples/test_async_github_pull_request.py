from collections import namedtuple

import pytest

from finite_state_machine.exceptions import ConditionsNotMet
from examples.async_github_pull_request import GitHubPullRequest

User = namedtuple("User", "name github_id is_admin")


@pytest.mark.asyncio
async def test_approved_pr_can_be_merged__with_sync_condition_function():
    # Arrange
    github_pr = GitHubPullRequest()
    await github_pr.approve()
    assert github_pr.state == "opened"
    user = User(name="Aly Sivji", github_id="alysivji", is_admin=False)

    # Act
    await github_pr.async_merge_pull_request_with_sync_condition(user)

    # Assert
    assert github_pr.state == "merged"


@pytest.mark.asyncio
async def test_approved_pr_can_be_merged__fully_async():
    # Arrange
    github_pr = GitHubPullRequest()
    await github_pr.approve()
    assert github_pr.state == "opened"
    user = User(name="Aly Sivji", github_id="alysivji", is_admin=False)

    # Act
    await github_pr.fully_async_merge_pull_request(user)

    # Assert
    assert github_pr.state == "merged"


@pytest.mark.asyncio
async def test_pr_with_no_approvals_cannot_be_merged():
    # Arrange
    github_pr = GitHubPullRequest()
    assert github_pr.state == "opened"
    user = User(name="Aly Sivji", github_id="alysivji", is_admin=False)

    # Act
    with pytest.raises(ConditionsNotMet):
        await github_pr.fully_async_merge_pull_request(user)


@pytest.mark.asyncio
async def test_pr_with_no_approvals_can_be_merged_by_admin():
    # Arrange
    github_pr = GitHubPullRequest()
    assert github_pr.state == "opened"
    user = User(name="Aly Sivji", github_id="alysivji", is_admin=True)

    # Act
    await github_pr.fully_async_merge_pull_request(user)

    # Assert
    assert github_pr.state == "merged"


@pytest.mark.asyncio
async def test_request_approval():
    # Arrange
    github_pr = GitHubPullRequest()
    assert github_pr.state == "opened"

    # Act
    await github_pr.request_changes()

    # Assert
    assert github_pr.state == "opened"
    assert github_pr.changes_request is True


@pytest.mark.asyncio
async def test_close_pull_request():
    # Arrange
    github_pr = GitHubPullRequest()
    assert github_pr.state == "opened"

    # Act
    await github_pr.close_pull_request()

    # Assert
    assert github_pr.state == "closed"
