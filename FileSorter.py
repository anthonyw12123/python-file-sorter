class Schemas:
    def __init__(self) -> None:
        pass

import os

def isDirectoryValidator(path):
    if not os.path.isdir(path):
        raise argparse.ArgumentError
    return path

if __name__ == '__main__':
    import os
    import argparse

    currentDirectory = os.getcwd()
    parser = argparse.ArgumentParser(description ='Filesorter. Organizes directory by scheme.')
    parser.add_argument('-r', help='Recursive. Defaults to false.', dest='recursive', default=False)
    parser.add_argument('directory', type=isDirectoryValidator, nargs='?', default=currentDirectory, help='The directory in which to operate.')

    args = parser.parse_args()

    print(args.directory)
    print(args.recursive)

