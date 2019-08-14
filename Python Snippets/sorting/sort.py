import logging

def bubble(sortlist,order='asc'):
    for i in range(0,len(sortlist)):
        tryagain = False
        for j in range(0,len(sortlist)-i-1):
            if _compareto(sortlist[j+1],sortlist[j],order):
                sortlist[j], sortlist[j+1] = sortlist[j+1], sortlist[j]
                tryagain = True
        if not tryagain:
            break
    return sortlist

def insertion(sortlist,order='asc'):
    for i in range(1,len(sortlist)):
        for j in range(0,i):
            if _compareto(sortlist[i],sortlist[j],order):
                num = sortlist.pop(i)
                sortlist.insert(j,num)
                break
    return sortlist

def merge(sortlist,order='asc'):
    if len(sortlist) > 1:
        splitindex = len(sortlist)//2
        arr1 = merge(sortlist[:splitindex],order)
        arr2 = merge(sortlist[splitindex:],order)
        sortlist = _mergelists(arr1,arr2,sortlist,order)
    else:
        pass
    return sortlist

def quick(sortlist,order='asc'):

    return sortlist

def selection(sortlist,order='asc'):
    for i in range(0,len(sortlist)-1):
        minj = i
        for j in range(i+1,len(sortlist)):
            if _compareto(sortlist[j],sortlist[minj],order):
                minj = j
        num = sortlist.pop(minj)
        sortlist.insert(i,num)
    return sortlist

def _compareto(num,compareto,order='asc'):
    result = False
    if (num < compareto) and order == 'asc':
        result = True
    elif (num > compareto) and order == 'dsc':
        result = True 
    return result

def _mergelists(arr1,arr2,sortlist,order):
    i = j = 0
    for k in range(0,len(sortlist)):
        if (i < len(arr1)) and (j < len(arr2)):
            if _compareto(arr2[j],arr1[i],order):
                sortlist[k] = arr2[j]
                j += 1
            else:
                sortlist[k] = arr1[i]
                i += 1
        elif ( i == len(arr1)):
            sortlist[k] = arr2[j]
            j += 1
        else:
            sortlist[k] = arr1[i]
            i += 1
    return sortlist