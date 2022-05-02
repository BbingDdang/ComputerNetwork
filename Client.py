# echo_client.py
#-*- coding:utf-8 -*-

from socket import *


IP = "127.0.0.1"
PORT = 9999
SIZE = 1024

def request_formating(method, body, url):
    return f"{method}/HTTP/1.1\r\nHost: {url}\r\nContent-Type: text/html\r\nConnection: keep-alive\r\nContent-Length: {len(body)}\r\n\n{body}"


with socket(AF_INET, SOCK_STREAM) as client_socket:
    client_socket.connect((IP, PORT))
    while True:
        mub = input()
        mub = mub.split()
        method = mub[0]
        if method == 'GET':
            url = mub[1]
            body = ''

        elif method == 'POST':
            url = mub[1]
            if len(mub) == 5:
                body = f"{mub[2]} : {{'level' : {mub[3]}, ATK : {mub[4]}}}"
            else:
                body = ''
        elif method == 'PUT':

            url = mub[1]
            if len(mub) == 5:
                body = f"{mub[2]} : {{'level' : {mub[3]}, ATK : {mub[4]}}}"
            else:
                body = ''
        elif method == 'HEAD':
            url = mub[1]
            body = ''

        else:
            False
        request = request_formating(method, body, url)
        client_socket.send(request.encode('utf-8'))
        response = client_socket.recv(SIZE).decode('utf-8')
        print(response)
        print('---------------------client---------------------\n')

        #client_socket.close()