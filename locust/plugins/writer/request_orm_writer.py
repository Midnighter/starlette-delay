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
from typing import Optional

from .abstract_request_writer import AbstractRequestWriter
from .orm import Request, Session


logger = logging.getLogger(__name__)


class RequestORMWriter(AbstractRequestWriter):
    def __init__(self, *, session: Session, run_id: int, **kwargs) -> None:
        """"""
        super().__init__(run_id=run_id, **kwargs)
        self._session = session

    def request(
        self,
        timestamp: datetime,
        method: str,
        url: str,
        is_successful: bool,
        response_time: float,
        response_length: Optional[int] = None,
    ) -> None:
        self._session.add(
            Request(
                timestamp=timestamp,
                run_id=self._run_id,
                greenlet_id=self._greenlet_id,
                pid=self._pid,
                method=method,
                url=url,
                is_successful=is_successful,
                response_time=response_time,
                response_length=response_length,
            )
        )
        self._session.commit()
