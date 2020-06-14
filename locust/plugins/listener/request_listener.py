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
from ..writer import AbstractRequestWriter


class RequestListener:
    def __init__(
        self,
        *,
        environment: locust.env.Environment,
        writer: AbstractRequestWriter,
        **kwargs
    ) -> None:
        """"""
        super().__init__(**kwargs)
        self._writer = writer
        environment.events.request_failure.add_listener(self.request_failure)
        environment.events.request_success.add_listener(self.request_success)

    def request_failure(
        self,
        request_type: str,
        name: str,
        response_time: float,
        response_length: int,
        **_kwargs
    ):
        self._writer.request(
            timestamp=timezone_aware_now(),
            method=request_type,
            url=name,
            is_successful=False,
            response_time=response_time,
            response_length=response_length,
        )

    def request_success(
        self,
        request_type: str,
        name: str,
        response_time: float,
        response_length: int,
        **_kwargs
    ):
        self._writer.request(
            timestamp=timezone_aware_now(),
            method=request_type,
            url=name,
            is_successful=True,
            response_time=response_time,
            response_length=response_length,
        )
