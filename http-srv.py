from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ThreadingMixIn
import threading
import argparse
import re
import cgi
import json
import xmlrpclib

class LocalData(object):
    records = {}


class HTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        self.send_response(403)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        return

    def do_GET(self):
        if None != re.search('/api/v1/getrecord/*', self.path):
            recordID = self.path.split('/')[-1]
            s = xmlrpclib.ServerProxy('http://localhost:8000')
            retutn_list = s.selectByID(recordID)
            if retutn_list:

                req = {
                    'method': "sum_all",
                    'data': retutn_list
                }

                import requests
                resp = requests.post("http://127.0.0.1:8008/api/run", json=req)
                print resp.status_code
                print resp.text

                self.send_response(200)
                #self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(resp.text)
            else:
                self.send_response(400, 'Bad Request: record does not exist')
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(
                    '{ "errors": [{"status": "400","detail": "record does not exist" }]}')

        else:
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

    server = SimpleHttpServer("127.0.0.1", 8009)
    print 'HTTP Server Running...........'
    server.start()
    server.waitForThread()