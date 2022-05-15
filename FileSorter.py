"""
:doc: `filesorter.py` is a file sorter, given a directory. Sorts by month.
"""

import glob
import datetime
import os
import argparse

def is_directory_validator(path):
    """validates a given directory"""
    if not os.path.isdir(path):
        raise argparse.ArgumentError
    return path

def get_arguments():
    """Gets the arguments for the utility."""
    parser = argparse.ArgumentParser(description ='Filesorter. Organizes directory by scheme.')
    parser.add_argument('-r',
        help='Recursive. Defaults to false.',
        dest='recursive',
        default=False)
    parser.add_argument('-x', 
        help='Execute. Executes file actions. Defaults to false.',
        dest='execute',
        default=False)
    parser.add_argument('-v',
        help='Verbose. Lists all actions taken. Defaults to false.',
        dest='verbose',
        default=False)
    parser.add_argument('directory',
        type=is_directory_validator,
        nargs='?',
        default=os.getcwd(),
        help='The directory in which to operate.')
    parsed_args = parser.parse_args()

    return parsed_args

def get_tree(path):
    """returns a dictionary tree of months and filenames, given a path"""
    output = dict()
    files = glob.glob("*.*", root_dir=path)
    for file in files:
        last_modified = datetime.datetime.fromtimestamp(os.path.getmtime(f))
        full_path = os.path.join(path, file)
        months_files = output.setdefault(str(last_modified.month), [ ])
        months_files.append(full_path)
    return output

def get_directory_for_month(working_directory, month, execute):
    """Creates target directory for month. Returns created directory path."""
    directory_path = os.path.join(working_directory, month)
    if not os.path.exists(directory_path) and execute:
        os.mkdir(directory_path)
    print("Created " + directory_path)
    return directory_path
def move_file(working_directory,key, file, execute):
    """Moves a file to the target directory"""
    filename = os.path.basename(file)
    new_path = os.path.join(working_directory, key, filename)
    if execute:
        os.rename(file, new_path)
    print(file + " -> " + new_path)
def sort_tree(working_directory, directory_tree, execute):
    """Enacts sorting on a given directory_tree."""
    for month in directory_tree:
        target = get_directory_for_month(working_directory, month, execute)
        for file in directory_tree[month]:
            move_file(working_directory, month, file, execute)
    return

if __name__ == '__main__':
    args = get_arguments()
    tree = get_tree(args.directory)
    sort_tree(args.directory , tree, args.execute)
