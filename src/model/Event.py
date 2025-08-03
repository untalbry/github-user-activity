class Event:
    def __init__(self, type, repo_name, created_at, commits, branch):
        self.type = type
        self.repo_name = repo_name
        self.created_at = created_at
        self.commits = commits
        self.branch = branch 