import logging, os, shutil
import numpy

def append_all_text(text,filename,encoding=r'utf-8'):
    if not isinstance(text,str):
        raise ValueError('Invalid argument for <text>.\nAccepted types: '+str(str)+'\nGot type: '+str(type(text)))
    if not isinstance(filename,str):
        raise ValueError('Invalid argument for <filename>.\nAccepted types: '+str(str)+'\nGot type: '+str(type(filename)))
    if not isinstance(encoding,str):
        raise ValueError('Invalid argument for <encoding>.\nAccepted types: '+str(str)+'\nGot type: '+str(type(encoding)))
    if not fileexists(filename):
        raise FileNotFoundError()
    return _writefile(text,filename,'at',encoding)

def copy(fromfilename,tofilename=None,overwrite=False):
    if not isinstance(fromfilename,str):
        raise ValueError('Invalid argument for <fromfilename>.\nAccepted types: '+str(str)+'\nGot type: '+str(type(fromfilename)))
    if tofilename and not isinstance(tofilename,str):
        raise ValueError('Invalid argument for <tofilename>.\nAccepted types: '+str(None)+', '+str(str)+'\nGot type: '+str(type(tofilename)))
    if not isinstance(overwrite,bool):
        raise ValueError('Invalid argument for <overwrite>.\nAccepted types: '+str(bool)+'\nGot type: '+str(type(overwrite)))
    if not fileexists(fromfilename):
        raise FileNotFoundError()
    if (not tofilename):
        tofilename = fromfilename
    if (not overwrite):
        tofilename = _incrementfilename(tofilename)
        shutil.copy2(fromfilename,tofilename)
    else:
        if fileexists(tofilename):
            move(fromfilename,tofilename,overwrite)
        else:
            shutil.copy2(fromfilename,tofilename)
    logging.info('Copied file: '+str(fromfilename))
    logging.info('Copied to: '+str(tofilename))
    return tofilename

def delete(filename):
    if not isinstance(filename,str):
        raise ValueError('Invalid argument for <filename>.\nAccepted types: '+str(str)+'\nGot type: '+str(type(filename)))
    if not fileexists(filename):
        raise FileNotFoundError
    os.remove(filename)
    logging.info('Deleted file: '+str(filename))
    return True

def fileexists(filename):
    if not isinstance(filename,str):
        raise ValueError('Invalid argument for <filename>.\nAccepted types: '+str(str)+'\nGot type: '+str(type(filename)))
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
    if not isinstance(filename,str):
        raise ValueError('Invalid argument for <filename>.\nAccepted types: '+str(str)+'\nGot type: '+str(type(filename)))
    return os.path.splitext(filename)[-1]

def move(fromfilename,tofilename,overwrite=True):
    if not isinstance(fromfilename,str):
        raise ValueError('Invalid argument for <fromfilename>.\nAccepted types: '+str(str)+'\nGot type: '+str(type(fromfilename)))
    if not isinstance(tofilename,str):
        raise ValueError('Invalid argument for <tofilename>.\nAccepted types: '+str(str)+'\nGot type: '+str(type(tofilename)))
    if not isinstance(overwrite,bool):
        raise ValueError('Invalid argument for <overwrite>.\nAccepted types: '+str(bool)+'\nGot type: '+str(type(overwrite)))
    if fileexists(tofilename) and (not overwrite):
        raise FileExistsError()
    shutil.move(fromfilename,tofilename)
    logging.info('Moved file: '+str(fromfilename))
    logging.info('Moved to: '+str(tofilename))
    return True

def read_all_bytes(filename):
    if not isinstance(filename,str):
        raise ValueError('Invalid argument for <filename>.\nAccepted types: '+str(str)+'\nGot type: '+str(type(filename)))
    if not fileexists(filename):
        raise FileNotFoundError()
    return _readfile(filename,'rb')

def read_all_text(filename,encoding=r'utf-8'):
    if not isinstance(filename,str):
        raise ValueError('Invalid argument for <filename>.\nAccepted types: '+str(str)+'\nGot type: '+str(type(filename)))
    if not isinstance(encoding,str):
        raise ValueError('Invalid argument for <encoding>.\nAccepted types: '+str(str)+'\nGot type: '+str(type(encoding)))
    if not fileexists(filename):
        raise FileNotFoundError()
    return _readfile(filename,'rt',encoding)

def write_all_bytes(bytesdata,filename,overwrite=True):
    if not isinstance(bytesdata,bytes):
        raise ValueError('Invalid argument for <bytesdata>.\nAccepted types: '+str(bytes)+'\nGot type: '+str(type(bytesdata)))
    if not isinstance(filename,str):
        raise ValueError('Invalid argument for <filename>.\nAccepted types: '+str(str)+'\nGot type: '+str(type(filename)))
    if not isinstance(overwrite,bool):
        raise ValueError('Invalid argument for <overwrite>.\nAccepted types: '+str(bool)+'\nGot type: '+str(type(overwrite)))
    if fileexists(filename) and not overwrite:
        raise FileExistsError()
    return _writefile(bytesdata,filename,'wb')

def write_all_text(text,filename,encoding=r'utf-8',overwrite=True):
    if not isinstance(text,str):
        raise ValueError('Invalid argument for <text>.\nAccepted types: '+str(str)+'\nGot type: '+str(type(text)))
    if not isinstance(filename,str):
        raise ValueError('Invalid argument for <filename>.\nAccepted types: '+str(str)+'\nGot type: '+str(type(filename)))
    if not isinstance(encoding,str):
        raise ValueError('Invalid argument for <encoding>.\nAccepted types: '+str(str)+'\nGot type: '+str(type(encoding)))
    if not isinstance(overwrite,bool):
        raise ValueError('Invalid argument for <overwrite>.\nAccepted types: '+str(bool)+'\nGot type: '+str(type(overwrite)))
    if fileexists(filename) and not overwrite:
        raise FileExistsError()
    return _writefile(text,filename,'wt',encoding)

def _incrementfilename(filename):
    '''Private function to generate incremented filename if the input <filename> already exists.\n
       Otherwise, returns the <filename> unaltered.'''
    if not fileexists(filename):
        return filename
    else:
        i = 1
        ext = getextension(filename)
        filename = filename.replace(ext,'('+str(i)+')'+ext)
        while fileexists(filename):
            i += 1
            filename = filename.replace(ext,'('+str(i)+')'+ext)
    return filename

def _readfile(filename,options,encoding=None):
    '''Private function for reading a file in full.'''
    if encoding:
        with open(filename,options,encoding=encoding) as fopen:
            data = fopen.read()
    else:
        with open(filename,options) as fopen:
            data = fopen.read()
    return data

def _writefile(data,filename,options,encoding=None):
    '''Private function for wrapping io.open'''
    if encoding:
        with open(filename,options,encoding=encoding) as fopen:
            fopen.write(data)
    else:
        with open(filename,options) as fopen:
            fopen.write(data)
    return True
