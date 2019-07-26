import logging, os, shutil, sys

def Copy(filename):
    return

def Delete(filename):
    if not FileExists(filename):
        raise Exception(r'Invalid filename.')
    os.remove(filename)
    logging.info('Deleted file: '+str(filename))
    return

def FileExists(filename):
    return os.path.exists(filename)

def FileSize(filename,units='KB'):
    '''Returns filesize (defaults to 'KB')\n
       Options: 'B', 'KB', 'MB' '''
    if not FileExists(filename):
        raise Exception(r'Invalid filename.')
    if units not in ['B', 'KB', 'MB', None]:
        raise Exception(r'Invalid units.')
    filesize = os.stat(filename).st_size
    if (units == 'KB') or (units == None):
        return numpy.ceil(filesize/1024)
    if units == 'B':
        return = filesize
    if units == 'MB':
        numpy.ceil(filesize//1024/1024)

def IncrementFilename(filename):
    if not FileExists(filename):
        return filename
    else:
        
    return filename

def Move(fromFile,toFile,forceMove=False):
    return