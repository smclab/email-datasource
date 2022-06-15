"""
Copyright (c) 2020-present SMC Treviso s.r.l. All rights reserved.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import threading
from fastapi import FastAPI
from pydantic import BaseModel
from imap.imap_extraction import AsyncEmailExtraction

app = FastAPI()


class ImapRequest(BaseModel):
    mailServer: str
    port: str
    username: str
    password: str
    timestamp: int
    datasourceId: int
    folder: str


@app.post("/execute")
def get_data(request: ImapRequest):

    class AsyncTask(threading.Thread):

        def __init__(self, mail_server_, port_, username_, password_, timestamp_, datasource_id_, folder_):
            super(AsyncTask, self).__init__()
            self.email_extraction_task = AsyncEmailExtraction(mail_server_, port_, username_, password_, timestamp_,
                                                              datasource_id_, folder_)

        def run(self):
            self.email_extraction_task.extract()

    request = request.dict()

    mail_server = request['mailServer']
    port = request['port']
    username = request["username"]
    password = request["password"]
    datasource_id = request["datasourceId"]
    timestamp = request["timestamp"]
    folder = request["folder"]

    async_task = AsyncTask(mail_server, port, username, password, timestamp, datasource_id, folder)
    async_task.start()

    return "extraction started"
