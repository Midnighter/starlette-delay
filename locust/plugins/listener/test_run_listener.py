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


import atexit

import locust.env

from ..helpers import timezone_aware_now
from ..writer import AbstractTestRunWriter


class TestRunListener:
    def __init__(
        self,
        *,
        environment: locust.env.Environment,
        writer: AbstractTestRunWriter,
        **kwargs
    ) -> None:
        """"""
        super().__init__(**kwargs)
        self._writer = writer
        self._is_complete = False
        environment.events.test_start.add_listener(self.test_start)
        environment.events.test_stop.add_listener(self.test_stop)
        environment.events.quitting.add_listener(self.quitting)
        atexit.register(self.exit)

    def test_start(self, **_kwargs):
        self._writer.start(timestamp=timezone_aware_now())

    def _end(self):
        self._writer.stop(timestamp=timezone_aware_now())
        self._is_complete = True

    def test_stop(self, **_kwargs):
        self._end()

    def quitting(self, **_kwargs):
        if not self._is_complete:
            self._end()

    def exit(self):
        if not self._is_complete:
            self._end()
