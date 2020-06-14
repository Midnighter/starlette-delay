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
from datetime import datetime

from .abstract_test_run_writer import AbstractTestRunWriter


logger = logging.getLogger(__name__)


class TestRunLogWriter(AbstractTestRunWriter):
    def __init__(
        self,
        *,
        run_id: int,
        test_plan: str,
        profile: str = "",
        description: str = "",
        **kwargs
    ) -> None:
        """"""
        super().__init__(
            test_plan=test_plan, profile=profile, description=description, **kwargs
        )
        self._run_id = run_id
        logger.info(
            "Creating test run:\nid=%d\ntest_plan=%s\nprofile=%s\ndescription=%s",
            run_id,
            test_plan,
            profile,
            description,
        )

    @property
    def run_id(self) -> int:
        return self._run_id

    def start(self, timestamp: datetime) -> None:
        logger.info("Test run started on %s", timestamp.isoformat())

    def stop(self, timestamp: datetime) -> None:
        logger.info("Test run stopped on %s", timestamp.isoformat())
