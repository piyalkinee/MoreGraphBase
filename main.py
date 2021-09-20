import asyncio

from asyncio.runners import run
from database.core import connect_postgre, disconnect_postgre, database_postgre


async def main():
    await postgre_test()


async def postgre_test():
    await connect_postgre()

    query = """
    CREATE TABLE IF NOT EXISTS "Users" (
    "Id" integer NOT NULL,
    "Name" character(32),
    PRIMARY KEY ("Id")
    );
    """

    await database_postgre.execute(query)

    await disconnect_postgre()


run(main())
