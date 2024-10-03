import pandas as pd
from datetime import datetime
# class Message:
#     def __init__(self, message, sent_time):
#         self.message = message
#         self.sent_time = sent_time
    
#     def __repr__(self):
#         return f'Message(message="{self.message}", sent_time="{self.sent_time}")'

class Message:
    def __init__(self, message, sent_time, first_message_time):
        self.message = message
        self.sent_time = sent_time
        self.elapsed_time = sent_time - first_message_time
        self.first_message_time = first_message_time
    
    def __repr__(self):
        return f'Message(message="{self.message}", sent_time="{self.sent_time}", elapsed_time={self.elapsed_time})'


df = pd.read_csv("messages.csv", index_col=False)
df = df.drop([0, 1, 2, 3])

# print(output_string)
# messages = [Message(f"{row['sender']}: {row['content']}", row['sentTime']) for index, row in df.iterrows()]


first_message_time = df['sentTime'].iloc[0]
first_message_time = datetime.strptime(df['sentTime'].iloc[0], '%Y-%m-%d %H:%M:%S')

print(first_message_time)

chat_history = [
    Message(
        message=f"{row['sender']}: {row['content']}", 
        sent_time=datetime.strptime(row['sentTime'], '%Y-%m-%d %H:%M:%S'),
        first_message_time=first_message_time
    ) 
    for index, row in df.iterrows()
]


