import logging, os, shutil, sys

from helpers import file

def createdirectory(directory):
    '''Creates directory'''
    if directoryexists(directory):
        raise Exception(r'Directory already exists.')
    os.mkdir(directory)
    logging.info(r'Created directory: '+directory)
    return

def delete(directory,forcedelete=False):
    if not directoryexists(directory):
        raise Exception(r'Invalid directory.')
    files = getfiles(directory) 
    if (len(files) > 0) and not forcedelete:
        raise Exception(r'Directory is not empty.')
    else:
        for filename in files:
            file.delete(filename)
        for subdirectory in getdirectories(directory)[::-1]:
            os.rmdir(subdirectory)
            logging.info(r'Deleted directory: '+subdirectory)
    return

def directoryexists(directory):
    if not isinstance(directory,str):
        raise ValueError('Invalid argument for <directory>.\nAccepted types: '+str(str)+'\nGot type: '+str(type(directory)))
    else:
        return os.path.isdir(directory)

def getdirectories(directory):
    if not directoryexists(directory):
        raise Exception(r'Invalid directory.')
    directories = [directory]
    for path, dirs, __ in os.walk(directory):
        for subdirectory in dirs:
            directories.append(os.path.join(path,subdirectory))
    return directories

def getfiles(directory,ext=None,filterby=None):
    if not directoryexists(directory):
        raise Exception(r'Invalid directory.')

    filelist = []
    for path, dirs, files in os.walk(directory):
        for filename in files:
            if filterby is not None:
                if filterby not in filename:
                    continue # Skip if filename doesn't contain filterby
            
            if ext is not None:
                fileext = os.path.splitext(filename)[1]
                if fileext.lower() is not ext:
                    continue # Skip if file extension doesn't match
            
            filelist.append(os.path.join(path,filename))
    logging.info(r'Found '+str(len(files))+' file(s) in '+str(len(dirs))+' subdirectories.')
    return filelist

# def move(sourceDirectory,destDirecory,forceMove=False):
#     if directoryexists(destDirecory):
#         raise Exception(r'Destination directory already exists.')
#     for path, dirs, files in os.walk(directory):
#         for directory in dirs:
#             newDirectory = directory.replace(path,destDirecory)
#             if not directoryexists(newDirectory):
#                 createdirectory(newDirectory)
#         for filename in files:
#             newFilename = 1
#     return