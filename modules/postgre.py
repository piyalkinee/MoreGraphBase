from database.core import database_postgre
from .dbgenerator import create_graph_string


async def create_graph():
    await create_schema_for_algoritm()
    await create_function()
    await create_schema_for_data()
    await create_table_for_data()
    await create_data()


async def test_graph(start: int, end: int):
    await test(start, end)


async def create_schema_for_algoritm():
    query = """
    CREATE SCHEMA IF NOT EXISTS pggraph;
    """
    await database_postgre.execute(query)


async def create_function():
    query = """
    CREATE OR REPLACE FUNCTION pggraph.dijkstra (
    v_graph_sql TEXT
    , i_source BIGINT
    , i_target BIGINT
    )
    RETURNS TABLE (
      id BIGINT
    , vertex BIGINT
    , previous_vertex BIGINT
    , cost DOUBLE PRECISION
    ) AS $$
    DECLARE
      r_vertex RECORD;
      d_infinity DOUBLE PRECISION := 9999999999;
      i_current_vertex BIGINT;
      i_neighbour_vertex BIGINT;
      i_current_vertex_cost DOUBLE PRECISION;
    BEGIN
      CREATE TEMP TABLE IF NOT EXISTS dijkstra_graph (
        id BIGINT
      , source BIGINT
      , target BIGINT
      , cost DOUBLE PRECISION
      ) ON COMMIT DROP;
    
      CREATE TEMP TABLE IF NOT EXISTS dijkstra_result (
        id BIGINT
      , vertex BIGINT
      , previous_vertex BIGINT
      , cost DOUBLE PRECISION
      , is_visited BOOLEAN
      ) ON COMMIT DROP;
    
      DELETE FROM dijkstra_graph;
      DELETE FROM dijkstra_result;
    
      EXECUTE 'INSERT INTO dijkstra_graph (id, source, target, cost) ' || v_graph_sql;
    
      INSERT INTO dijkstra_result (id, vertex, previous_vertex, cost, is_visited)
      SELECT NULL::BIGINT, dg.source, NULL::BIGINT, d_infinity, FALSE FROM dijkstra_graph dg
      UNION
      SELECT NULL::BIGINT, dg.target, NULL::BIGINT, d_infinity, FALSE FROM dijkstra_graph dg;
    
      UPDATE dijkstra_result dr SET cost = 0 WHERE dr.vertex = i_source;
    
      LOOP
    	i_current_vertex := NULL;
    
      	SELECT dr.vertex, dr.cost
      	INTO i_current_vertex, i_current_vertex_cost
      	FROM dijkstra_result dr
      	WHERE dr.is_visited = FALSE AND dr.cost < d_infinity
      	ORDER BY cost ASC
      	LIMIT 1;
    
      	EXIT WHEN i_current_vertex IS NULL OR (i_target IS NOT NULL AND i_current_vertex = i_target);
    
      	UPDATE dijkstra_result dr SET is_visited = TRUE WHERE dr.vertex = i_current_vertex;
    
    	UPDATE dijkstra_result dr
    	SET id = dg.id
    	  , previous_vertex = i_current_vertex
    	  , cost = i_current_vertex_cost + dg.cost
    	FROM dijkstra_graph dg
    	WHERE dr.vertex = dg.target
    	  AND dr.is_visited = FALSE
    	  AND dg.source = i_current_vertex
    	  AND (i_current_vertex_cost + dg.cost) < dr.cost;
    
      END LOOP;
    
      IF i_target IS NULL THEN
      	RETURN QUERY SELECT dr.id, dr.vertex, dr.previous_vertex, dr.cost FROM dijkstra_result dr;
      ELSE
      	RETURN QUERY WITH RECURSIVE backtrack_dijkstra_result(id, vertex, previous_vertex, cost) AS (
      		SELECT dr.id, dr.vertex, dr.previous_vertex, dr.cost
      		FROM dijkstra_result dr
      		WHERE dr.vertex = i_target
      		
      		UNION ALL
      		
      		SELECT dr.id, dr.vertex, dr.previous_vertex, dr.cost
      		FROM dijkstra_result dr, backtrack_dijkstra_result bdr
      		WHERE dr.vertex = bdr.previous_vertex
      	) SELECT bdr.id, bdr.vertex, bdr.previous_vertex, bdr.cost
      	FROM backtrack_dijkstra_result bdr;
      END IF;
    END
    $$ LANGUAGE plpgsql
      SECURITY DEFINER
      SET search_path = pggraph, pg_temp;
    """
    await database_postgre.execute(query)


async def create_schema_for_data():
    query = """
    CREATE SCHEMA IF NOT EXISTS pggraph_dijkstra_test;
    """
    await database_postgre.execute(query)


async def create_table_for_data():
    query = """
    CREATE TABLE IF NOT EXISTS pggraph_dijkstra_test.graph (
      id BIGINT
    , source BIGINT
    , target BIGINT
    , cost DOUBLE PRECISION
    );
    """
    await database_postgre.execute(query)


async def create_data():
    values: str = create_graph_string(500)

    query = f"""
    INSERT INTO pggraph_dijkstra_test.graph (id, source, target, cost) VALUES
    {values};
    """
    await database_postgre.execute(query)


async def test(start: int, end: int):
    query = f"""
    SELECT * FROM pggraph.dijkstra('SELECT id, source, target, cost FROM pggraph_dijkstra_test.graph', {start} , {end});
    """

    for x in await database_postgre.fetch_all(query):
        print(list(x.items()))
