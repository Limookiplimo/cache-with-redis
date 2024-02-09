import redis
import psycopg2
import json

# Establish database connection - Done
# Read data from the database - Done
# Cache the data - Done

db_config = {
    'dbname': 'cache_db',
    'host': 'localhost',
    'port': 5432,
    'user': 'db_user',
    'password': 'user_password'
}

redis_config = {
    'host': 'localhost',
    'port': 6379,
    'db': 0,
    'decode_responses': True
}

def database_connection():
    with psycopg2.connect(**db_config) as conn:
        return conn

def get_db_data(table, conn):
    with conn.cursor() as cur:
        cur.execute(f'select * from {table}')
        data = cur.fetchall()
        return data

def cache_data(table, data, expiration_time):
    r = redis.StrictRedis(**redis_config)
    r.set(table, json.dumps(data),ex=expiration_time)
    
def get_cached_data(table_name):
    r = redis.StrictRedis(**redis_config)
    data = r.get(table_name)
    if data:
        return json.loads(data)
    else:
        return None

if __name__=='__main__':
    table_name = 'personnel'
    
    cached_data = get_cached_data(table_name)
    if cached_data:
        print("Data retrieved from cache:")
        print(cached_data)
    else:
        db_conn = database_connection()
        data = get_db_data(table_name, db_conn)
        print("Data retrieved from database:")
        print(data)
        
        cache_data(table_name,data,60)



