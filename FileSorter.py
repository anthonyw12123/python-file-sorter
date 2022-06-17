"""
:doc: `filesorter.py` is a recursive file sorter, given a directory. Sorts by year and month.
"""

import argparse
import datetime
import glob
from itertools import chain
import logging
import os
import uuid
from collections import defaultdict, namedtuple

from mapping import Mapping


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
        action=argparse.BooleanOptionalAction,
        default=False)
    parser.add_argument('directory',
        type=is_directory_validator,
        nargs='?',
        default=os.getcwd(),
        help='The directory in which to operate.')
    parsed_args = parser.parse_args()
    return parsed_args

def is_mapping_processed(mapping):
    """utility method to determine if mapping is processed"""
    return mapping.source == mapping.target
def get_target_filename(input_path):
    """Return or derive unique filename"""
    if os.path.exists(input_path):
        logging.warning("File collision. Deriving new filename for %s" , input_path)
        file_extension = os.path.splitext(input_path)
        return os.path.join(
            os.path.dirname(input_path),
            uuid.uuid4().hex + file_extension[1])
def process_mapping(mapping, execute):
    """Universal processing of mapping"""
    if is_mapping_processed(mapping):
        logging.debug("Skipping file: %s" , mapping.source)
        return
    if execute:
        target_filename = get_target_filename(mapping.target)
        os.renames(mapping.source, target_filename)
    logging.info(mapping.source + " -> " + mapping.target)

def get_tree_using_memory(path):
    """trying to be more performant"""
    output = defaultdict(list)
    with os.scandir(path) as it:
        for entry in it:
            if not entry.is_file():
                print('recursing')
                child = get_tree_using_memory(os.path.join(path, entry.name))
                for key in child:
                    output[key] += (child[key])
            last_modified = datetime.datetime.fromtimestamp(entry.stat().st_mtime)
            output[last_modified.strftime("%Y-%m-%d")].append(os.path.join(path,last_modified.strftime("%Y-%m-%d"),os.path.basename(entry.name)))
    return output

def get_tree_by_date(path):
    """returns a dictionary tree with years, months, for file names; given a path"""
    output = defaultdict(list)
    Mapping = namedtuple('Mapping', [ 'source', 'target' ])
    for file in glob.iglob("**", root_dir=path, recursive=True):
        source_path = os.path.join(path, file)
        if not os.path.isfile(source_path):
            continue
        last_modified = datetime.datetime.fromtimestamp(os.path.getmtime(source_path))
        target_path = os.path.join(
            path,
            last_modified.strftime("%Y-%m-%d"),
            os.path.basename(file))
        file_mapping = Mapping(source=source_path, target=target_path)
        output[last_modified.strftime("%Y-%m-%d")].append(file_mapping)
    return output

def process_tree_by_date(tree, execute):
    """process dictionary of"""
    for date in tree:
        for item in tree[date]:
            if item is Mapping:
                process_mapping(item, execute)
            else:
                target = os.path.join(
                            os.path.curdir,
                            date,
                            os.path.basename(item)
                        )
                if execute:
                    os.renames(item, target)
                logging.info(item + " -> " + target)
            


def get_tree_with_years(path):
    """returns a dictionary tree with years, months, for file names; given a path"""
    output = defaultdict(lambda: defaultdict(list))
    Mapping = namedtuple('Mapping', [ 'source', 'target' ])

    for file in glob.iglob("**", root_dir=path, recursive=True):
        source_path = os.path.join(path, file)
        if not os.path.isfile(source_path):
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
                process_mapping(mapping, execute)

if __name__ == '__main__':
    logging.basicConfig(filename='filesorterlog.log', encoding='utf-8', level=logging.DEBUG)
    args = get_arguments()
    tree = get_tree_using_memory(args.directory)
    process_tree_by_date(tree, args.execute)
    logging.info("Finished.")
