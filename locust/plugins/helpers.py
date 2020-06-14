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
import sys
from datetime import datetime, timezone


logger = logging.getLogger(__name__)


def timezone_aware_now():
    """Return a timezone-aware datetime instance in this moment in UTC."""
    return datetime.now(timezone.utc)


def is_worker():
    return "--worker" in sys.argv


def is_manager():
    return "--master" in sys.argv
