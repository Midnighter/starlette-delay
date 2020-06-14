# Copyright (C) 2020  Moritz E. Beber
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


""""""


import asyncio
import logging
import time
from datetime import datetime, timedelta, timezone

from databases import Database, DatabaseURL
from starlette.applications import Starlette
from starlette.config import Config
from starlette.responses import JSONResponse
from starlette.routing import Route


# logging.getLogger("asyncio").setLevel(logging.DEBUG)
logger = logging.getLogger(__name__)
config = Config(".env")
DATABASE_URL = config("POSTGRES_URL", cast=DatabaseURL)
database = Database(DATABASE_URL)


async def endpoint(_) -> JSONResponse:
    # Provide an opportunity for context switching.
    await asyncio.sleep(0.001)
    # Simulate 10 ms of processing time.
    time.sleep(0.01)
    # Provide an opportunity for context switching.
    await asyncio.sleep(0.001)
    return JSONResponse({"message": "Hello, World!"})


async def measure_delay() -> None:
    """"""
    while True:
        start = time.perf_counter()
        await asyncio.sleep(1)
        delay = time.perf_counter() - start - 1
        app.state.records.append(
            {
                "timestamp": datetime.now(timezone.utc),
                "delay": delay,
                "run_id": app.state.run_id,
            }
        )
        logger.info(f"Measured delay: %.3G s", delay)


async def query_run_id(database: Database, max_tries: int = 20) -> int:
    starting_from = datetime.now(timezone.utc) - timedelta(seconds=5)
    for _ in range(max_tries):
        try:
            result = await database.fetch_one(
                """SELECT id, created_on FROM test_run
                WHERE completed_on IS NULL AND created_on > :start
                ORDER BY created_on DESC NULLS LAST
                LIMIT 1""",
                {"start": starting_from},
            )
            return result["id"]
        except Exception:
            logger.error("Could not find the test run id yet. Retrying.")
            await asyncio.sleep(0.5)
            continue
    raise RuntimeError("Could not find the test run id!")


async def start() -> None:
    await database.connect()
    app.state.run_id = await query_run_id(database)
    logger.info("Identified run id %d.", app.state.run_id)
    app.state.records = []
    app.state.delay = asyncio.get_running_loop().create_task(measure_delay())


async def end() -> None:
    app.state.delay.cancel()
    await database.execute_many(
        """INSERT INTO delay(run_id, timestamp, delay)
        VALUES (:run_id, :timestamp, :delay)""",
        app.state.records,
    )
    await database.disconnect()


# app = Starlette(debug=True, routes=[Route("/json", endpoint)], on_startup=[start])
app = Starlette(
    routes=[Route("/json", endpoint)], on_startup=[start], on_shutdown=[end]
)
