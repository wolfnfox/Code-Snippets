import logging, os, shutil, sys

from Helpers import File

def CreateDirectory(directory):
    '''Creates directory'''
    if DirectoryExists(directory):
        raise Exception(r'Directory already exists.')
    os.mkdir(directory)
    logging.info(r'Created directory: '+directory)
    return

def Delete(directory,forcedelete=False):
    if not DirectoryExists(directory):
        raise Exception(r'Invalid directory.')
    files = GetFiles(directory) 
    if (len(files) > 0) and not forcedelete:
        raise Exception(r'Directory is not empty.')
    else:
        for filename in files:
            File.Delete(filename)
        for subdirectory in GetDirectories(directory)[::-1]:
            os.rmdir(subdirectory)
            logging.info(r'Deleted directory: '+subdirectory)
    return

def DirectoryExists(directory):
    if not isinstance(directory,str):
        raise ValueError('Invalid argument for <directory>.\nAccepted types: '+str(str)+'\nGot type: '+str(type(directory)))
    else:
        return os.path.isdir(directory)

def GetDirectories(directory):
    if not DirectoryExists(directory):
        raise Exception(r'Invalid directory.')
    directories = [directory]
    for path, dirs, files in os.walk(directory):
        for subdirectory in dirs:
            directories.append(os.path.join(path,subdirectory))
    return directories

def GetFiles(directory,ext=None,filterby=None):
    if not DirectoryExists(directory):
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

# def Move(sourceDirectory,destDirecory,forceMove=False):
#     if DirectoryExists(destDirecory):
#         raise Exception(r'Destination directory already exists.')
#     for path, dirs, files in os.walk(directory):
#         for directory in dirs:
#             newDirectory = directory.replace(path,destDirecory)
#             if not DirectoryExists(newDirectory):
#                 CreateDirectory(newDirectory)
#         for filename in files:
#             newFilename = 1
#     return