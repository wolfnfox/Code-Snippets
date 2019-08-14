import logging
import numpy

def binary(searchlist,item,order='asc',lb=None,ub=None):
    '''Search a sorted list'''
    if (lb is None) or (ub is None):
        lb, ub = 0, len(searchlist)-1
    if (ub > lb):
        mid = (ub-lb)//2
        if searchlist[mid] == item:
            return mid
        if ((searchlist[mid] > item) and order =='asc') or\
           ((searchlist[mid] < item) and order == 'dsc'):
            return binary(searchlist,item,order,lb,mid-1)
        else:
            return binary(searchlist,item,order,mid+1,ub)
    return -1

def linear(searchlist,item,find='first'):
    '''Search a sorted or unsorted list'''
    if find == 'all':
        result = []
        for i in range(len(searchlist)):
            if searchlist[i] == item:
                result.append(i)
        return result
    if find == 'first':
        for i in range(len(searchlist)):
            if searchlist[i] == item:
                return i
    if find == 'last':
        for i in range(len(searchlist)-1,-1,-1):
            if searchlist[i] == item:
                return i
    return -1

def jump(searchlist,item):
    '''Search a sorted list (ascending)'''
    step = int(numpy.floor(len(searchlist)**(0.5)))
    k = 0
    for i in range(0,len(searchlist),step):
        if searchlist[i] > item:
            k = i
        else:
            break
    for i in range(k,max(k+step,len(searchlist))):
        if searchlist[i] == item:
            return i
    return -1