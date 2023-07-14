import ast
import importlib
import logging
import subprocess
from tkinter import Tk
from tkinter.filedialog import askopenfilename

# Step 1: Select user's script using file explorer
Tk().withdraw()
file_path = askopenfilename(title="Select Python script file")

# Step 2: Configure logging
logging.basicConfig(filename='log.txt', level=logging.INFO)

# Step 3: Analyze the script
with open(file_path, "r") as file:
    tree = ast.parse(file.read())

imported_packages = set()
for node in ast.walk(tree):
    if isinstance(node, ast.Import):
        for alias in node.names:
            imported_packages.add(alias.name)
    elif isinstance(node, ast.ImportFrom):
        imported_packages.add(node.module)

# Step 4: Install required packages
for package in imported_packages:
    try:
        importlib.import_module(package)
        logging.info(f"Package {package} is already installed and not required.")
    except ImportError:
        logging.info(f"Installing package: {package}")
        result = subprocess.call(['pip', 'install', package])
        if result == 0:
            logging.info(f"Package {package} successfully installed.")
        else:
            logging.error(f"Failed to install package: {package}")
