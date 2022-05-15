def log(content):
    print(content)

def GetTree(path):
    output = dict()
    files = glob.glob("*.*", root_dir=path)
    for f in files:
        lastModified = datetime.datetime.fromtimestamp(os.path.getmtime(f))
        fullPath = os.path.join(path, f)
        monthsFiles = output.setdefault(str(lastModified.month), [ ])
        monthsFiles.append(fullPath)
    return output

def GetDirectory(workingDirectory, month, execute):
    directoryPath = os.path.join(workingDirectory, month)
    if not os.path.exists(directoryPath) and execute:
        os.mkdir(directoryPath)
    print("Created " + directoryPath)
    return directoryPath

def MoveFile(workingDirectory,key, file, execute):
    filename = os.path.basename(file)
    newPath = os.path.join(workingDirectory, key, filename)
    if execute:
        os.rename(file, newPath)
    print(file + " -> " + newPath)

def SortTree(workingDirectory, tree, execute):
    for month in tree:
        target = GetDirectory(workingDirectory, month, execute)
        for file in tree[month]:
            MoveFile(workingDirectory, month, file, execute)
    return

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
    parser.add_argument('-x', help='Execute. Executes file actions. Defaults to false.', dest='execute', default=False)
    parser.add_argument('-v', help='Verbose. Lists all actions taken. Defaults to false.', dest='verbose', default=False)
    parser.add_argument('directory', type=isDirectoryValidator, nargs='?', default=currentDirectory, help='The directory in which to operate.')

    args = parser.parse_args()

    print(args.directory)
    print(args.recursive)

    import glob
    import datetime

    tree = GetTree(args.directory)

    SortTree(args.directory , tree, args.execute)
    
