from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ThreadingMixIn
import threading
import argparse
import re
import cgi
import json
from math_lib import math_dict




class LocalData(object):
    records = {}


class HTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if None != re.search('/api/run', self.path):
            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            if ctype == 'application/json':
                length = int(self.headers.getheader('content-length'))
                content_len = int(self.headers.getheader('content-length', 0))
                post_body = self.rfile.read(content_len)
                print post_body
                j_data = json.loads(post_body)
                print j_data

                method = j_data["method"]
                print method

                method = math_dict[method]
                print method

                data  = j_data["data"]
                print data

                resp = method(data)
                print resp

                #resp = math_dict[j_data["method"]](j_data["data"])

                print resp
                self.send_response(200)
                # self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(resp)

                #recordID = self.path.split('/')[-1]
                #LocalData.records[recordID] = j_data
                #print "record %s is added successfully" % recordID
            else:
                data = {}
            self.send_response(200)
            self.end_headers()
        else:
            self.send_response(403)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
        return

    def do_GET(self):
        self.send_response(403)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        return


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    allow_reuse_address = True

    def shutdown(self):
        self.socket.close()
        HTTPServer.shutdown(self)


class SimpleHttpServer():
    def __init__(self, ip, port):
        self.server = ThreadedHTTPServer((ip, port), HTTPRequestHandler)

    def start(self):
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()

    def waitForThread(self):
        self.server_thread.join()

    def addRecord(self, recordID, jsonEncodedRecord):
        LocalData.records[recordID] = jsonEncodedRecord

    def stop(self):
        self.server.shutdown()
        self.waitForThread()


if __name__ == '__main__':
    # parser = argparse.ArgumentParser(description='HTTP Server')
    # parser.add_argument('port', type=int, help='Listening port for HTTP Server')
    # parser.add_argument('ip', help='HTTP Server IP')
    # args = parser.parse_args()

    server = SimpleHttpServer("127.0.0.1", 8008)
    print 'HTTP Server Running...........'
    server.start()
    server.waitForThread()