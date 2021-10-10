from finite_state_machine import StateMachine, transition


async def async_is_approved_or_is_admin(machine, user):
    return machine.num_approvals >= 1 or user.is_admin


def sync_is_approved_or_is_admin(machine, user):
    return machine.num_approvals >= 1 or user.is_admin


class GitHubPullRequest(StateMachine):
    """State Machine to represent a GitHub Pull Request workflow"""

    def __init__(self):
        self.state = "opened"
        self.num_approvals = 0
        self.changes_request = False

    @transition(source="opened", target="opened")
    async def approve(self):
        self.num_approvals += 1

    @transition(source="opened", target="opened")
    async def request_changes(self):
        self.changes_request = True

    @transition(source="opened", target="closed")
    async def close_pull_request(self):
        pass

    @transition(
        source="opened",
        target="merged",
        conditions=[async_is_approved_or_is_admin],
    )
    async def fully_async_merge_pull_request(self, user):
        pass

    @transition(
        source="opened",
        target="merged",
        conditions=[sync_is_approved_or_is_admin],
    )
    async def async_merge_pull_request_with_sync_condition(self, user):
        pass
