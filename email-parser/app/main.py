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
from typing import Optional
from imap.imap_extraction import AsyncEmailExtraction

app = FastAPI()


class ImapRequest(BaseModel):
    mailServer: str
    port: str
    username: str
    password: str
    timestamp: int
    datasourceId: int
    scheduleId: str
    folder: str
    tenantId: str
    indexAcl: Optional[bool] = False
    getAttachments: Optional[bool] = False


@app.post("/execute")
def get_data(request: ImapRequest):

    request = request.dict()

    mail_server = request['mailServer']
    port = request['port']
    username = request["username"]
    password = request["password"]
    datasource_id = request["datasourceId"]
    timestamp = request["timestamp"]
    folder = request["folder"]
    schedule_id = request["scheduleId"]
    tenant_id = request["tenantId"]
    index_acl = request["indexAcl"]
    get_attachments = request["getAttachments"]

    email_extraction_task = AsyncEmailExtraction(mail_server, port, username, password, timestamp, datasource_id,
                                                 folder, schedule_id, tenant_id, index_acl, get_attachments)

    thread = threading.Thread(target=email_extraction_task.extract())
    thread.start()

    return "extraction started"
