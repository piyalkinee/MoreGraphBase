from .dbgenerator import format_graph, get_edges
from neo4j import GraphDatabase

DB_NAME = "morebasedb"

NEO4J_DATABASE_URL = "bolt://localhost:11005"

neo4j_driver = GraphDatabase.driver(NEO4J_DATABASE_URL, auth=("neo4j", "1231"))


def connect_neo4j():
    return neo4j_driver.session(database=DB_NAME)


def disconnect_neo4j():
    neo4j_driver.close()


# CREATE


async def neo4j_create_graph():
    formated_graph: dict = format_graph(await get_edges())

    query: str = "CREATE "

    for vertex in formated_graph:
        query += f'(ver_{vertex}:Location' + '{name:"' + str(vertex) + '"}),'

    for vertex_key in formated_graph:
        for vertex_value in formated_graph[vertex_key]:
            query += f"(ver_{vertex_key})-[:ROAD " + \
                "{cost:0}" + f"]->(ver_{vertex_value}),"

    query = query[:-1]

    query += ";"

    session = connect_neo4j()

    session.run(query)

    create_myGraph()


def create_myGraph():
    query = """
            CALL gds.graph.create('myGraph', 'Location', 'ROAD', {relationshipProperties: 'cost'})
            """
    session = connect_neo4j()

    session.run(query)

# TEST


def neo4j_test_graph(start: int, end: int):
    return test(start, end)


def test(start: int, end: int):
    query = """
    MATCH (source:Location {name: '"""+str(start)+"""'}), (target:Location {name: '"""+str(end)+"""'})
    CALL gds.shortestPath.dijkstra.stream('myGraph', {
    sourceNode: source,
    targetNode: target,
    relationshipWeightProperty: 'cost'
    })
    YIELD index, sourceNode, targetNode, totalCost, nodeIds, costs, path
    RETURN
    index,
    gds.util.asNode(sourceNode).name AS sourceNodeName,
    gds.util.asNode(targetNode).name AS targetNodeName,
    totalCost,
    [nodeId IN nodeIds | gds.util.asNode(nodeId).name] AS nodeNames,
    costs,
    nodes(path) as path
    ORDER BY index
    """

    session = connect_neo4j()

    data = session.run(query)
    
    return data.single()[4] #[dict(d) for d in data[0]]

# REMOVE


def neo4j_remove_graph():
    remove_myGraph()
    remove_graph()


def remove_myGraph():
    session = connect_neo4j()

    query = f"CALL gds.graph.drop('myGraph') YIELD graphName;"
    session.run(query)


def remove_graph():
    session = connect_neo4j()

    query = f"MATCH (n:Location) DETACH DELETE n"

    session.run(query)
