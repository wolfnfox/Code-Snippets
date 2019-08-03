def _compareto(num,compareto,direction='asc'):
    result = False
    if (num <= compareto) and direction == 'asc':
        result = True
    elif (num >= compareto) and direction == 'dsc':
        result = True 
    return result