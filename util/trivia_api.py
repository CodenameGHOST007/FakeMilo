import aiohttp
import random
import base64
import json


class API:
    def __init__(self):
        self.url = ""

    async def api_response(self):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.url) as resp:
                    response = await resp.json()
                    return response
        except Exception:
            return None

    async def get_trivia(self):
        self.url = "https://opentdb.com/api.php?amount=1&type=multiple"
        response = await self.api_response()
        response = response['results'][0]
        correct = response['correct_answer']
        options = [correct]+response['incorrect_answers']
        random.shuffle(options)
        char = 'A'
        for x in options:
            if x == correct:
                break
            char = chr(ord(char)+1)
        data = [response['question'], options, char, response['difficulty'], response['category']]
        #print(correct)
        return data