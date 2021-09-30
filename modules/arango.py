from .dbgenerator import format_graph, get_edges
from pyArango.connection import *
from pyArango.graph import Graph, EdgeDefinition
from pyArango.collection import *

DB_NAME = 'morebasedb'


def connect_arango():
    return Connection(arangoURL="http://192.168.0.105:8529",
                      username="dbuser", password="1231")

# MODELS


class Position(Collection):
    _fields = {
        "name": Field()
    }


class Path(Edges):
    _fields = {
        "lifetime": Field()
    }


class MyGraph(Graph):
    _edgeDefinitions = [EdgeDefinition("Path", fromCollections=[
                                       "Position"], toCollections=["Position"])]
    _orphanedCollections = []

# CREATE


async def arango_create_graph():
    formated_graph: dict = format_graph(await get_edges())

    session = connect_arango()

    if session.hasDatabase(DB_NAME) == False:
        session.createDatabase(DB_NAME)

    db = session[DB_NAME]

    collection_vertices = db.createCollection(
        className='Collection', name="Position")
    collection_edges = db.createCollection(className='Edges', name="Path")

    graph = db.createGraph("MyGraph")

    created_positions = {}

    for vertex_key in formated_graph:
        created_positions[str(vertex_key)] = graph.createVertex(
            'Position', {"_key": f"{vertex_key}", "name": f"{vertex_key}"})

    path_key = 1

    for vertex_key in formated_graph:
        for vertex_value in formated_graph[vertex_key]:
            graph.link('Path', created_positions[str(vertex_key)], created_positions[str(
                vertex_value)], {"_key": f"{path_key}", "lifetime": "eternal"})
            path_key += 1


# TEST


def arango_test_graph(start: int, end: int):
    return test(start, end)


def test(start: int, end: int):

    query_aql = f"FOR v, e IN OUTBOUND SHORTEST_PATH 'Position/{start}' TO 'Position/{end}' GRAPH 'MyGraph' RETURN [v._key, e._key]"
    
    session = connect_arango()

    db = session[DB_NAME]

    queryResult = db.AQLQuery(query_aql)

    return queryResult

# REMOVE


def arango_remove_graph():
    session = connect_arango()
    db = session[DB_NAME]

    db.dropAllCollections()
