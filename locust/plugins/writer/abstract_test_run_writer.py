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


class AbstractTestRunWriter(ABC):
    def __init__(
        self, test_plan: str, profile: str = "", description: str = "", **kwargs
    ) -> None:
        """"""
        super().__init__(**kwargs)

    def start(self, timestamp: datetime) -> None:
        raise NotImplementedError()

    def stop(self, timestamp: datetime) -> None:
        raise NotImplementedError()
