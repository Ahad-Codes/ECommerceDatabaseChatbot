from langchain.callbacks.base import BaseCallbackHandler
from pyboxen import boxen



class ChatModelStartHandler(BaseCallbackHandler):
    def on_chat_model_start(self, serialized, messages, **kwargs):
        print("\n\n========= Sending Messages to Chat Model =========\n\n")

        for msg in messages[0]:

            if msg.type == 'system':
                boxen_print(msg.content, title = msg.type, color = 'yellow')
            
            elif msg.type == 'human':
                boxen_print(msg.content, title = msg.type, color = 'green')

            elif msg.type == 'ai':
                if "function_call" in msg.additional_kwargs:
                    call = msg.additional_kwargs['function_call']
                    boxen_print(f"Running Tool {call['name']} with args {call['arguments']}", title = msg.type, color = 'blue')
                else: 
                    boxen_print(msg.content, title = msg.type, color = 'purple')

            elif msg.type == 'function':
                boxen_print(msg.content, title = msg.type, color = 'red')

            else:
                boxen_print(msg.content, title = msg.type, color = 'white')
            
def boxen_print(*args, **kwargs):
    print(boxen(*args, **kwargs))

boxen_print('Hey im testing this out', title = "Check", color='purple')