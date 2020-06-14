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


import logging
import time
from datetime import timedelta

from sqlalchemy import desc, nullslast
from sqlalchemy.exc import SQLAlchemyError

from .helpers import timezone_aware_now
from .writer.orm import Session, TestRun


logger = logging.getLogger(__name__)


def query_run_id(session: Session, max_tries: int = 20) -> int:
    starting_from = timezone_aware_now() - timedelta(seconds=5)
    for _ in range(max_tries):
        try:
            return (
                session.query(TestRun.id, TestRun.created_on)
                .filter(
                    TestRun.completed_on.is_(None), TestRun.created_on > starting_from
                )
                .order_by(nullslast(desc(TestRun.created_on)))
                .first()
                .id
            )
        except (AttributeError, SQLAlchemyError):
            logger.error("Could not find the test run id yet. Retrying.")
            time.sleep(0.5)
            continue
    raise RuntimeError("Could not find the test run id!")
