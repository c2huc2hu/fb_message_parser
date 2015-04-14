# Get all messages from Facebook
from urllib.request import *
from urllib.parse import urlunsplit
import json

try:
    from defaults import access_token, thread_id
except ImportError as e:
    print("Make sure you created defaults.py as per the read-me")


def get_messages(thread_id, access_token):
    """
    Queries Facebook for all messages in a thread.

    Parameters:
    thread - an int or string with the id of the thread (e.g. 736059425928520)
    access_token - go here to get one: https://developers.facebook.com/tools/explorer/145634995501895
    
    Returns:
    A dictionary with {'created_times': [ ... ], 'from_names': [ ... ], 'messages': [ ... ]}
        The created times are strings representing the timestamps.
        From is who created the message as a string. 
        The messages are strings.
    All of these are in the same order. 
    """

    paging_token = "''"
    created_times = []
    from_names = []
    messages = []

    url = urlunsplit(('https', 'graph.facebook.com/v2.3', str(thread_id) + '/comments', 'fields=message,created_time,from&access_token={}'.format(access_token), ""))

    while(True):
        temp_created_times, temp_from_names, temp_messages = [], [], []  # temporary arrays that hold data backwards
        
        response = urlopen(url).read().decode()
        data = json.loads(str(response))
        #print(data)

        for message in data['data']:
            temp_created_times.append(message['created_time'])
            temp_from_names.append(message['from']['name'])
            if 'message' in message:
                temp_messages.append(message['message'])
            else:
                temp_messages.append("<Non-text message>")
        created_times.extend(temp_created_times[::-1])
        from_names.extend(temp_from_names[::-1])
        messages.extend(temp_messages[::-1])
        
        # get the next page of data if it exists
        if 'paging' in data:
            url = data['paging']['next']
        else:
            break
        
    return {'created_times': created_times, 'from_names': from_names, 'messages': messages}

d = get_messages(thread_id, access_token)
#print(d)
