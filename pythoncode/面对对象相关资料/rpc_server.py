from tornado.web import RequestHandler, Application
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
import json
import rpc_impl


class DispatchHandler(RequestHandler):
    def post(self, *args, **kwargs):
        payload = json.loads(self.request.body.decode())
        cls = getattr(rpc_impl, payload['class'])
        method = getattr(cls(), payload['method'])
        ret = method(**payload.get("params", {}))
        self.write(json.dumps(ret))


app = Application([
    ('/', DispatchHandler)
], debug=True)


app.listen(8080, address='0.0.0.0')
server = HTTPServer(app)

if __name__ == '__main__':
    IOLoop.current().start()
