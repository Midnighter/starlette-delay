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


from sqlalchemy import Column, DateTime, Integer, String, Text

from ...helpers import timezone_aware_now
from . import Base


class TestRun(Base):

    __tablename__ = "test_run"

    id = Column(Integer, primary_key=True)
    test_plan = Column(String(32), default="", nullable=False)
    profile = Column(String(32))
    description = Column(Text)
    created_on = Column(
        DateTime(timezone=True), nullable=False, default=timezone_aware_now
    )
    started_on = Column(DateTime(timezone=True))
    completed_on = Column(DateTime(timezone=True))
