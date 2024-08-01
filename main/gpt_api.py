import openai
'''
class GptAPI():
    def __init__(self, model, api_key):
        self.messages = []
        self.model = model
        openai.api_key = api_key
    
    def get_message(self, prompt):
        self.messages.append({"role": "user", "content": prompt})

        stream = openai.ChatCompletion.create(
            model=self.model,
            messages=self.messages,
            stream=True,
        )

        result = ''
        for chunk in stream:
            if 'delta' in chunk['choices'][0]:
                if 'content' in chunk['choices'][0]['delta']:
                    string = chunk['choices'][0]['delta']['content']
                    result += string

        self.messages.append({"role": "assistant", "content": result})
        return result
'''
import openai

class GptAPI():
    def __init__(self, model, api_key):
        self.messages = []
        self.model = model
        openai.api_key = api_key
    
    def get_message(self, prompt):
        self.messages.append({"role": "user", "content": prompt})

        response = openai.ChatCompletion.create(
            model=self.model,
            messages=self.messages,
        )

        result = response.choices[0].message['content']
        self.messages.append({"role": "assistant", "content": result})
        return result, self.messages
