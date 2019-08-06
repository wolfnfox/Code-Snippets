import copy, random, time

from sorting import sort

num = random.sample(range(1000),1000)

print('*** Bubble sort ***')
start_time = time.perf_counter()
sort.bubble(copy.copy(num),'asc')
print('Elapsed time: '+str(time.perf_counter()-start_time)+'(s)\n')

print('*** Insertion sort ***')
start_time = time.perf_counter()
sort.insertion(copy.copy(num),'asc')
print('Elapsed time: '+str(time.perf_counter()-start_time)+'(s)\n')

print('*** Selection sort ***')
start_time = time.perf_counter()
sort.selection(copy.copy(num),'asc')
print('Elapsed time: '+str(time.perf_counter()-start_time)+'(s)\n')

print('*** Merge sort ***')
start_time = time.perf_counter()
sort.merge(copy.copy(num),'asc')
print('Elapsed time: '+str(time.perf_counter()-start_time)+'(s)\n')