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


import atexit
import logging
import os

from sqlalchemy import create_engine

from locust import constant_pacing, events, task
from locust.contrib.fasthttp import FastHttpUser
from plugins.helpers import is_manager
from plugins.listener import RequestListener, TestRunListener
from plugins.query import query_run_id
from plugins.writer import RequestORMWriter, TestRunORMWriter, UserCountORMWriter
from plugins.writer.orm import Session


logger = logging.getLogger(__name__)
engine = create_engine(
    f"postgresql+psycopg2://postgres:{os.getenv('POSTGRES_PASSWORD')}@db:5432/postgres"
)
Session.configure(bind=engine)
session = Session()


class APIClient(FastHttpUser):

    wait_time = constant_pacing(3)

    @task
    def index_page(self):
        response = self.client.get("/json")
        assert response.status_code == 200
        assert response.json()["message"] == "Hello, World!"


@events.init.add_listener
def on_locust_init(environment, **_kwargs):
    if is_manager():
        TestRunListener(
            environment=environment,
            writer=TestRunORMWriter(
                session=session,
                test_plan="delay_benchmark",
                description="Testing async delay",
            ),
        )
    run_id = query_run_id(session)
    logger.info("Identified run id %d.", run_id)
    RequestListener(
        environment=environment,
        writer=RequestORMWriter(session=session, run_id=run_id),
    )
    if is_manager():
        UserCountORMWriter(environment=environment, session=session, run_id=run_id)


def shutdown():
    session.close()


atexit.register(shutdown)
