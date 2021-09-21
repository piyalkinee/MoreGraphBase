from asyncio.runners import run
from database.core import connect_postgre, disconnect_postgre
from modules.postgre import create_graph, test_graph


async def main():
    await postgre_test()


async def postgre_test():
    await connect_postgre()

    await test_graph(1, 256)
    await test_graph(6, 80)
    await test_graph(75, 1)
    await test_graph(257, 48)

    await disconnect_postgre()


run(main())
