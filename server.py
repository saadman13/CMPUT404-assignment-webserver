#  coding: utf-8 
import socketserver

# Copyright 2023 Saadman Islam Khan
# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

import os
class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        request_data = self.data.split()
        HTTP_VERB = request_data[0].decode("utf-8")
        path = "./www" + request_data[1].decode("utf-8")

        if "../" in path:
            response = "HTTP/1.1 404 Not Found\r\n" + "Content-Type: text/html" + "\r\n\r\n <h1>404 Not Found</h1>"

        elif HTTP_VERB != "GET":
            response = "HTTP/1.1 405 Method Not Allowed\r\n" + "Content-Type: text/html" + "\r\n\r\n <h1>405 Method Not Allowed</h1>"
            
        else:
            contentType = ""
            response = ""
            
            if os.path.isfile(path):
                fileName = request_data[1].decode("utf-8")
                extension = ""

                if '.' in fileName:
                    extension = fileName.split(".")

                file_content = open(path).read()

                if extension == "html":
                    contentType = "text/html"
                    response = "HTTP/1.1 200 OK\r\n" + "Content-Type: " + contentType + "\r\nContent_Length: " + str(len(file_content)) + "\r\n\r\n" + file_content

                elif extension == "css":
                    contentType = "text/css"
                    response = "HTTP/1.1 200 OK\r\n" + "Content-Type: " + contentType + "\r\nContent_Length: " + str(len(file_content)) + "\r\n\r\n" + file_content
            
                #other or no extensions
                else:
                    contentType = "text/plain"
                    response = "HTTP/1.1 200 OK\r\n" + "Content-Type: " + contentType + "\r\nContent_Length: " + str(len(file_content)) + "\r\n\r\n" + file_content

            elif os.path.isdir(path):
                
                if os.path.isfile(path + "index.html"):
                    file_content = open(path + "index.html").read()
                    contentType = "text/html"                
                    response = "HTTP/1.1 200 OK\r\n" + "Content-Type: " + contentType + "\r\nContent_Length: " + str(len(file_content)) + "\r\n\r\n" + file_content
            
                elif path[-1] != "/":
                    location = request_data[1].decode("utf-8") + "/"
                    response = "HTTP/1.1 301 Moved Permanently\r\n" + "Location: " + location + "\r\nContent_Length: 0" + "\r\n\r\n"
                else:
                    response = "HTTP/1.1 404 Not Found\r\n" + "Content-Type: text/html" + "\r\n\r\n<h1>404 Not Found</h1>"

            #Page not found
            else:
                response = "HTTP/1.1 404 Not Found\r\n" + "Content-Type: text/html" + "\r\n\r\n<h1>404 Not Found</h1>"
                
        
        print ("Got a request of: %s\n" % self.data)
        self.request.sendall(bytearray(response,'utf-8'))

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
