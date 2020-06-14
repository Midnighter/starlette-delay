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


from datetime import datetime

from .abstract_test_run_writer import AbstractTestRunWriter
from .orm import Session, TestRun


class TestRunORMWriter(AbstractTestRunWriter):
    def __init__(
        self,
        *,
        session: Session,
        test_plan: str,
        profile: str = "",
        description: str = "",
        **kwargs
    ) -> None:
        """"""
        super().__init__(
            test_plan=test_plan, profile=profile, description=description, **kwargs
        )
        self._session = session
        self._run = self._create_run(session, test_plan, profile, description)

    @staticmethod
    def _create_run(
        session: Session, test_plan: str, profile: str = "", description: str = "",
    ) -> TestRun:
        run = TestRun(test_plan=test_plan, profile=profile, description=description)
        session.add(run)
        session.commit()
        return run

    @property
    def run_id(self) -> int:
        return self._run.id

    def start(self, timestamp: datetime) -> None:
        self._run.started_on = timestamp
        self._session.commit()

    def stop(self, timestamp: datetime) -> None:
        self._run.completed_on = timestamp
        self._session.commit()
