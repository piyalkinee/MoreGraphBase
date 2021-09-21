import random
#from database.core import database_postgre, DB_NAME


def create_graph_for_postgre(vertex_count: int):
    dots_to_connect: list = [1]
    dots_map: dict = {}

    last_id: int = 1

    while dots_to_connect != []:

        dots_to_connect_current: int = dots_to_connect.pop(0)

        if dots_to_connect_current >= vertex_count:
            break

        dots_map[dots_to_connect_current] = []

        for i in range(random.randint(1, 5)):
            last_id += 1
            dots_map[dots_to_connect_current].append(last_id)
            dots_to_connect.append(last_id)

    return dots_map


def create_graph_string(vertex_count: int):
    graph: dict = create_graph_for_postgre(vertex_count)

    string: str = ""

    id: int = 1

    for v1 in graph:
        for v2 in graph[v1]:
            string += f"({id},{v1},{v2},1),"
            id += 1

    string = string[:-1]

    return string

create_graph_string(500)