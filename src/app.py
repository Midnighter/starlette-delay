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

from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route


logging.getLogger("asyncio").setLevel(logging.DEBUG)
logger = logging.getLogger(__name__)


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
        logger.info(f"Measured delay: %.3G s", delay)


async def start() -> None:
    asyncio.get_running_loop().create_task(measure_delay())


app = Starlette(debug=True, routes=[Route("/json", endpoint)], on_startup=[start])
