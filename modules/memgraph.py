from .dbgenerator import format_graph, get_edges
import mgclient

connection = mgclient.connect(host='192.168.0.105', port=7687)


def connect_memgraph():
    return connection.cursor()


def disconnect_memgraph():
    connection.close()


async def memgraph_create_graph():
    formated_graph: dict = format_graph(await get_edges())

    query: str = "CREATE "

    for vertex in formated_graph:
        #query += f'(ver_{vertex}:Location' + '{name:"' + str(vertex) + '"}),'
        query += f"(ver_{vertex}:Location),"

    # for vertex_key in formated_graph:
    #    for vertex_value in formated_graph[vertex_key]:
    #        query += f"(ver_{vertex_key})-[:ROAD " + \
    #            "{cost:0}" + f"]->(ver_{vertex_value}),"

    #query = query[:-1]

    #query += ";"

    session = connect_memgraph()

    print(session.execute("CREATE (n:bot) RETURN n;"))


def memgraph_test_graph(start: int, end: int):
    session = connect_memgraph()

    print(session.execute("MATCH (n:bot) RETURN n;"))
    rows = session.fetchall()
    print(rows)
    print("--------")
    data = session.fetchone()

    return data


# DELETE
def memgraph_remove_graph():
    session = connect_memgraph()

    session.execute("MATCH (n) DETACH DELETE n")
