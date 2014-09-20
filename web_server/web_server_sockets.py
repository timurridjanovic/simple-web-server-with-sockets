import os
import socket

class WebServer(object):
    def __init__(self):
        self.router = {}
        self.file_path = os.getcwd()

    def start_server(self):
        host = ''
        port = 8080
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((host, port))
        sock.listen(1)

        request_dict = {
            "request": None,
            "path": None
        }
        
        print "server listening in on localhost:" + str(port)

        while True:
            csock, caddr = sock.accept()
            req = csock.recv(1024)
            request = req.split("\n")
            request_first_line = request[0]
            fields = request[-1]
            request_dict["request"] = request_first_line.split(" ")[0]
            request_dict["path"] = request_first_line.split(" ")[1]
            if fields:
                fields_dict = {}
                for field in fields.split("&"):
                    (key, value) = field.split("=")
                    fields_dict[key] = value
                request_dict["fields"] = fields_dict 
            (body, response) = self.app(request_dict)
            response = "HTTP/1.0 200 OK \nContent-Type: " + response + "\n\n"
            csock.sendall(response + "\n".join(body))
            csock.close()

    def app(self, environ):
        if environ["request"] == "GET":
            return self.handle_get_request(environ)
        elif environ["request"] == "POST":
            return self.handle_post_request(environ)

    def handle_get_request(self, environ):
        path_vars = [e for e in environ["path"].split("/") if e]

        if environ["path"] in self.router:
            return (self.router[environ["path"]].get(), "text/html")

        elif path_vars[0] == "css" and len(path_vars) > 1:
            return (self.serve_css(environ["path"]), "text/css")

        elif path_vars[0] == "js" and len(path_vars) > 1:
            return (self.serve_javascript(environ["path"]), "application/javascript")

        else:
            return (["404 Error"], "text/html")

    def handle_post_request(self, environ):
        if environ["path"] in self.router:
            return (self.router[environ["path"]].post(environ["fields"]), "text/html")
        else:
            return (["404 Error"], "text/html")

    def serve_page(self, page, template_vars=None):
        with open(self.file_path + "/views/" + page + ".html", "r") as p:
            template = p.readlines()
            if template_vars == None:
                return template
            for e in template_vars.keys():
                template = [line.replace("{{" + e + "}}", template_vars[e]) for line in template]
            return template

    def serve_css(self, path):
        try:
            with open(self.file_path + "/" + path, "r") as p:
                return p.readlines()
        except IOError:
            return ["no such file"]

    def serve_javascript(self, path):
        try:
            with open(self.file_path + "/" + path, "r") as p:
                return p.readlines()
        except IOError:
            return ["no such file"]

web_server = WebServer()

