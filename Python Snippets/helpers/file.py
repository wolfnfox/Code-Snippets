import logging, os, shutil, sys
import numpy

def append_all_text(string,filename,encoding=r'utf-8',overwrite=True):
    return

def copy(filename):
    return

def delete(filename):
    if not fileexists(filename):
        raise FileNotFoundError
    os.remove(filename)
    logging.info('Deleted file: '+str(filename))
    return

def fileexists(filename):
    if not isinstance(filename,str):
        raise ValueError('Invalid argument for <filename>.\nAccepted types: '+str(str)+'\nGot type: '+str(type(filename)))
    else:
        return os.path.isfile(filename)

def filesize(filename,units=None):
    '''Returns filesize (defaults to 'KB')\n
       Options: 'B', 'KB', or 'MB' '''
    if not fileexists(filename):
        raise FileNotFoundError
    if units not in ['B', 'KB', 'MB', None]:
        raise ValueError('Invalid argument for <units>.\nAccepted types: '+str(str)+' \'B\', \'KB\', \'MB\' or '+str(None)+'\nGot type: '+str(type(units))+' \''+str(units)+'\'')
    filesize = os.stat(filename).st_size
    if (units == 'KB') or (units == None):
        if (filesize > 1024):
            filesize = int(numpy.ceil(filesize/1024))
        else:
            filesize = numpy.ceil((filesize*1000)/1024)/1000
    if units == 'MB':
        if (filesize > (1024**2)):
            filesize = int(numpy.ceil(filesize/(1024**2)))
        else:
            filesize = numpy.ceil((302577*1000**2)/(1024**2)/(1000))/1000
    return filesize

def getextension(filename):
    return

def move(fromFile,toFile,overwrite=True):
    return

def read_all_bytes(filename):
    return

def read_all_text(filename,encoding=r'utf-8'):
    return

def write_all_bytes(byteArray,filename,overwrite=True):
    return

def write_all_text(string,filename,encoding=r'utf-8',overwrite=True):
    return

def _incrementfilename(filename):
    if not fileexists(filename):
        return filename
    else:
        i = 1
        filename = filename+'('+str(i)+')'
        while fileexists(filename):
            i += 1
    return filename

def _readfile(filename,options):
    with open(filename,options) as fopen:
        array = fopen.read()
    return array

def _writefile(array,filename,options,encoding=None):
    if encoding:
        with open(filename,options,encoding) as fopen:
            fopen.write(array)
    else:
        with open(filename,options) as fopen:
            fopen.write(array)
    return
