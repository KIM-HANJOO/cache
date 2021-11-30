import pandas as pd
import random
import time
'''
cache는 가장 맨 뒤의 값을 가장 최근의 값으로 한다.
뒤에 추가하나 앞에 추가하나 리스트가 한 칸씩 밀리는 것은 같으나,
cache가 가득 차지 않은 초기에는 뒤에 추가하는 것이 더 이득이 있기 때문.

앞이나 뒤에 추가하는 것의 속도차이는 미미하므로 무시한다.
'''


def status_log(f, m, t, runtime, rt_add) :
	status = ' '
	
	front_length = 10
	middle_length = 9
	tail_length = 50
	runtime_length = 4
	
	pointer = '->' + ' ' * 3
	
	fs = front_length - len(f)
	ms = middle_length - len(m)
	ts = tail_length - len(t)
	rs = runtime_length - len(str(runtime))
	
	status += f + ' ' * fs + pointer
	status += m + ' ' * ms + pointer
	status += t + ' ' * ts + '|'
	status += '  runtime = {}'.format(str(runtime))\
		+ ' ' * rs + '(+{})'.format(str(rt_add))
	
	return status


def cache_analysis(size, names) :
	
	
	df = pd.DataFrame(columns = ['added', 'status', 'runtime', \
								'runtime_added'])
	df_num = 0
	
	# names(리스트) 의 맨 앞부터 차례대로 읽으면서 cache에 저장
	runtime = 0
	in_cache = 1
	not_in_UC = 5
	not_in_FC = 7
	
	
	cache = []
	check = 0
	'''
	check = 0 : default
	check = 1 : in cache
	check = 2 : not in cache, cache not full
	check = 3 : not in cache, cache full
	'''

	for num, N in enumerate(names) :
		start_time = time.perf_counter()
		
		if num == 0 :
			print('\n\n##################< STATUS LOG >##################')
		
		rt_org = runtime
		# lower string으로 cache에 포함 여부를 확인
		n = N.lower()
		cache_temp = cache.copy()
		for i in range(len(cache_temp)) :
			cache_temp[i] = cache_temp[i].lower()
		
		# n, cache_temp로 확인해서 N을 cache에 업데이트
		
		if n in cache_temp :
			index_num = cache_temp.index(n)
			cache.pop(index_num)
			cache.append(N)
			
			runtime += in_cache
			check = 1
			
		else :
			if len(cache) < size : # 아직 cache가 차지 않음
				cache.append(N) # cache의 뒤에 추가
				
				runtime += not_in_UC
				check = 2
				
			else : # cache가 가득 참
				cache = cache[1 :] + [N]
				
				runtime += not_in_FC
				check = 3
				
				
		end_time = time.perf_counter()
		print("elapsed : {}ms^7".format(int(round((end_time - start_time) * pow(10, 10)))))
		print("cache size = {}".format(size), cache)
		# status log		
		f = 'add : {}'.format(str(N))
		m = ''
		if check == 1 :
			m = '{}, NF'.format(chr(8712))
		elif check == 2 :
			m = '{}/, NF'.format(chr(8712))
		elif check == 3 :
			m = '{}/, F'.format(chr(8712))	
		t = str(cache)
	
		status = status_log(f, m, t, runtime, runtime - rt_org)
		
		
		# df add line
		
		df.loc[df_num, 'added'] = str(N)
		df.loc[df_num, 'status'] = m
		df.loc[df_num, 'runtime'] = runtime
		df.loc[df_num, 'runtime_added'] = runtime - rt_org
		df_num += 1
		
		print(status)
		
	return df, runtime
	


def choice(n) :
	fond_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'A', 'B', 'C', 'D', 'E']
	choice_n = [random.choice(fond_list) for i in range(n)]
	
	return choice_n

choice_5 = choice(8)

all_runtime = []
for i in range(2, 10) :
	df, runtime = cache_analysis(i, choice_5)
	all_runtime.append(runtime)
	
print('\n', all_runtime)
