import redis


redis_host = 'localhost'
redis_port = 6379
redis_password = '123456'

r = redis.Redis(host=redis_host, port=redis_port, password=redis_password)

def set(key,value):
 # 设置键值对
 r.set(key, value)

# 获取键对应的值
def get(key):
 value = r.get(key)
 print(value)

if __name__ == '__main__':
    # set("123","456")
    get('123')
