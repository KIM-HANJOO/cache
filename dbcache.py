import pandas as pd
import random
import time
import matplotlib.pyplot as plt

'''
cache는 가장 맨 뒤의 값을 가장 최근의 값으로 한다.
뒤에 추가하나 앞에 추가하나 리스트가 한 칸씩 밀리는 것은 같으나,
cache가 가득 차지 않은 초기에는 뒤에 추가하는 것이 더 이득이 있기 때문.

앞이나 뒤에 추가하는 것의 속도차이는 미미하므로 무시한다.
'''


def status_log(f, m, t, runtime, rt_add) : # cache 연산 결과 출력 함수
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


def cache_analysis(size, names) : # 캐시 사이즈, 검색어 인자로 캐시 동작시간 계산
	
	# names(리스트) 의 맨 앞부터 차례대로 읽으면서 cache에 저장
	runtime = 0
	in_cache = 1
	not_in_UC = 5
	not_in_FC = 7
	
	
	cache = [] # 빈 캐시 생성(캐시 크기는 뒤에서 if문으로 제한)
	check = 0 # 캐시에서 검색어 조회 시, 1, 2, 3 세 시나리오로 정해짐
	'''
	check = 0 : default
	check = 1 : in cache
	check = 2 : not in cache, cache not full
	check = 3 : not in cache, cache full
	'''
	calc_time = 0 # 총 연산시간
	
	for num, N in enumerate(names) : # 검색어(리스트) 앞에서 차례로 검색어 조회
		start_time = time.perf_counter() # 연산시간 측정 시작
		
		if num == 0 :
			print('\n\n##################< STATUS LOG >##################')
		
		rt_org = runtime
		
		# lower string으로 cache에 포함 여부를 확인
		n = N.lower() # 검색어(영문 가정)의 대문자, 소문자 무시하기 위해 비교는 소문자로 진행
		cache_temp = cache.copy() # 소문자 버젼의 임시 리스트
		for i in range(len(cache_temp)) :
			cache_temp[i] = cache_temp[i].lower() # 캐시의 항목을 소문자로 임시 리스트에 추가
		
		# n, cache_temp로 확인해서 N을 cache에 업데이트
		
		if n in cache_temp : # 소문자 검색어(n)을 임시 리스트에 검색
			index_num = cache_temp.index(n)
			cache.pop(index_num)
			cache.append(N)
			
			runtime += in_cache
			check = 1 # 시나리오 1
			
		else :
			if len(cache) < size : # 아직 cache가 차지 않음
				cache.append(N) # cache의 뒤에 추가
				
				runtime += not_in_UC
				check = 2 # 시나리오 2
				
			else : # cache가 가득 참
				cache = cache[1 :] + [N]
				
				runtime += not_in_FC
				check = 3 # 시나리오 3
				
				
		end_time = time.perf_counter() # 연산시간 측정 완료
		
		print("\nelapsed : {}(x10^7)ms".format(int(round((end_time - start_time) * pow(10, 10)))))
		print("cache size = {}".format(size), cache) # 연산시간 출력
		
		calc_time += end_time - start_time # 현재 연산 시간 총 연산시간에 합
		
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
	
		status = status_log(f, m, t, runtime, runtime - rt_org) # status log 문자열 생성
		
		print(status) # status log 출력
		
	return calc_time, runtime # 총 계산시간 반환
	


def choice(n) : # 'a'부터 'p'까지의 소 / 대문자 검색어(알파벳) 중 랜덤한 n개 고르는 함수
	fond_list = ['a', 'b', 'C', 'd', 'e', 'f', 'G', 'h', 'i', 'j', 'K', 'l', 'm', 'n', 'o', 'p']
	choice_n = [random.choice(fond_list) for i in range(n)]
	
	return choice_n # 사용할 검색어 목록

choice = choice(20) # 8개의 검색어 설정

x_values = [] 
all_runtime = []
calc_runtime = []

for i in range(2, 20) :
	x_values.append(i)
	calc_time, runtime = cache_analysis(i, choice)
	calc_runtime.append(calc_time)
	all_runtime.append(runtime)

# 해석 출력

# 최소 가정 연산 시간
min_min = 0
for i in range(len(all_runtime)) :
	if i > 0 :
		if all_runtime[i] < all_runtime[i - 1] :
			min_min = x_values[i]

# 최소 실제 연산 시간
min_calctime = []
for i in range(len(calc_runtime)) :
	if calc_runtime[i] == min(calc_runtime) :
		min_calctime.append(x_values[i])

log_end = '#' * 50

print('\n', log_end)
print('\n캐시 연산 시간(가정) : ', all_runtime)
print('검색어 : ', choice)			
print(f'{len(choice)}개의 검색어, 최소 시간 {min_min} 사이즈 캐시부터\n')
print(f'{min_min}보다 작은 사이즈에서는 캐시의 연산시간 차이가 있으나 이후로는 연산시간 차이 없음')
print(f'캐시 연산 시간은 중복되는 검색어의 개수와 검색어의 순서에 영향을 받는다')
if len(min_calctime) == 1 :
	print(f'실제 연산 시간은 {min_calctime[0]}에서 최소 ({round(calc_runtime[i],4)}(x10^7)ms)')
else :
	print(f'실제 연산 시간은 {min_calctime} 모두에서 최소)')
	
print(f'최적의 캐시 사이즈는 {min_min}개')
print('\n\n실제 캐시의 효율성은 연산 시간이 아닌 캐시의 용량, 검색어의 빈도에 따라 최적화 알고리즘을 구현해야 함')
print('캐시 연산시간의 최소 시간은 가정된 검색어 리스트에 대해서만 유효하므로, 일반적인 검색어 길이와 빈도에 따른 일반적인 연산 시간은 고려되지 않음(특수성)')



# 결과 출력 (그래프)
	
plt.plot(x_values, all_runtime, 'b--')
plt.xlabel('cache size')
plt.ylabel('runtime')
plt.title('cache runtime for cache size')
plt.xticks(x_values)
plt.grid()
plt.show()

	
