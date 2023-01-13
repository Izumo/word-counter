import os
import datetime
import json

import uvicorn
from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response

import aiohttp
import asyncio
import urllib

PORT = os.environ.get('PORT', 8000)
TOKENIZER_URL = os.environ.get('TOKENIZER_URL', 'http://127.0.0.1:8001')
MAPPER_URL = os.environ.get('MAPPER_URL', 'http://127.0.0.1:8002')
REDUCER_URL = os.environ.get('REDUCER_URL', 'http://127.0.0.1:8003')

def log(message):
    print(str(datetime.datetime.now()) + ": " + message)

app = FastAPI()

@app.post("/CountWords")
async def count_words(request: Request):

    log("Request Received")

    text_data = (await request.body()).decode()    # b string to string

    tasks = []
    session = aiohttp.ClientSession()
    for line in text_data.split('\n'):
        if (len(line) > 0):
            task = handle_lines(line, session)
            tasks.append(task)

    log("Send all request to handlers")

    word_dict = []
    word_dict_lists = await asyncio.gather(*tasks)

    log("All responses are received. Counting words")

    for list in word_dict_lists:
        word_dict.extend(list)

    count = await count_words(word_dict, session)
#   print(count)

    log("Count words done")

    result = sorted(count.items(), reverse=True, key = lambda word : word[1])[0:25]
    log("Sorted and return the result")

    await session.close()

    print(f"RESULT: {result}")
#   return jsonpickle.encode(result)
    return result



def split_lines(data):
    return data.split('\n')

def tokenize(line):
    return line.split(' ')

async def handle_lines(line, session):

    async with session.get(TOKENIZER_URL + '?line=' + urllib.parse.quote(line)) as response:
        word_list = await response.json()

#   log("Tokenized")

    async with session.post(MAPPER_URL, data = json.dumps(word_list)) as response:
        word_dicts = await response.json()

#   log("Mapped")

    return word_dicts

async def count_words(list, session):
    async with session.post(REDUCER_URL, data = json.dumps(list)) as response:
        return await response.json()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(PORT))
