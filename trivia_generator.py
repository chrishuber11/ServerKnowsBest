#Make a code that stores all questions, and when called by
#server it generates topics with questions and bonus question
import random

#Global Variables
global Geography, History, Music, Entertainment, FoodandDrink, Technology, Animals, ForFun, Science, PopCulture
from trivia_questions import *

#Topics = [Geography, History, Music, Entertainment, FoodandDrink, Technology, Animals, Mythology, Nature, PopCulture]

#Settings

def generate_topics(max_topics):
    chosen_topics = []
    topic_keys = list(Topics.keys())
    while len(chosen_topics) < max_topics:
        topic_num = random.randint(0, len(Topics) - 1)
        topic_key = topic_keys[topic_num]
        if topic_key not in chosen_topics:
            chosen_topics.append(topic_key)
    return chosen_topics

def generate_questions(topic, questions_per_topic):
    chosen_questions = []
    topic_values = list(Topics[topic].keys())
    if len(topic_values) < questions_per_topic:
        print(f'Error: Not enough unique questions in the topic {topic}')
        return []
    while len(chosen_questions) < questions_per_topic:
        question_num = random.randint(0, len(topic_values) - 1)
        topic_value = topic_values[question_num]
        if topic_value not in chosen_questions:
            chosen_questions.append(topic_value)
    return chosen_questions

def trivia_generator(max_topics, questions_per_topic):
    topics = generate_topics(max_topics)
    question_list = []
    for topic in topics:
        question_list.append(generate_questions(topic, questions_per_topic))
    
    return topics, question_list

def main():
    max_topics = 3
    questions_per_topic = 5
    print(trivia_generator(max_topics, questions_per_topic))

if __name__ == '__main__':
    main()