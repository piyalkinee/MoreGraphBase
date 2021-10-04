from asyncio.runners import run
from modules.arango import arango_create_graph, arango_remove_graph, arango_test_graph
from modules.nebula import connect_nebula, disconnect_nebula, nebula_info_graph, nebula_init_graph, nebula_create_graph, nebula_remove_graph, nebula_test_graph
from modules.postgre import connect_postgre, disconnect_postgre, postgre_create_graph, postgre_test_graph, postgre_remove_graph
from modules.neo4j import disconnect_neo4j, neo4j_create_graph, neo4j_test_graph, neo4j_remove_graph
from modules.memgraph import disconnect_memgraph, memgraph_create_graph, memgraph_test_graph, memgraph_remove_graph
import time


async def main():
    await connect_postgre()
    connect_nebula()

    command = input()

    if command == "init":
        await nebula_init_graph()
    if command == "create":
        # await postgre_create_graph()
        # await neo4j_create_graph()
        await memgraph_create_graph()
        # await nebula_create_graph()
        # await arango_create_graph()
    elif command == "test":
        print(await postgre_test_graph(1, 256))
        print(neo4j_test_graph(1, 256))
        #print(memgraph_test_graph(1, 256))
        print(nebula_test_graph(1, 256))
        print(arango_test_graph(1, 256))
    elif command == "remove":
        # await postgre_remove_graph()
        # neo4j_remove_graph()
        memgraph_remove_graph()
        # nebula_remove_graph()
        # arango_remove_graph()
    elif command == "info":
        nebula_info_graph()
    elif command == "start":
        await full_test()
    else:
        print("Incorrect command")

    await disconnect_postgre()
    disconnect_neo4j()
    disconnect_memgraph()
    disconnect_nebula()


async def full_test():

    iter_size = [1000, 3000, 6000]

    resolts_test = {}
    resolts_test_time = {}

    for iter in iter_size:
        resolt_in_iter = []
        resolt_time_in_iter = []

        print("[-POSGRE_"+str(iter)+"-]")
        await postgre_remove_graph()
        await postgre_create_graph(iter)

        time_postgre = time.time()
        resolt_in_iter.append({"postgre_" + str(iter): await postgre_test_graph(1, iter - 100)})
        resolt_time_in_iter.append({"postgre_time_":time.time() - time_postgre})

        print("[-NEO4J_"+str(iter)+"-]")
        neo4j_remove_graph()
        await neo4j_create_graph()

        time_neo4j = time.time()
        resolt_in_iter.append({"neo4j_" + str(iter): neo4j_test_graph(1, iter - 100)})
        resolt_time_in_iter.append({"neo4j_time_":time.time() - time_neo4j})

        print("[-NEBULA_"+str(iter)+"-]")
        nebula_remove_graph()
        await nebula_create_graph()

        time_nebula = time.time()
        resolt_in_iter.append({"nebula_" + str(iter): nebula_test_graph(1, iter - 100)})
        resolt_time_in_iter.append({"nebula_time_":time.time() - time_nebula})

        print("[-ARANGO_"+str(iter)+"-]")
        arango_remove_graph()
        await arango_create_graph()

        time_arango = time.time()
        resolt_in_iter.append({"arango_" + str(iter): arango_test_graph(1, iter - 100)})
        resolt_time_in_iter.append({"arango_time_":time.time() - time_arango})

        print(resolt_in_iter)
        print(resolt_time_in_iter)

        resolts_test[iter] = resolt_in_iter
        resolts_test_time[iter] = resolt_time_in_iter

    print(resolts_test)
    print(resolts_test_time)

run(main())
