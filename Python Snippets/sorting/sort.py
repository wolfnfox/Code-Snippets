import logging

from sorting import common

def insertion(sortlist,direction='asc'):
    logging.debug(str(sortlist))
    for i in range(len(sortlist)-1,0,-1):
        trycompare = True
        while(trycompare):
            trycompare = False
            for j in range(0,i):
                if not common._compareto(sortlist[j],sortlist[i],direction):
                    num = sortlist.pop(i)
                    sortlist.insert(j,num)
                    trycompare = True
                    logging.debug('Insert index['+str(i)+'] = '+str(num)+' into index['+str(j)+']')
                    logging.debug(str(sortlist))
                    break
    return sortlist