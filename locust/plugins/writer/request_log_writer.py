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


logger = logging.getLogger(__name__)


class RequestLogWriter(AbstractRequestWriter):
    def __init__(self, *, run_id: int, **kwargs) -> None:
        """"""
        super().__init__(run_id=run_id, **kwargs)

    def request(
        self,
        timestamp: datetime,
        method: str,
        url: str,
        is_successful: bool,
        response_time: float,
        response_length: Optional[int] = None,
    ) -> None:
        logger.info(
            "Request: %s %s %s %s in %.3G microseconds run=%d pid=%d greenlet=%d",
            timestamp.isoformat(),
            method,
            url,
            "Succeeded" if is_successful else "Failed",
            response_time,
            self._run_id,
            self._pid,
            self._greenlet_id,
        )
