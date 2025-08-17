import asyncpg
import os

pg_user=os.environ["POSTGRES_USER"]
pg_password = os.environ["POSTGRES_PASSWORD"]
pg_database = os.environ["POSTGRES_DATABASE"]


async def update_user(username: str, user_id: str, score: int) -> None:
    conn = await asyncpg.connect(host=pg_database, port=5432, user=pg_user, database=pg_database, password=pg_password)
    table = await conn.fetch("SELECT * FROM scores WHERE user_name = $1; ", username)
    if len(table) == 0:
        await conn.execute("INSERT INTO scores (user_name, user_id, score) VALUES ($1, $2, $3)  ;", username, user_id, score)
    else:
        await conn.execute("UPDATE scores SET score=score+($1) WHERE user_id = $2", score, user_id)
    await conn.close()

async def get_scores() -> list[tuple]:
    conn = await asyncpg.connect(host = pg_database, port=5432, user=pg_user, database=pg_database, password=pg_password)
    table = await conn.fetch("SELECT * FROM scores ORDER BY score DESC")
    await conn.close()
    return table


