import xmlrpclib

s = xmlrpclib.ServerProxy('http://localhost:8000')
print s.selectByID(6)
print s.selectAll()