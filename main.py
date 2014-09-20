from web_server.web_server_sockets import web_server

class Index(object):
    @classmethod
    def get(self):
        return web_server.serve_page("index", {"name": "Timur", "phone": "123-4567"})

    @classmethod
    def post(self, fields):
        return web_server.serve_page("index", fields)
        
class Hello(object):
    @classmethod
    def get(self):
        return web_server.serve_page("hello")

    @classmethod
    def post(self, fields):
        return web_server.serve_page("hello", fields)


web_server.router = {
    "/": Index,
    "/hello": Hello
}

if __name__ == "__main__":
    web_server.start_server()
