from socket import *
import time
from trivia_generator import trivia_generator
from trivia_questions import *

while True:
    total_player_count = int(input('Enter number for amount of players: '))
    if total_player_count < 1:
        print('Error: Please choose a number higher than 0.')
    else:
        break

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(total_player_count+1)

#Settings
max_topics = 1
questions_per_topic = 3

try:
    trivia = trivia_generator(max_topics, questions_per_topic)
except:
    print('Error: An issue occured with the trivia generator.')
    exit()

topics = trivia[0]
questions = trivia[1]
print(f'The topics chosen are: {topics}, with these questions: {questions}')

usernames = {}
player_count = 0

print('The Server is ready to recieve players!')

while player_count < total_player_count:

    #waiting for incoming connection requests
    connectionSocket, addr = serverSocket.accept()
    print('A Player is attempting to join.')
    try:
        username_request = connectionSocket.recv(2048).decode()
    except:
        print('A Player failed to join.')
        connectionSocket.close()
        continue

    if username_request[:2] == 'u0':
        if username_request[2:] not in usernames.keys() and addr not in usernames.values():
            usernames[username_request[2:]] = {'socket': connectionSocket, 'score': 0}
            #print('Recieved the message', message)
            serversend_username = str(max_topics) + str(questions_per_topic) + 'You are in! Your username is now: ' + username_request[2:]
            print('A Player has joined.')
            player_count += 1
        else:
            serversend_username = 'This username is taken'

        connectionSocket.send(serversend_username.encode())
        #print('Username List: ', usernames)

time.sleep(2)
print('Player lobby has been successfully created!')
time.sleep(2)
lobby = [key for key in usernames]
print('Lobby: ', lobby)
time.sleep(2)
print('Starting game...')
#Example Formatting for selecting a question: Topics['topic'][questions[0][0]]


topic_total = 0
while topic_total < len(topics):
    topic = topics[topic_total]
    serversend_topic = f'Topic {topic_total+1} is: {topic}\n'
    print(serversend_topic)
    serversend_topic_coded = 't0' + serversend_topic
    for user in usernames:
        try:
            usernames[user]['socket'].send(serversend_topic_coded.encode())
        except:
            print(f'Player: {user} has left.')
            del usernames[user]
            player_count -= 1
        #print(f'All users successfully recieved Topic: {serversend_topic}\n')

    question_total = 0
    while question_total < questions_per_topic:
        time.sleep(2)
        serversend_question = Topics[topics[topic_total]][questions[topic_total][question_total]][0]
        print(serversend_question)
        serversend_question_coded = 'q0' + serversend_question + '\n'
        for user in usernames:
            usernames[user]['socket'].send(serversend_question_coded.encode())
        #print(f'All users successfully recieved Question: {serversend_question}')
        
        #Code to wait for answers
        answers_recieved = 0
        correct_answer = Topics[topics[topic_total]][questions[topic_total][question_total]][1]
        for user in usernames:
            connectionSocket = usernames[user]['socket']
            #print(connectionSocket)

            # Each player has its own flag
            received = False

            while not received:
                try:
                    server_receive_answer = connectionSocket.recv(2048).decode()
                    if server_receive_answer:
                        received = True
                        break
                    else:
                        time.sleep(1)
                except (OSError, socket.error) as e:
                    print(f'Socket Error: {e}')
                    break

            if received:
                answers_recieved += 1
                if server_receive_answer[:2] == 'a0':
                    answer, user = server_receive_answer[2:].split(':', 1)
                    if answer == correct_answer:
                        usernames[user]['score'] += 1
                        serversend_answer = f'Correct! Your score is now: {usernames[user]["score"]}'
                    else:
                        serversend_answer = f'Incorrect! The answer was {correct_answer}. Your score is now: {usernames[user]["score"]}'
                        
                    serversend_answer_coded = 'q1' + serversend_answer
                    connectionSocket.send(serversend_answer_coded.encode())

        print('The correct answer was: ' + correct_answer + '\n')
        question_total += 1

    topic_total += 1

    if max_topics-topic_total == 0:
        print(f'Topic {topic_total+1} - {topic} is complete! Thats all of the questions!')
        highest_score = None
        winners = []
        time.sleep(2)
        print('Time to announce the winner!')
        for username, user_info in usernames.items():
            if highest_score is None or user_info['score'] > highest_score:
                highest_score = user_info['score']
                winners = [username]
            elif user_info['score'] == highest_score:
                winners.append(username)
        
        for user in usernames:
            serversend_final = f'The game is over! This is your final score: {usernames[user]["score"]}\n'
            serversend_final_coded = 'f0' + serversend_final
            if user in winners:
                if len(winners) > 1:
                    serversend_final_coded = serversend_final_coded + 'You tied for first! Congrats!'
                else:
                    serversend_final_coded = serversend_final_coded + 'You won the game! Congrats!'
            try:
                usernames[user]['socket'].send(serversend_final_coded.encode())
            except:
                continue        
        for winner in winners:
            print(f'Username: {winner}, Score: {highest_score}')
        if len(winners) > 1:
            print('It was a tie!')
        else:
            print(f'Congrats {winners[0]}!\n')
        time.sleep(3)
        print('Final Scores: ')
        for username, user_info in usernames.items():
            print(f'Username: {username}, Score: {user_info["score"]}')
    elif max_topics-topic_total == 1:
        print(f'Topic {topic_total+1} - {topic} is complete! There is {max_topics-topic_total} Topic left!')
        time.sleep(2)
        print('Current Scores: ')
        for username, user_info in usernames.items():
            print(f'Username: {username}, Score: {user_info["score"]}')
        print('Good Luck!\n')
    else:
        print(f'Topic {topic_total+1} - {topic} is complete! There is {max_topics-topic_total} Topics left!')
        time.sleep(2)
        print('Current Scores: ')
        for username, user_info in usernames.items():
            print(f'Username: {username}, Score: {user_info["score"]}')
        print('Good Luck!\n')

    #serversend = server sending packet
    #serverrecieve = server recieving packet
    #u0 == general username code word
    #t0 == general title code word
    #q0 == general question code word
    #a0 == general answer code word
    #q1 == reply to whether correct or not code word
    #q2 == tie breaker question code word
    #f0 == final score for client code word
