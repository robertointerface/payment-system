
#!/usr/bin/env python3

import os
import pathlib
import shlex
import subprocess
from pathlib import Path
from typing import List

LAMBDAS_DIRECTORY = Path(__file__).parent.parent / 'lambdas'


def run_poetry_export(lambda_directory: Path) -> bytes:
    cmd = "poetry export --without-hashes"
    args = shlex.split(cmd)
    poetry_lock_file = lambda_directory/"poetry.lock"
    pyproject_toml = lambda_directory/"pyproject.toml"
    if not (poetry_lock_file.exists() and pyproject_toml.exists()):
        raise FileExistsError(f"Mandatory Poetry lock or pyproject.toml file missing {lambda_directory}")
    process = subprocess.run(args, cwd=lambda_directory, capture_output=True)

    try:
        process.check_returncode()
    except Exception as ex:
        print(f"Poetry export has failed for lambda directory {lambda_directory}")
        raise ex

    stdout = process.stdout
    return stdout


def process_lambda_directories(lambda_directories: List[Path]):
    for lambda_directory in lambda_directories:
        requirements_path = pathlib.Path(lambda_directory) / "requirements.txt"
        poetry_export_result = run_poetry_export(lambda_directory)
        requirements_path.write_bytes(poetry_export_result)


def get_all_lambda_directories(python_directory: Path) -> List[Path]:
    lambda_directories = []
    for item in python_directory.iterdir():
        if item.is_dir() and not str(item).endswith("__pycache__"):
            lambda_directories.append(item)
    return lambda_directories


def get_python_directory(project_directory: Path) -> Path:
    python_directory = project_directory
    return python_directory


if __name__ == '__main__':
    project_directories = [LAMBDAS_DIRECTORY]
    for directory in project_directories:
        python_dir = get_python_directory(directory)
        lambda_dirs = get_all_lambda_directories(python_dir)
        process_lambda_directories(lambda_dirs)
