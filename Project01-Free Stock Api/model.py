from data import Database
from financial_api import fmp_financial_analyst
from openai import OpenAI
from typing import Any

class BotModel:
    def __init__(self) -> None:
        self.db = Database()
        self.client : OpenAI = OpenAI()
        self.messages = self.load_chat_history()
        self.messsage = None

    def load_chat_history(self)->[]:
        return self.db.load_chat_history()

    def save_chat_history(self):
        print("Model: Save", self.messages)
        self.db.save_chat_history(messages=self.messages)

    def listen_chat_history(self):
      
        if len(self.messages) > 0:
            full_response = ""
            for message in self.messages:
                
                full_response += message["content"]
                
            #print('full reponse', full_response)
            #getUserMassage = [{'role': entry['role'], 'content': entry['content']} for entry in self.messages] 
           #print('////////////////////////////////////////////////////////////////////////')    
            #print(getUserMassage)  
            #print('////////////////////////////////////////////////////////////////////////')    
            speech_file_path : str = "urdu.mp3"
            response = self.client.audio.speech.create(
                model="tts-1",
                voice="alloy",
                input=full_response
            )
            response.stream_to_file(speech_file_path)
            
    def translation(self, language):
        if len(self.messages) > 0:
            full_response = ""
            for message in self.messages:
                full_response += message["content"]
                
            try:
                
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo-1106",
                    messages=[
                        {
                        "role": "system",
                        "content": f"You will be provided with a sentence in English, and your task is to translate it into {language}."
                        },
                        {
                        "role": "user",
                        "content": full_response
                        }
                    ]
                    )
                print('////////////////////////////////////////////////////////////////////////')    
                print(full_response)
                print('////////////////////////////////////////////////////////////////////////')    
                return response.choices[0].message.content  
            except: 
                return "Something went wrong, please try again"
        
            
        
        
    def delete_chat_history(self):
        print("Model: Delete")
        self.messages = []
        self.save_chat_history()

    def get_messages(self)->[dict]:
        return self.messages
    
    def append_message(self, message: dict):
        self.messages.append(message)
        
    def send_message(self, message: dict)->Any:
        self.append_message(message=message)
        stream = message.get('content', 'No content available')
        stream = fmp_financial_analyst(stream)
        print(stream)
        return stream
    
    
