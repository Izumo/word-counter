from flask import Flask
from flask import request

import requests
import json
import os

import queue
import threading

app = Flask(__name__)

PORT = os.environ.get('PORT', 8000)
TOKENIZER_URL = os.environ.get('TOKENIZER_URL', 'http://127.0.0.1:8001')
MAPPER_URL = os.environ.get('MAPPER_URL', 'http://127.0.0.1:8002')
REDUCER_URL = os.environ.get('REDUCER_URL', 'http://127.0.0.1:8003')

@app.route('/CountWords', methods=['POST'])
def count_words():

    word_space = queue.Queue()
    threads = []

    text_data = request.get_data(as_text=True)
#   print(text_data)

    for line in split_lines(text_data):
        if (len(line) > 0):
            t = threading.Thread(target = handle_line, args=(word_space, line))
            t.start()
            threads.append(t)

    [t.join() for t in threads]

    word_list = []
    while not word_space.empty():
        word_list.extend(word_space.get())

    count = count_words(word_list)

    result  = sorted(count.items(), reverse=True, key = lambda word : word[1])[0:25]

    print(f"RESULT: {result}")
    return result

def split_lines(data):
    return data.split('\n')

def count_words(list):
    response = requests.post(REDUCER_URL, data = json.dumps(list))
    return  response.json()
    

def handle_line(queue, line):
#   print(line)

    response = requests.get(TOKENIZER_URL + '?line=' + line)
    word_list = response.json()

#   for word in word_list:
#       print(f"DEBUG: {word}")

    response = requests.post(MAPPER_URL, data = json.dumps(word_list))
    word_dicts = response.json()

#   print(f"DEBUG: {word_dicts}")

    queue.put(word_dicts)


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=PORT)
