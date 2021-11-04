import threading
import redis
import rediscluster
import time

def create_redis_client(host: str, port: int):
    return rediscluster.RedisCluster(
        host=host,
        port=port,
        decode_responses=True,
        ssl=True,
        skip_full_coverage_check=True)

def time_measurement(action: str):
    def wrapper(func):
        def decorated(*args, **kwargs):
            start_time = time.time() # 작업 시작 시간
            func(*args, **kwargs)
            end_time = time.time() # 작업 종료 시간
            print({ # 작업 정보 출력
                "thread_name": threading.current_thread().getName(),
                "range": f"{kwargs['range_start']} ~ {kwargs['range_end']}",
                "action": action,
                "execution_time": end_time - start_time,
                "start_time": time.strftime('%Y-%m-%d %H:%M:%S.%s', time.localtime(start_time)),
                "end_time": time.strftime('%Y-%m-%d %H:%M:%S.%s', time.localtime(end_time))
            })
        return decorated
    return wrapper

@time_measurement(action="write")
def write(redis_client, range_start: int, range_end: int):
    for i in range(range_start, range_end):
        key = str(i).zfill(6)
        value = "empty"
        redis_client.set(key, value)

@time_measurement(action="get")
def get(redis_client, range_start: int, range_end: int):
    for i in range(range_start, range_end):
        key = str(i).zfill(6)
        redis_client.get(key)

@time_measurement(action="delete")
def delete(redis_client, range_start: int, range_end: int):
    for i in range(range_start, range_end):
        key = str(i).zfill(6)
        redis_client.delete(key)

@time_measurement(action="transact")
def transact(redis_client, range_start: int, range_end: int):
    value = "empty"
    for i in range(range_start, range_end):
        key = str(i).zfill(6)
        pipe = redis_client.pipeline()
        pipe.set(key, value)
        pipe.get(key)
        pipe.delete(key)
        pipe.execute()