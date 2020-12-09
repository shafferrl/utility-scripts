"""
Replace all instances of a string with another one 
in a specified directory.
"""

# Relevant library imports
import os, re, subprocess

# Target string and new string with which to replace it
target_string = 'new_home_site'
new_string = 'django_project'

# The root directory to make the changes to
target_dir = ''
# File types to check within for target string
file_types = {'js', 'css', 'html', 'py',}
# Subdirectories to exclude from search
exclude_dirs = {'venv',}

# Construct regular expression that looks for files of specified types
types_re = '('
for i, ftype in enumerate(file_types):
    if i < len(file_types) - 1:
        types_re += '\.' + ftype + '|'
    else:
        types_re += '\.' + ftype + ')$'

rel_dirs = []
rel_files = []
# Traverse the directory tree
for root, dirs, files in os.walk(target_dir):
    dirs[:] = [d for d in dirs if d not in exclude_dirs]
    for d in dirs:
        if target_string in d:
            rel_dirs.append(os.path.join(root, d))
    for file in files:
        if re.search(types_re, file):
            rel_files.append(os.path.join(root, file))

# Go into each file and check for and change target string
for file in rel_files:
    with open(file) as read_file:
        new_file = read_file.readlines()
        
    with open(file, 'w') as write_file:
        for line in new_file:
            if target_string in line:
                line = line.replace(target_string, new_string)
            write_file.write(line)
    
# Change any relevant file names
for file in rel_files:
    new_file = '/'.join(file.split('/')[:-1]) + '/' + file.split('/')[-1].replace(target_string, new_string)
    file_cmd = subprocess.run('mv '+ file +' '+ new_file, shell=True, capture_output=True) #Command for Unix-based systems

# Put lowest directories first to avoid issues changing names
rel_dirs.sort(reverse=True)

# Change directory names
for rd in rel_dirs:
    new_dir = '/'.join(rd.split('/')[:-1]) + '/' + rd.split('/')[-1].replace(target_string, new_string)
    dir_cmd = subprocess.run('mv '+ rd +' '+ new_dir, shell=True, capture_output=True) #Command for Unix-based systems

