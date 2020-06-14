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


from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String

from . import Base


class Request(Base):

    __tablename__ = "request"

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime(timezone=True), nullable=False, primary_key=True)
    run_id = Column(Integer, ForeignKey("test_run.id"), nullable=False)
    greenlet_id = Column(Integer, nullable=False)
    pid = Column(Integer, nullable=False)
    method = Column(String(7), nullable=False)
    url = Column(String, nullable=False)
    is_successful = Column(Boolean, nullable=False)
    response_time = Column(Float, nullable=False)
    response_length = Column(Integer)
