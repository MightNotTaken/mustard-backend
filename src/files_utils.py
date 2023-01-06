import json
import os
import datetime

def p(segment):
    return os.path.join(os.path.dirname(__file__), segment)

def date_to_number(date=None):
    if not date:
        date = datetime.datetime.now()
    response = date.year
    response *= 100
    response += date.month
    response *= 100
    response += date.day
    return response

def get_index():
    try:
        with open(p('./../database/index.json'), 'r') as f:
            data = json.load(f)
        if date_to_number() > data['date']:
            data = {'index': 1, 'date': date_to_number()}
            with open(p('./../database/index.json'), 'w') as f:
                json.dump(data, f)
        return data['index']
    except FileNotFoundError:
        with open(p('./../database/index.json'), 'w') as f:
            json.dump({'index': 1, 'date': date_to_number()}, f)
        return 1
    except ValueError:
        return 'Error parsing JSON file'

def update_index():
    try:
        index = get_index()
        with open(p('./../database/index.json'), 'w') as f:
            json.dump({'index': index + 1, 'date': date_to_number()}, f)
        return index + 1
    except:
        return 'Error updating index file'

def get_today_file():
    try:
        file_name = f'./../database/{date_to_number()}.csv'
        if not os.path.exists(p(file_name)):
            with open(p(file_name), 'w') as f:
                f.write('S.No.,Test No.,Yellow,Dark Green,Medium Green,Light Green,Brown\n')
        return file_name
    except OSError as error:
        return error

def get_test_number(id):
    return f'SQT{date_to_number()}-{id}'

def mapToStr(data):
    for i in range(len(data)):
        data[i] = str(data[i])
    return data

def add_new_entry(data):
    try:
        file_name = get_today_file()
        index = get_index()
        response = f'{index},{get_test_number(index)},{",".join(mapToStr(data))}\n'
        with open(p(file_name), 'a') as f:
            f.write(response)
        update_index()
        return True
    except OSError as error:
        return error

def initialize():
    if not os.path.exists(p('./../database')):
        try:
            os.mkdir(p('./../database'))
        except OSError:
            print('Unable to initialize database directory')

initialize()
