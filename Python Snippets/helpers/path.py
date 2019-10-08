import logging, os

def combine(folder_path: str,filename: str) -> str:
    return os.path.join(folder_path,filename)

def get_filename(filename: str) -> str:
    return os.path.basename(filename)

def get_filename_without_extension(filename: str) -> str:
    if not isinstance(filename,str):
        raise ValueError('Invalid argument for <filename>.\nAccepted types: '+str(str)+'\nGot type: '+str(type(filename)))
    return os.path.splitext(get_filename(filename))[0]
