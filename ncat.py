#!/usr/bin/env python

import socket
import argparse

ap = argparse.ArgumentParser(description='This is ncat in python')
ap.add_argument('hostname', type=str, help='hostname or IP address', default=None)
ap.add_argument('port', type=int, help='port', default='80')
ap.add_argument('--content', help='content to send', default='GET / HTTP/1.1\nHost: %s\n\n" %hostname')
args = ap.parse_args()

def ncat(hostname, port, content):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((hostname, port))
    s.send(content)
    while 1:
        data = s.recv(1024)
        if data == "":
            break
        print "Received:", repr(data)
    print "Connection closed."
    s.close()

#hostname = "10.0.0.2"
#port = 8000
#content = "GET / HTTP/1.1\nHost: %s\n\n" %hostname
ncat(args.hostname, args.port, args.content)
