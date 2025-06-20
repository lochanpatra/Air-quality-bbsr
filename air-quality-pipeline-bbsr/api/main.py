
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import asyncpg
import asyncio

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_URL = "postgresql://ts_user:ts_pass@localhost:5433/tsdb"

@app.on_event("startup")
async def startup():
    app.state.db_pool = await asyncpg.create_pool(DATABASE_URL)

@app.on_event("shutdown")
async def shutdown():
    await app.state.db_pool.close()

@app.get("/api/aq/latest")
async def get_latest_aq():
    async with app.state.db_pool.acquire() as connection:
        rows = await connection.fetch(
            """
            SELECT station_id, pm25, ST_X(geom) AS lon, ST_Y(geom) AS lat, timestamp
            FROM aq_stations
            WHERE timestamp >= NOW() - INTERVAL '10 minutes'
            """
        )
        result = [
            {
                "station_id": r['station_id'],
                "pm25": r['pm25'],
                "lon": r['lon'],
                "lat": r['lat'],
                "timestamp": r['timestamp'].isoformat()
            }
            for r in rows
        ]
    return result
