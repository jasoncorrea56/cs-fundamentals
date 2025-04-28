# cs-fundamentals
Python project to hone computer science fundamentals of data structures, algorithms and problem solving patterns. Includes pytests to verify implementation accuracy for normal and practice classes.

## Setup
This project supports Python 3, UV, Conda, and pip/virtualenv for dependency and virtual environment management. Linting and formatting are managed with pre-commit and ruff.

### Requirements
Python 3 is required for this project
- https://www.python.org/downloads/

### Pre-commit Setup
Install pre-commit hooks to automatically run linting and formatting prior to making a commit or run pre-commit manually anytime.

Install pre-commit hooks:
```shell
uv tool install pre-commit
pre-commit install
```

Manually run pre-commit hooks:
```shell
pre-commit run --all-files
```

### UV Setup
Install UV
- https://github.com/astral-sh/uv
- https://docs.astral.sh/uv/

Update UV:
```shell
uv self update
```

Add dependency with UV:
```shell
uv add ruff
```

Refresh dependencies in UV lockfile:
```shell
uv lock
```

Sync dependencies to venv:
```shell
uv sync
```

Run UV to execute tests:
```shell
uv run pytest automation
```

### Conda Setup
Install Anaconda
- https://www.anaconda.com/products/distribution#Downloads

Create conda environment:
```shell
conda env create -f environment.yml
```

Activate conda new environment:
```shell
conda activate cs-fundamentals-env
```

### Pip/VirtualEnv Setup
Install Pip:
```shell
python3 -m pip install --user --upgrade pip
```

For Ubuntu, install pip, venv, and git:
```shell
sudo apt-get update
sudo apt install python3-pip
sudo apt install python3.10-venv
sudo apt-get install git
```

Create virtual environment:
```shell
mkdir ~/envs
python3 -m venv envs/cs-fundamentals-env
```

Activate virtual environment:
```shell
source envs/cs-fundamentals-env/bin/activate
```

Install required packages from requirements.txt:
```shell
cd ~/Projects/cs-fundamentals
pip install -r requirements.txt
```

## Usage
1. Implement the practice class of your choice.
2. Run pytest against:
    - Module
        ```shell
        pytest automation/test_sorting.py
        ```

    - Package
        ```shell
        pytest automation/test_data_structures
        ```

    - All tests
        ```shell
        pytest automation
        ```

    - UV-specific syntax
        ```shell
        uv run pytest automation
        ```

NOTE: If using an IDE like VSCode or PyCharm, right-click on the test module or package and select `Run <test_module or test_package>` or use hotkeys CTRL + SHIFT + F10 to execute the current test module.
