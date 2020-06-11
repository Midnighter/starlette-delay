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

FROM python:3.8-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/src

COPY requirements/requirements.txt requirements/requirements.txt

RUN set -eux \
    && pip install -r /app/requirements/requirements.txt \
    && rm -rf /root/.cache/pip

COPY src src/

CMD ["uvicorn", "--host", "0.0.0.0", "--no-access-log", "app:app"]
