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


import locust.env

from ..helpers import timezone_aware_now
from .abstract_user_count_writer import AbstractUserCountWriter
from .orm import Session, UserCount


class UserCountORMWriter(AbstractUserCountWriter):
    def __init__(
        self,
        *,
        session: Session,
        run_id: int,
        environment: locust.env.Environment,
        **kwargs
    ) -> None:
        """"""
        super().__init__(environment=environment, **kwargs)
        self._session = session
        self._run_id = run_id

    def _write_count(self, count: int):
        self._session.add(
            UserCount(timestamp=timezone_aware_now(), run_id=self._run_id, count=count,)
        )
        self._session.commit()
