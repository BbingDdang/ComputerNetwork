
import socket
import time
import json


HOST = "127.0.0.1"
PORT = 9999
SIZE = 1024


def response_form(code, status, body = ''):
    date = time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.localtime(time.time()))
    return f"HTTP/1.1 {code} {status}\r\nDate: {date}\r\nContent-Length: {len(body)}\r\nConnection: Keep-Alive\r\nContent-Type: text/html\r\ncharset=UTF-8\r\n\n{body}"

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((HOST, PORT))

server_socket.listen()

client_socket, addr = server_socket.accept()

# with socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
#     server_socket.bind((HOST, PORT))  # 생성한 소켓에 HOST와 PORT 바인딩
#     server_socket.listen(1)  # 소켓 연결 대기 상태
exist_job = ['Scouter', 'Bard', 'Spearman', 'BattleMaster', 'Arcana', 'Destroyer']
while True:

    data = client_socket.recv(SIZE).decode('utf-8')  # client에서 보내는 데이터 받기
    with open('test.json', 'r', encoding='utf-8') as f:
        json_data = json.load(f)
    #method = int(input("1. GET, 2. POST, 3. PUT, 4. HEAD"))

    data1 = data.split('\n')
    method = data1[0].split('/')
    method = method[0]

    #GET
    if method == "GET":
        get_response = response_form('200', 'OK', str(json_data))
        res = get_response
        print(data)
        print("-----------server-------------")
        client_socket.send(res.encode('utf-8'))

    #POST
    elif method == "POST":
        tmp = data1[-1]
        tmp = tmp.split()
        if len(tmp) != 8:
            put_response = response_form('400', 'BAD_REQUEST')
            res = put_response
            print(data)
            print("-----------server-------------")
            client_socket.send(res.encode('utf-8'))
        else:
            job = tmp[0]
            if job in exist_job:
                post_response = response_form('400', 'BAD_REQUEST')
                res = post_response
                print(data)
                print("-----------server-------------")
                client_socket.send(res.encode('utf-8'))

            else:
                exist_job.append(job)
                level = tmp[4][:-1]
                ATK = tmp[7][:-1]
                jla = {"level": level, "ATK": ATK}
                json_data[job] = jla

                file = open('test.json', 'w', encoding='utf-8')
                json.dump(json_data, file)
                file.close()
                post_response = response_form('201', 'CREATED', body=str(jla))
                res = post_response
                print(data)
                print("-----------server-------------")
                client_socket.send(res.encode('utf-8'))

    #PUT
    elif method == "PUT":
        #1. input job
        #2. input level, ATK
        #

        tmp = data1[-1]
        tmp = tmp.split()
        if len(tmp) != 8:
            put_response = response_form('400', 'BAD_REQUEST')
            res = put_response
            print(data)
            print("-----------server-------------")
            client_socket.send(res.encode('utf-8'))
        else:
            job = tmp[0]
            if job not in exist_job:
                put_response = response_form('400', 'BAD_REQUEST')
                res = put_response
                print(data)
                print("-----------server-------------")
                client_socket.send(res.encode('utf-8'))

            else:
                level = tmp[4][:-1]
                ATK = tmp[7][:-1]
                jla = {"level" : level, "ATK" : ATK}
                json_data[job] = jla

                file = open('test.json', 'w', encoding='utf-8')
                json.dump(json_data, file)
                file.close()
                put_response = response_form('200', 'OK', body=str(jla))
                res = put_response
                print(data)
                print("-----------server-------------")
                client_socket.send(res.encode('utf-8'))

    #HEAD
    elif method == "HEAD":
        head_response = response_form('100', 'CONTINUE')
        res = head_response
        print(data)
        print("-----------server-------------")
        client_socket.send(res.encode('utf-8'))
    else:
        continue


