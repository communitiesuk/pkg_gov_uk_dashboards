"""Utilities for writing dashboard pathname manifests to a shared directory.

This module generates a JSON manifest of valid dashboard pathnames for a repo.
It is intended to support downstream consumers, such as KPI processing, that
need a whitelist of known dashboard paths and should exclude unexpected or
manually entered URLs.

The manifest is only rewritten when the set of dashboard pathnames has changed.
"""

import json
from pathlib import Path


def update_dashboard_path_manifest(
    dashboards: list,
    manifest_dir: str | None,
    repo_name: str,
) -> None:
    """Write dashboard pathnames to a repo-specific manifest file only if changed."""
    if not manifest_dir or not manifest_dir.strip():
        raise ValueError(
            "DASHBOARD_PATH_MANIFEST_DIR is not set. "
            "Please add it to your environment variables."
        )

    safe_repo_name = repo_name.lower().replace(" ", "_")
    output_path = Path(manifest_dir) / f"{safe_repo_name}.json"

    pathnames = sorted(
        {
            dashboard.pathname
            for dashboard in dashboards
            if getattr(dashboard, "pathname", None)
        }
    )

    new_payload = {
        "repo": repo_name,
        "paths": pathnames,
    }
    new_content = json.dumps(new_payload, sort_keys=True, separators=(",", ":"))

    if output_path.exists():
        existing_content = output_path.read_text(encoding="utf-8")
        if existing_content == new_content:
            return

    output_path.parent.mkdir(parents=True, exist_ok=True)

    temp_path = output_path.with_suffix(".tmp")
    temp_path.write_text(new_content, encoding="utf-8")
    temp_path.replace(output_path)
