### About

Redis Cluster의 Read/Write 성능을 측정하기 위한 스크립트입니다.

솔루션 간의 성능 차이를 대략적으로 표현하기에 적합하지만, 자세한 성능을 측정하기에는 부적합합니다.

스크립트는 아래의 각 작업을 수행하고, 소요되는 시간을 측정합니다.
- SET : 100000 개의 key-value 데이터를 생성합니다.
    - Key: 1 ~ 100000
    - Value: "Empty"
- GET : 100000 개의 key 값을 각각 한번 씩 읽습니다.
    - Key: 1 ~ 100000
- DEL : 100000 개의 key-value 데이터를 삭제합니다.
    - Key: 1 ~ 100000

### 실행 방법

`redis_performance_test.py` 파일 수정
```python 
# MemoryDB 또는 ElastiCache의 Cluster Endpoint 로 변경합니다.
if __name__ == "__main__":
    redis_client = redis_function.create_redis_client(
        host="clustercfg.dev-rdsworkshop-memorydb-redis-cluster.mdgzac.memorydb.us-east-1.amazonaws.com",
        port=6379)
```

필요한 라이브러리 설치
```bash
pip3 install -r requirements.txt
```

스크립트 실행
```bash
python3 redis_performance_test.py
```

### 예상 출력

```json
{
    "thread_name": "Thread-1", // 작업을 실행한 쓰레드의 이름
    "range": "1 ~ 10001", // Key 범위
    "action": "write",  // write: SET, get: GET, delete: DEL
    "execution_time": 11.171400308609009, // 작업 실행에 걸린 시간
    "start_time": "2021-11-04 02:12:03.1635991923", // 작업 시작 시간
    "end_time": "2021-11-04 02:12:14.1635991934" // 작업 종료 시간
}
...
```

샘플 출력은 sample_results 디렉터리를 확인합니다.
