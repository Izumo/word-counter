from flask import Flask
from flask import request

import requests
import json
import os
import datetime
import urllib
import asyncio

import queue
import threading
import jsonpickle

app = Flask(__name__)

PORT = os.environ.get('PORT', 8000)
TOKENIZER_URL = os.environ.get('TOKENIZER_URL', 'http://127.0.0.1:8001')
MAPPER_URL = os.environ.get('MAPPER_URL', 'http://127.0.0.1:8002')
REDUCER_URL = os.environ.get('REDUCER_URL', 'http://127.0.0.1:8003')

def log(message):
    print(str(datetime.datetime.now()) + ": " + message)

@app.route('/CountWords', methods=['POST'])
def count_words():

    print(str(datetime.datetime.now()) + ": Request Received")

    word_space = queue.Queue()
    threads = []

    text_data = request.get_data(as_text=True)
#   print(text_data)

    log("Send all request to handler")
    for line in split_lines(text_data):
        if (len(line) > 0):
            handle_line(word_space, line);
#           t = threading.Thread(target = handle_line, args=(word_space, line))
#           t.start()
#           threads.append(t)

    log("Waiting all thread termination")
#   [t.join() for t in threads]

    word_list = []
    while not word_space.empty():
        word_list.extend(word_space.get())

    log("Counting Words")
    count = count_words(word_list)

    result  = sorted(count.items(), reverse=True, key = lambda word : word[1])[0:25]
    log("Sorted and return the result")

    print(f"RESULT: {result}")
    return jsonpickle.encode(result)

def split_lines(data):
    return data.split('\n')

def count_words(list):
    response = requests.post(REDUCER_URL, data = json.dumps(list))
    return  response.json()
    

def handle_line(queue, line):

    response = requests.get(TOKENIZER_URL + '?line=' + urllib.parse.quote(line))
    word_list = response.json()

    response = requests.post(MAPPER_URL, data = json.dumps(word_list))
    word_dicts = response.json()

    queue.put(word_dicts)


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=PORT)
