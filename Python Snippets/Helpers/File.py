import logging, os, shutil, sys
import numpy

def AppendAllText(string,filename,encoding=r'utf-8',overwrite=True):
    return

def Copy(filename):
    return

def Delete(filename):
    if not FileExists(filename):
        raise FileNotFoundError
    os.remove(filename)
    logging.info('Deleted file: '+str(filename))
    return

def FileExists(filename):
    if not isinstance(filename,str):
        raise ValueError('Invalid argument for <filename>.\nAccepted types: '+str(str)+'\nGot type: '+str(type(filename)))
    else:
        return os.path.isfile(filename)

def FileSize(filename,units=None):
    '''Returns filesize (defaults to 'KB')\n
       Options: 'B', 'KB', or 'MB' '''
    if not FileExists(filename):
        raise FileNotFoundError
    if units not in ['B', 'KB', 'MB', None]:
        raise ValueError('Invalid argument for <units>.\nAccepted types: '+str(str)+' \'B\', \'KB\', \'MB\' or '+str(None)+'\nGot type: '+str(type(units))+' \''+str(units)+'\'')
    filesize = os.stat(filename).st_size
    if (units == 'KB') or (units == None):
        if (filesize > 1024):
            return int(numpy.ceil(filesize/1024))
        else:
            return numpy.ceil((filesize*1000)/1024)/1000
    if units == 'B':
        return filesize
    if units == 'MB':
        if (filesize > (1024**2)):
            return int(numpy.ceil(filesize/(1024**2)))
        else:
            return numpy.ceil((302577*1000**2)/(1024**2))/(1000**2)

def GetExtension(filename):
    return

def Move(fromFile,toFile,overwrite=True):
    return

def ReadAllBytes(filename):
    return

def ReadAllText(filename,encoding=r'utf-8'):
    return

def WriteAllByte(byteArray,filename,overwrite=True):
    return

def WriteAllText(string,filename,encoding=r'utf-8',overwrite=True):
    return

def _IncrementFilename(filename):
    if not FileExists(filename):
        return filename
    else:
        i = 1
        filename = filename+'('+str(i)+')'
        while FileExists(filename):
            i += 1
    return filename

def _ReadFile(filename,options):
    with open(filename,options) as fopen:
        array = fopen.read()
    return array

def _WriteFile(array,filename,options,encoding=None):
    if encoding:
        with open(filename,options,encoding) as fopen:
            fopen.write(array)
    else:
        with open(filename,options) as fopen:
            fopen.write(array)
    return
