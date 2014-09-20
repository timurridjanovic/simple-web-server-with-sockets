
# Simple python web server using sockets: 

**Description**:  
It's a simple python web server using sockets. It serves static css and javascript files and has custom templating.

Just execute "python main.py" and see the result on localhost:8080

* To add another route in order to serve another html page, you need to edit main.py and:
    
    1)  add the route in the router
        `web_server.router = { "/hello-world": HelloWorld }`
    
    2)  In the router, the key is the path and the value is the name of a class. You need to    
        create this class like so:
        
        `class HelloWorld(object):
            @classmethod
            def get(self):
                return web_server.serve_page("hello_world")

            @classmethod
            def post(self, fields):
                return web_server.serve_page("hello_world", fields)`
    
        The HelloWorld class has 2 class methods (get and post). It uses the serve_page
        method to serve the html page in the views directory.
    
    3)  Create hello_world.html in the views directory and you're good to go!
