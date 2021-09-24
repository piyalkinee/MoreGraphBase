from asyncio.runners import run
from database.core import connect_postgre, disconnect_postgre
from database.core import disconnect_neo4j
from database.core import disconnect_memgraph
from modules.postgre import postgre_create_graph, postgre_test_graph, postgre_remove_graph
from modules.neo4j import neo4j_create_graph, neo4j_test_graph, neo4j_remove_graph


async def main():
    await connect_postgre()

    command = input()

    if command == "create":
        await postgre_create_graph()
        await neo4j_create_graph()
    elif command == "test":
        print(await postgre_test_graph(1, 256))
        print(neo4j_test_graph(1, 256))
        # memgraph_test()
    elif command == "remove":
        await postgre_remove_graph()
        neo4j_remove_graph()
    else:
        print("Incorrect command")

    await disconnect_postgre()
    disconnect_neo4j()
    disconnect_memgraph()

run(main())
