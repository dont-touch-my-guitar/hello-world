from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler
from lib import selectAll, insertData, selectByID


# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

# Create server
server = SimpleXMLRPCServer(("localhost", 8000),
                            requestHandler=RequestHandler)


server.register_function(selectAll)
server.register_function(insertData)
server.register_function(selectByID)
# Run the server's main loop
server.serve_forever()