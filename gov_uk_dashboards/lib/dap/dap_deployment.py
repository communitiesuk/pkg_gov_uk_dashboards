"""
Scripts for deploying dashboard code to the DLUHC DAP Hosting Area.
The DAP Hosting area is maintained by the DLUHC DAP Support team.
"""

import subprocess
import tempfile


def deploy_main_branch_to_pydash_test_environment(
    github_repo: str, dap_repo: str, dap_repo_folder_name: str
):
    """
    Deploying to the DLUHC DAP hosting area involves pushing the dashboards code
    from the GitHub main branch to the pydash repos test branch

    See also our internal documentation section "DAP Hosting environment (pydash)"
    https://github.com/communitiesuk/plotly_dashboard_docs#dap-hosting-environment-pydash
    """
    with tempfile.TemporaryDirectory() as temporary_cloning_directory:
        pydash_repo = _clone_repo(
            url=dap_repo,
            into=temporary_cloning_directory,
            path_to_code=dap_repo_folder_name,
        )

        _add_git_remote(
            url=github_repo,
            name="github",
            repo_path=pydash_repo,
        )

        _update_git_reference(
            branch="Test",
            to_point_at="github/main",
            repo_path=pydash_repo,
        )

        _force_push_changes_to_test_branch_of_pydash_repo(
            branch="Test", repo_path=pydash_repo
        )


def _clone_repo(url: str, path_to_code: str, into: str) -> str:
    subprocess.check_call(
        ["git", "clone", url],
        cwd=into,
    )
    return f"{into}\\{path_to_code}"


def _add_git_remote(url: str, name: str, repo_path: str):
    subprocess.check_call(
        [
            "git",
            "remote",
            "add",
            name,
            url,
        ],
        cwd=repo_path,
    )
    subprocess.check_call(["git", "fetch", name], cwd=repo_path)


def _update_git_reference(branch: str, to_point_at: str, repo_path: str):
    _checkout_branch(repo_path, branch=branch)

    subprocess.check_call(
        ["git", "reset", "--hard", to_point_at],
        cwd=repo_path,
    )


def _checkout_branch(repo_path: str, branch: str):
    return subprocess.check_call(["git", "checkout", branch], cwd=repo_path)


def _force_push_changes_to_test_branch_of_pydash_repo(
    branch: str,
    repo_path: str,
):
    subprocess.check_call(
        ["git", "push", "--force-with-lease", "origin", branch],
        cwd=repo_path,
    )
