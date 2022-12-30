import sqlite3
import json
import aiosqlite
import asyncio
import aiohttp
import aiofiles
import pandas as pd
from aiohttp import web

conn = sqlite3.connect('dbase.db')
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM mini_projekt_db")
counter_check = cursor.fetchone()[0]

if counter_check == 0:
    print("Database is empty.")
else:
    print("Database is NOT empty.")

routes = web.RouteTableDef()

@routes.get("/JSON_Data")
async def json_data(request):
    try:
        async with open('file-000000000040.json', 'r') as file_data:
            read_data = { await file_data.readline() for _ in range(10)}
            whole_data = [json.loads(line) for line in read_data]
            database = []
            async with aiosqlite.connect("dbase.db") as db:
                for item in whole_data:
                    db_item = {}
                    db_item["username"] = item["repo_name"].rsplit("/", 1)[0]
                    db_item["ghublink"] = "https://github.com/" + item["repo_name"] + ".com"
                    db_item["filename"] = item["path"].rsplit("/", 1)[1]
                    database.append(db_item)
                    await db.execute(
                        "INSERT INTO mini_projekt_db (username, ghublink, filename) VALUES (?,?,?)",
                        (
                            db_item["username"], db_item["ghlink"], db_item["filename"]))
                    await db.commit()
                async with db.execute("SELECT * FROM mini_projekt_db") as cur:
                    result = len(await cur.fetchall())
            message = {"status": "ok", "data": {"numberOfRowsInTable": result}}
            return web.json_response(message, status=200)

    except Exception as e:
        return web.json_response({"Error": str(e)}, status=500)

app = web.Application()
app.router.add_routes(routes)
web.run_app(app, port=8081)