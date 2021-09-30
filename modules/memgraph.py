from .dbgenerator import format_graph, get_edges
import mgclient

database_memgraph = mgclient.connect(host='192.168.0.105', port=7687)

def connect_memgraph():
    return database_memgraph.cursor()

def disconnect_memgraph():
    database_memgraph.close()

async def memgraph_create_graph():
    formated_graph: dict = format_graph(await get_edges())

    query: str = "CREATE "

    for vertex in formated_graph:
        #query += f'(ver_{vertex}:Location' + '{name:"' + str(vertex) + '"}),'
        query += f"(ver_{vertex}:Location),"

    #for vertex_key in formated_graph:
    #    for vertex_value in formated_graph[vertex_key]:
    #        query += f"(ver_{vertex_key})-[:ROAD " + \
    #            "{cost:0}" + f"]->(ver_{vertex_value}),"

    #query = query[:-1]

    #query += ";"

    session = connect_memgraph()

    session.execute("CREATE (n) RETURN 'Node ' + id(n)")

    print(session.fetchall())


def memgraph_test_graph(start: int, end: int):
    return test(start, end)


def test(start: int, end: int):
    query: str = "MATCH (n) RETURN id(n)"

    session = connect_memgraph()

    session.execute(query)
    rows = session.fetchall()
    print(rows)
    print("--------")
    data = session.fetchone()

    return data


# DELETE
def memgraph_remove_graph():
    remove_graph()


def remove_graph():
    session = connect_memgraph()

    query = "MATCH (n) DETACH DELETE n"

    session.execute("MATCH (n) DETACH DELETE n")
