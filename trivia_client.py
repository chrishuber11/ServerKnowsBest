from socket import *
import time
serverName = '149.84.185.123'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

topic_num = 1

print('Welcome to Server Knows Best!')
time.sleep(2)

#Username Input
username = input('Please enter your username: ')
username_encode = 'u0' + username
clientSocket.send(username_encode.encode())
username_decision = clientSocket.recv(2048).decode()
max_topics = username_decision[:1]
questions_per_topic = username_decision[1:2]
time.sleep(2)
if max_topics == 1:
    print(f'There will be {max_topics} topic, with {questions_per_topic} questions.')
else:
    print(f'There will be {max_topics} topics, each with {questions_per_topic} questions.')
time.sleep(2)
print('The game is case sensitive so use capitals and use numbers when applicable\nsuch as 1234 not onetwothreefour and dont worry about grammar.\nExample: What bug is yellow and black? Bee (not A Bee)')
#time.sleep(2)
#print('At the end of every round, the lowest scored player chooses the next topic.')
time.sleep(2)
print('Good Luck!')
time.sleep(2)

while True:
    server_message = clientSocket.recv(2048).decode()

    if server_message[:2] == 't0':
        decode_server_message = server_message[2:]
        print(decode_server_message)
        topic_num += 1

    if server_message[:2] == 'q0':
        decode_server_message = server_message[2:]
        print(decode_server_message)
        answer = input('Your Answer: ')
        answer_encode = 'a0' + answer + ':' + username
        clientSocket.send(answer_encode.encode())
        recieved = False
        while recieved == False:
            try:
                server_message = clientSocket.recv(2048).decode()
                if server_message:
                    decode_server_message = server_message[2:]    
                    if server_message[:2] == 'q1':
                        decode_server_message = server_message[2:]
                        print(decode_server_message)
                        recieved = True
            except:
                time.sleep(1)
            finally:
                time.sleep(1)

    if server_message[:2] == 'f0':
        decode_server_message = server_message[2:]
        print(decode_server_message)
        break
