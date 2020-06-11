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


""""""


from locust import constant_pacing, task
from locust.contrib.fasthttp import FastHttpUser


class APIClient(FastHttpUser):

    wait_time = constant_pacing(2)

    @task
    def index_page(self):
        response = self.client.get("/json")
        assert response.status_code == 200
        assert response.json()["message"] == "Hello, World!"
