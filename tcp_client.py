#2021058995 황인혁

import socket

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
NAME = None #client의 이름
SERVER = socket.gethostbyname(socket.gethostname()) #어느 서버로 연결할 것인지 ip 입력
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #소켓 생성
client.connect(ADDR) #서버로 연결

def send(msg):
    message = msg.encode(FORMAT) #메세지를 보낼 때 string을 바이트 format으로 encode
    msg_length = len(message) #메세지 길이 
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length)) #padding 추가
    client.send(send_length)#길이를 먼저 보내고
    client.send(message) #메세지를 보냄 
    print(client.recv(2048).decode(FORMAT)) #서버로부터 보내짐

print("Enter your name :") #이름 입력 메세지
NAME = input() 
send(NAME) #입력한 이름을 서버로 전송


while True:
    msg = input() #메세지 입력 
    if msg == "quit": #quit을 입력할 경우 while문을 나가면서 서버와 연결을 끊음 
        break;
    send(msg)


send("[" +NAME + " DISCONNECTED]") #누가 연결을 끊었는지 서버로 전송