from asyncio.runners import run
from modules.arango import arango_create_graph, arango_remove_graph, arango_test_graph, connect_arango
from modules.nebula import connect_nebula, disconnect_nebula, nebula_test_graph
from modules.postgre import connect_postgre, disconnect_postgre, postgre_create_graph, postgre_test_graph, postgre_remove_graph
from modules.neo4j import disconnect_neo4j, neo4j_create_graph, neo4j_test_graph, neo4j_remove_graph
from modules.memgraph import disconnect_memgraph, memgraph_create_graph, memgraph_test_graph, memgraph_remove_graph


async def main():
    await connect_postgre()
    connect_nebula()

    command = input()

    if command == "create":
        await postgre_create_graph()
        await neo4j_create_graph()
        #await memgraph_create_graph()
        await arango_create_graph()
    elif command == "test":
        print(await postgre_test_graph(1, 256))
        print(neo4j_test_graph(1, 256))
        #print(memgraph_test_graph(1,256))
        #print(nebula_test_graph(1, 256))
        print(arango_test_graph(1, 256))
    elif command == "remove":
        await postgre_remove_graph()
        neo4j_remove_graph()
        #memgraph_remove_graph()
        arango_remove_graph()
    else:
        print("Incorrect command")

    await disconnect_postgre()
    disconnect_neo4j()
    disconnect_memgraph()
    disconnect_nebula()

run(main())
