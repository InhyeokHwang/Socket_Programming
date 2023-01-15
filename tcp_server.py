#2021058995 황인혁

import multiprocessing
import socket

HEADER = 64 #client로부터 몇 바이트를 받을 것인지 정함
PORT = 5050
#SERVER = "192.168.219.108"
SERVER = socket.gethostbyname(socket.gethostname()) #ipconfig로 local ip를 알 수 있지만 gethostbyname함수로도 구할 수 있다.
ADDR = (SERVER, PORT)
FORMAT = 'utf-8' #형식
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #소켓 생성
server.bind(ADDR) #주소와 server에 대한 socket을 bind한다



def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.") #누가 연결되었는지 확인

    name = None #client가 입력할 이름
    connected = True
    while connected:
        if name is None:
            name_length = conn.recv(HEADER).decode(FORMAT)#HEADER byte만큼 receive, 바이트 포멧에서 string으로 decode
            if name_length:#서버만 켜진 상태를 처리하기 위해 if문으로 만듦(아무 메세지가 없을 경우)
                name_length = int(name_length) #string을 int로 변환 
                name = conn.recv(name_length).decode(FORMAT) #이름 길이만큼 decode
                conn.send(f"YOUR NAME IS {name}".encode(FORMAT)) #client에게 입력된 이름을 보내줌 
                continue #while문의 처음으로 돌아감
        msg_length = conn.recv(HEADER).decode(FORMAT) #client가 입력할 메세지
        if msg_length:#서버만 켜진 상태를 처리하기 위해 if문으로 만듦(아무 메세지가 없을 경우)
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE: #client가 quit을 입력할 경우 보내짐 
                connected = False

            print(f"[{addr}] {name}: {msg}") #client가 보낸 메세지 
            
            conn.send("[Message sent]".encode(FORMAT)) #client에게 메세지가 정상적으로 보내졌다고 알려줌

    conn.close() #연결 종료

def start():
    server.listen() #client를 기다림
    print(f"[LISTENING] Server is listening on {SERVER}") #서버의 ip
    try:
        while True: #서버가 꺼질 때까지
            conn, addr = server.accept() #새로운 연결이 들어오면 conn값(해당 클라이언트로 정보를 전달해주는 object) 과 addr값(클라이언트의 IP와 포트) 반환 
            process = multiprocessing.Process(target=handle_client, args=(conn, addr))
            process.start()
    except:
        print("Unexpected exception")
    finally:
        for process in multiprocessing.active_children():
            process.terminate() #프로세스 종료
            process.join() #이 프로세스가 완료될 때까지 기다린다

print("[STARTING] server is starting...")
start()

