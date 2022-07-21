# cs-fundamentals
Python project to hone computer science fundamentals of data structures, algorithms and problem solving patterns.
Includes pytests to verify implementation accuracy for normal and practice classes.

## Requirements
- Python3 is already installed on your system
- https://www.python.org/downloads/

## Preferred
- Anaconda is already installed on your system
- https://www.anaconda.com/products/distribution#Downloads

## Conda Setup
- Create conda environment
```commandline
conda env create -f environment.yml
```

- Activate conda new environment
```commandline
conda activate cs-fundamentals-env
```

## Pip/VirtualEnv Setup
- Install Pip:
```commandline
python3 -m pip install --user --upgrade pip
```

- For Ubuntu, install pip, venv, and git:
```commandline
sudo apt-get update
sudo apt install python3-pip
sudo apt install python3.10-venv
sudo apt-get install git
```

- Create virtual environment:
```commandline
mkdir ~/envs
python3 -m venv envs/cs-fundamentals-env
```

- Activate virtual environment:
```commandline
source envs/cs-fundamentals-env/bin/activate
```

- Install required packages from requirements.txt:
```commandline
cd ~/Projects/cs-fundamentals
pip install -r requirements.txt
```


## Usage
- Implement the practice class of your choice.
- Run pytest against the desired module.
```commandline
pytest automation/test_sorting.py
```

- Run pytest against the desired package.
```commandline
pytest automation/test_data_structures
```

- Execute all automation tests.
```commandline
pytest automation
```

- If using an IDE like PyCharm, right-click on the test module or package and select `Run <test_module or test_package>` or use hotkeys CTRL + SHIFT + F10 to execute the current test module.
