"""Functions for use in data updates"""

import os
from pathlib import Path
import shutil

import pytest


def run_tests(folder="all", local_glossary_folder=None, additional_test_paths=None):
    """runs integration tests and returns 0 for success"""
    source_file = os.getenv("GLOSSARY_FILEPATH")

    if source_file:
        target_file = f"{local_glossary_folder}/glossary.csv"
        shutil.copy(source_file, target_file)

    if folder == "all":
        tests_to_run = ["tests/integration", "tests/data_tests"]
    else:
        tests_to_run = [f"tests/integration/{folder}", f"tests/data_tests/{folder}"]
        about_the_data_path = (
            "tests/integration/non_page_files/test_about_the_data_page.py"
        )
        if Path(about_the_data_path).exists():
            tests_to_run.append(about_the_data_path)

    if additional_test_paths:
        tests_to_run.extend(additional_test_paths)

    plugin = TestResultPlugin()
    test_result = pytest.main(
        tests_to_run,
        plugins=[plugin],
    )
    if os.path.exists(target_file):
        os.remove(target_file)
    return plugin, test_result


class TestResultPlugin:
    """
    Plugin to capture names of failed tests.
    """

    # pylint: disable=too-few-public-methods
    def __init__(self):
        self.failed_tests = []

    def pytest_runtest_logreport(self, report):
        "Collect the name of the test if it failed during the 'call' phase (test execution)"
        if report.failed and report.when == "call":
            self.failed_tests.append(report.nodeid)
