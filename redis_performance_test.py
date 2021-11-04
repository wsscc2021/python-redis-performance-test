import threading
import time
import sys
import redis_function

def multi_threading(function, redis_client):
    # 총 100000 개의 작업을 수행합니다.
    # 10개의 Thread도 나눠서 병렬 처리하며, 하나의 Thread는 10000개의 작업을 수행합니다.
    # Thread 1 : 1 ~ 10000
    # Thread 2 : 10001 ~ 20000
    # Thread 3 : 20001 ~ 30000 
    # ...
    # Thread 생성
    threads = list()
    for n in range(1, 11): # 1부터 10까지 반복
        range_start = ((n-1)*10000)+1
        range_end = (n*10000)+1
        threads.append(
            threading.Thread(
                target=function,
                kwargs={
                    'redis_client': redis_client,
                    'range_start': range_start,
                    'range_end': range_end
                }
            )
        )
    # Thread 시작
    for thread in threads:
        thread.start()
    # Thread 대기
    while threading.active_count() > 1:
        time.sleep(0.1)

if __name__ == "__main__":
    redis_client = redis_function.create_redis_client(
        host="clustercfg.dev-rdsworkshop-elasticache-redis.mdgzac.use1.cache.amazonaws.com",
        port=6379)
    print("================= write action ========================")
    multi_threading(redis_function.write, redis_client)
    print("================= get action ========================")
    multi_threading(redis_function.get, redis_client)
    print("================= delete action ========================")
    multi_threading(redis_function.delete, redis_client)
    print("================= transact action ========================")
    multi_threading(redis_function.transact, redis_client)