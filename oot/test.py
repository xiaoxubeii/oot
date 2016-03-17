__author__ = 'tardis'
import xmlrpclib

server = xmlrpclib.Server("http://localhost/cobbler_api")
server.login('cobbler', 'cobbler')
print(server.get_distros())
