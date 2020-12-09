"""
Upgrades all site packages for specified
python version.

"""

# Relevant library imports
import subprocess

# Specify Python version and requirements file
py_version = 'python3.7'
reqs_file = '../Desktop/' + '_'.join(py_version.split('.')) + '_requirements.txt'

# Create requirements file from which to upgrade packages
req_cmd = subprocess.run(py_version + ' -m pip freeze > ' + reqs_file, shell=True)

# Open requirements file and make relevant upgrades
with open(reqs_file) as requirements_file:
    for line in requirements_file:
        upgrade_cmd = subprocess.run(py_version + ' -m pip install --upgrade ' + line.strip().split('==')[0], shell=True, capture_output=True)
        print(upgrade_cmd.stdout.decode())

