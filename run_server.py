import subprocess
import sys
import os

# Only works on Windows
venv_path = os.path.join(os.path.dirname(__file__), '.venv')

python_executable = os.path.join(venv_path, 'Scripts', 'python.exe')

subprocess.run([python_executable, '-m', 'streamlit', 'run', "main.py"])
