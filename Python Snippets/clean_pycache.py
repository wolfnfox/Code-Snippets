import logging, sys

from helpers import directory
from helpers import file

logging.basicConfig(level=logging.INFO,format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p',\
                    handlers=[logging.StreamHandler(sys.stdout)])

cachefiles = directory.getfiles('./','.pyc')
for filename in cachefiles:
    file.delete(filename)