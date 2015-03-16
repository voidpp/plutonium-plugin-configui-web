import os
import sys
import threading

from plutonium.plugins.plugin import ConfigUserInterfacePluginBase

from http_server import AdvancedHTTPServer
from http_handler import RawHTTPHandler, VirtualHandler

import sqlchemyforms

from crud import CRUD
import models

Feed = getattr(sys.modules['plutonium.models.feed'], 'Feed')
Output = getattr(sys.modules['plutonium.models.output'], 'Output')
Filter = getattr(sys.modules['plutonium.models.filter'], 'Filter')

from plutonium.modules.logger import get_logger
logger = get_logger(__name__, 'plutonium')

class WebConfiguiPlugin(ConfigUserInterfacePluginBase):

    def __init__(self, host, port, plutonium):
        self.host = host
        self.port = port
        self.httpd = None
        self.plutonium = plutonium
        self.cwd = os.path.realpath(os.path.dirname(__file__))

        plutonium.register_after_successfully_init(self.after_plutonium_init)

        RawHTTPHandler.document_root = os.path.join(self.cwd, 'wwwroot')
        RawHTTPHandler.file_not_found_handler = VirtualHandler()

    # a little race here: the WebConfigUserInterfacePlugin.start func is called before this init, so if someone send a request to us,
    # so while this callback was not called a 404 response will returns
    def after_plutonium_init(self):

        RawHTTPHandler.file_not_found_handler.register('\/feeds.*', CRUD(Feed, self.plutonium.orm_manager))
        RawHTTPHandler.file_not_found_handler.register('\/outputs.*', CRUD(Output, self.plutonium.orm_manager))
        RawHTTPHandler.file_not_found_handler.register('\/filters.*', CRUD(Filter, self.plutonium.orm_manager))

    def listen(self):
        address = (self.host, self.port)
        logger.info('Web UI server listen on %s:%d' % address)

        if self.httpd:
            self.httpd.shutdown()

        self.httpd = AdvancedHTTPServer(address, RawHTTPHandler, 10)

        th = threading.Thread(target=self.httpd.serve_forever)
        th.setDaemon(True)
        th.start()

    def start(self):
        self.listen()

    def stop(self):
        logger.info('Web UI server is stopping...')
        if self.httpd:
            self.httpd.shutdown()

    def reload(self, host, port):
        self.stop()
        self.host = host
        self.port = port
        self.listen()
