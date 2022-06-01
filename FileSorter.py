"""
:doc: `filesorter.py` is a recursive file sorter, given a directory. Sorts by year and month.
"""

from collections import defaultdict, namedtuple
import glob
import datetime
import os
import argparse
from genericpath import isfile

def is_directory_validator(path):
    """validates a given directory"""
    if not os.path.isdir(path):
        raise argparse.ArgumentError
    return path

def get_arguments():
    """Gets the arguments for the utility."""
    parser = argparse.ArgumentParser(description ='Filesorter. Organizes directory by scheme.')
    parser.add_argument('-x', 
        help='Execute. Executes file actions. Defaults to false.',
        dest='execute',
        default=False)
    parser.add_argument('directory',
        type=is_directory_validator,
        nargs='?',
        default=os.getcwd(),
        help='The directory in which to operate.')
    parsed_args = parser.parse_args()

    return parsed_args

def get_tree_with_years(path):
    """returns a dictionary tree with years, months, for file names; given a path"""
    output = defaultdict(lambda: defaultdict(list))
    Mapping = namedtuple('Mapping', [ 'source', 'target' ])

    for file in glob.iglob("**", root_dir=path, recursive=True):
        source_path = os.path.join(path, file)
        if not isfile(source_path):
            continue
        last_modified = datetime.datetime.fromtimestamp(os.path.getmtime(source_path))
        target_path = os.path.join(
            path,
            str(last_modified.year),
            str(last_modified.month),
            os.path.basename(file))
        file_mapping = Mapping(source=source_path, target=target_path)
        output[last_modified.year][last_modified.month].append(file_mapping)
    return output
def process_full_tree(full_tree, execute):
    """Executes moves a full tree"""
    for year in full_tree:
        for month in full_tree[year]:
            for mapping in full_tree[year][month]:
                if execute:
                    os.renames(mapping.source, mapping.target)
                print(mapping.source + " -> " + mapping.target)

if __name__ == '__main__':
    args = get_arguments()
    tree = get_tree_with_years(args.directory)
    process_full_tree(tree, args.execute)
    print("Finished.")
