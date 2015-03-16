import sys
import json

from http_handler import VirtualRequestHandlerBase, HTTPResponse

from sqlchemyforms.exceptions import CrudException
from sqlchemyforms.crud_base import CrudBase, CrudRequest
from sqlchemyforms.tools import JSONEncoder

class CRUD(CrudBase, VirtualRequestHandlerBase):
    def __init__(self, model, db_mgr):
        CrudBase.__init__(self, model)
        self.db_mgr = db_mgr

    def handle(self, request):
        path_parts = request.path.split('/')
        command = 'list'
        if len(path_parts) > 2 and len(path_parts[2]) > 0:
            command = path_parts[2]

        command = 'do_%s' % command

        if not hasattr(self, command):
            return HTTPResponse('Undefined CRUD controller', 404)

        func = getattr(self, command)

        try:
            session = self.db_mgr.create_session()
            creq = CrudRequest(request.path, request.get_vars, request.post_vars, session)
            response = HTTPResponse(json.dumps(func(creq), cls = JSONEncoder), 200)
            session.commit()
        except CrudException as e:
            response = HTTPResponse(e.message, e.code)

        session.close()
        return response
