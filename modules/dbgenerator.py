from modules.postgre import database_postgre

DB_NAME = "morebasedb"


def format_graph(edges):
    formated_graph: dict = {1: []}
    for e in edges:
        if int(e["target"]) not in formated_graph:
            formated_graph[int(e["target"])] = []
        formated_graph[int(e["source"])].append(int(e["target"]))

    return formated_graph


async def get_edges():
    query = f"SELECT * FROM {DB_NAME}.graph LIMIT 10000"
    return [dict(d) for d in await database_postgre.fetch_all(query)]
