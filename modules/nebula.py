import time
from .dbgenerator import format_graph, get_edges
from nebula2.gclient.net import ConnectionPool
from nebula2.Config import Config

DB_NAME = 'morebasedb'

config = Config()
config.max_connection_pool_size = 10

connection_pool = ConnectionPool()


def connect_nebula():
    connection_pool.init([('192.168.0.105', 9669)], config)


def disconnect_nebula():
    connection_pool.close()


def session_nebula():
    return connection_pool.get_session('root', 'nebula')

# INIT


async def nebula_init_graph():
    create_space()
    time.sleep(20)
    create_metadata()


def create_space():
    session = session_nebula()

    query = f"""
    CREATE SPACE {DB_NAME} (vid_type = INT64);
    """

    session.execute(query)


def create_metadata():
    session = session_nebula()

    query = f"""
    USE {DB_NAME};
    CREATE TAG location(name string);
    CREATE EDGE road (cost double);
    CREATE TAG INDEX location_index on location();
    CREATE EDGE INDEX road_index on road();
    """

    session.execute(query)


# CREATE


async def nebula_create_graph():
    await create_data()
    # create_mini()


def create_mini():
    session = session_nebula()
    session.execute(f"USE {DB_NAME};")
    session.execute('INSERT VERTEX location(name) VALUE 1:("NANANA");')


async def create_data():
    formated_graph: dict = format_graph(await get_edges())

    session = session_nebula()

    session.execute(f"USE {DB_NAME};")

    for vertex_key in formated_graph:
        session.execute(
            f'INSERT VERTEX location(name) VALUE {int(vertex_key)}:("{vertex_key}");')

    for vertex_key in formated_graph:
        for vertex_value in formated_graph[vertex_key]:
            session.execute( f'INSERT EDGE road(cost) VALUES {vertex_key}->{vertex_value}:(1.0);')

    session.execute('REBUILD TAG INDEX location_index;')
    session.execute('REBUILD EDGE INDEX road_index;')

# TEST


def nebula_test_graph(start: int, end: int):
    return test(start, end)


def test(start: int, end: int):
    session = session_nebula()

    session.execute(f'USE {DB_NAME};')

    resolt = session.execute(
        f'FIND SHORTEST PATH FROM {int(start)} TO {int(end)} OVER *;')

    return resolt

# REMOVE


def nebula_remove_graph():
    session = session_nebula()

    session.execute(f'USE {DB_NAME}')

    #session.execute(f"DROP SPACE {DB_NAME};")

    values = session.execute('MATCH (v:location) RETURN v;')

    for a in values._data_set_wrapper.column_values("v"):
        session.execute(f'DELETE VERTEX {str(a).split(":")[0].replace("(","")}')


# INFO

def nebula_info_graph():
    session = session_nebula()

    session.execute(f'USE {DB_NAME}')

    print(session.execute('SHOW SPACES;'))
    print(session.execute('SHOW TAGS;'))
    print(session.execute('SHOW EDGES;'))
    print(session.execute('SHOW TAG INDEXES;'))
    print(session.execute('SHOW EDGE INDEXES;'))

    print(session.execute('MATCH (v:location) RETURN v;'))
    print(session.execute('MATCH ()-[e:road]-() RETURN e;'))