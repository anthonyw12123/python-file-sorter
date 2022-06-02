"""
:doc: `filesorter.py` is a recursive file sorter, given a directory. Sorts by year and month.
"""

from collections import defaultdict, namedtuple
import glob
import datetime
import os
import argparse
import logging

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
def is_mapping_processed(mapping):
    return mapping.source == mapping.target
def get_target_filename(input_path):
    import uuid
    if(os.path.exists(input_path)):
        logging.warning("File collision. Deriving new filename for " + input_path)
        file_extension = os.path.splitext(input_path)
        return os.path.join(
            os.path.dirname(input_path),
            uuid.uuid4().hex + file_extension[1])
    return input_path
def process_full_tree(full_tree, execute):
    """Executes moves a full tree"""
    for year in full_tree:
        for month in full_tree[year]:
            for mapping in full_tree[year][month]:
                if is_mapping_processed(mapping):
                    logging.debug("Skipping file: " + mapping.source)
                    continue
                if execute:
                    target_filename = get_target_filename(mapping.target)
                    os.renames(mapping.source, target_filename)
                logging.info(mapping.source + " -> " + mapping.target)

if __name__ == '__main__':
    logging.basicConfig(filename='filesorterlog.log', encoding='utf-8', level=logging.DEBUG)
    args = get_arguments()
    tree = get_tree_with_years(args.directory)
    process_full_tree(tree, args.execute)
    logging.info("Finished.")
