import subprocess
from pathlib import Path
from typing import Any, Optional

import httpx


class FileTools:
    """Basic file operations for the agent tool API."""

    @staticmethod
    def read_file(path: str) -> dict[str, Any]:
        file_path = Path(path).expanduser()
        return {"success": True, "path": str(file_path), "content": file_path.read_text()}

    @staticmethod
    def write_file(path: str, content: str) -> dict[str, Any]:
        file_path = Path(path).expanduser()
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content)
        return {"success": True, "path": str(file_path)}

    @staticmethod
    def delete_file(path: str) -> dict[str, Any]:
        file_path = Path(path).expanduser()
        file_path.unlink(missing_ok=True)
        return {"success": True, "path": str(file_path)}

    @staticmethod
    def list_files(path: str = ".") -> dict[str, Any]:
        directory = Path(path).expanduser()
        files = [str(item) for item in directory.iterdir()]
        return {"success": True, "path": str(directory), "files": files}


class TerminalTools:
    """Terminal command execution helper."""

    @staticmethod
    def execute_command(command: str, timeout: int = 30, sandbox: bool = True) -> dict[str, Any]:
        completed = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
        return {
            "success": completed.returncode == 0,
            "command": command,
            "returncode": completed.returncode,
            "stdout": completed.stdout,
            "stderr": completed.stderr,
            "sandbox": sandbox,
        }


class GitHubTools:
    """Minimal GitHub REST client for repository and issue operations."""

    base_url = "https://api.github.com"

    def get_repo(self, owner: str, repo: str) -> dict[str, Any]:
        return self._get(f"/repos/{owner}/{repo}")

    def list_issues(self, owner: str, repo: str, state: str = "open") -> dict[str, Any]:
        return self._get(f"/repos/{owner}/{repo}/issues", params={"state": state})

    def create_issue(self, owner: str, repo: str, title: str, body: Optional[str] = None) -> dict[str, Any]:
        return {
            "success": False,
            "error": "Creating GitHub issues requires authentication and is not configured yet.",
            "owner": owner,
            "repo": repo,
            "title": title,
            "body": body,
        }

    def _get(self, path: str, params: Optional[dict[str, str]] = None) -> dict[str, Any]:
        response = httpx.get(f"{self.base_url}{path}", params=params, timeout=10)
        return {"success": response.is_success, "status_code": response.status_code, "data": response.json()}


github_tools = GitHubTools()
