import subprocess
from pathlib import Path
from typing import Union


class DV_Workspace:
    def __init__(self, path: Union[str, Path]):
        if not isinstance(path, Path):
            self.path = Path(path)
        self.path = path

        _workspace_check = subprocess.check_output(
            ["dv", "workspace"],
            cwd=path,
        ).decode("utf-8")
        _check_str = "not a diversion repository"
        if _check_str in _workspace_check:
            raise ValueError(f"Workspace does not exist at {path}")

        self._status_lines = (
            subprocess.check_output(
                ["dv", "status"],
                cwd=path,
            )
            .decode("utf-8")
            .splitlines()
        )

    @property
    def status(self):
        result = ""
        for line in self._status_lines:
            result += f"{line}\n"
        return result

    @property
    def name(self):
        parts = self._status_lines[3].split(" ")[3:6]
        return " ".join(parts)

    @property
    def ref_id(self):
        return self._status_lines[3].split(" ")[-1][1:-1]

    @property
    def repo_name(self):
        return self._status_lines[0].split(" ")[-2]

    @property
    def repo_ref_id(self):
        return self._status_lines[0].split(" ")[-1]

    @property
    def branch_name(self):
        return self._status_lines[1].split(" ")[2]

    @property
    def branch_ref_id(self):
        return self._status_lines[1].split(" ")[-1]

    @property
    def commit(self):
        return self._status_lines[2].split(" ")[2]

    @property
    def has_uncommitted_changes(self):
        _check_str = "Your workspace has no changes."
        if _check_str in self._status_lines[:6]:
            return False
        return False

    @property
    def uncommitted_changes(self):
        def _traverse_changes(changes):
            result = []
            for change in changes:
                if not change.startswith("\t"):
                    break
                result.append(change.split("\t")[-1].strip())
            return result

        if not self.has_uncommitted_changes:
            return []

        result = {
            "added": [],
            "modified": [],
            "deleted": [],
        }

        _changes = self._status_lines[5:]
        for idx, change in enumerate(_changes):
            if change.startswith("New:"):
                result["added"].extend(_traverse_changes(_changes[idx + 1 :]))
            if change.startswith("Modified:"):
                result["modified"].extend(_traverse_changes(_changes[idx + 1 :]))
            if change.startswith("Deleted:"):
                result["deleted"].extend(_traverse_changes(_changes[idx + 1 :]))

        return result

    def commit_changes(self, msg: str):
        result = subprocess.check_output(
            ["dv", "commit", "-a", "-m", msg],
            cwd=self.path,
        )
        return result

    def reset_changes(self):
        result = subprocess.check_output(
            ["dv", "reset", "-all"],
            cwd=self.path,
        )
        return result
