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


from abc import ABC
from datetime import datetime
from os import getpid
from typing import Optional

import greenlet


def greenlet_identifier():
    """Return the greenlet's identifier or -1 if it doesn't exist."""
    if hasattr(glet := greenlet.getcurrent(), "minimal_ident"):
        return glet.minimal_ident
    return -1


class AbstractRequestWriter(ABC):
    def __init__(self, *, run_id: int, **kwargs) -> None:
        """"""
        super().__init__(**kwargs)
        self._run_id = run_id
        self._pid = getpid()
        self._greenlet_id = greenlet_identifier()

    def request(
        self,
        timestamp: datetime,
        method: str,
        url: str,
        is_successful: bool,
        response_time: float,
        response_length: Optional[int] = None,
    ) -> None:
        raise NotImplementedError()
