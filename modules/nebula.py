from nebula2.gclient.net import ConnectionPool
from nebula2.Config import Config

config = Config()
config.max_connection_pool_size = 10

connection_pool = ConnectionPool()

def connect_nebula():
    connection_pool.init([('192.168.0.105', 9669)], config)

def disconnect_nebula():
    connection_pool.close()

def session_nebula():
    return connection_pool.get_session('root', 'nebula')

#TEST

def nebula_test_graph(start: int, end: int):
    return test(start, end)


def test(start: int, end: int):
    session = connection_pool.get_session('root', 'nebula')

    session.execute('USE nba')

    resolt = session.execute('SHOW TAGS')

    session.release()

    return resolt
