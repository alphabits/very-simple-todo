#!/usr/bin/python
import json
from optparse import OptionParser
import os
import sys
from termcolor import colored


DATA_FILE = os.path.expanduser('~/.todos.json')
COLORS = {
    'normal': 'blue',
    'urgent': 'red',
    'chill': 'green'
}
URGENCY_LEVELS = COLORS.keys()
DEFAULT_URGENCY = 'normal'


def main():
    ensure_data_file_exists()
    todo_db = load_todos()
    command, args, options = parse_command_arguments()
    output = command(args, options, todo_db)
    if output:
        print output

def ensure_data_file_exists():
    if not os.path.isfile(DATA_FILE):
        with open(DATA_FILE, 'a') as f:
            f.write('[]')

def load_todos():
    with open(DATA_FILE, 'r') as f:
        todo_db = [Todo(**todo_data) for todo_data in json.load(f)]
    return todo_db

def parse_command_arguments():
    p = get_option_parser()
    options, args = p.parse_args()
    command = get_command_from_args(args)
    args = args[1:]
    return command, args, options

def get_command_from_args(args):
    command_name = args[0] if args else 'list'
    if not command_name in COMMANDS:
        raise Exception('Command not found')
    return COMMAND_ROUTES[command_name]

def get_option_parser():
    p = OptionParser()
    for urgency_level in URGENCY_LEVELS:
        short_opt = '-'+urgency_level[0]
        long_opt = '--'+urgency_level
        p.add_option(short_opt, long_opt, action='store_const', 
                const=urgency_level, dest='urgency_level')
    p.add_option('-a', '--show-all', action='store_true', dest='show_all')
    p.set_defaults(show_all=False)
    return p

def colorize(msg, color):
    return colored(msg, color, None, attrs=['bold'])

def print_todos(todos):
    return '\n'.join(map(print_todo, todos))

def print_todo(todo):
    color = 'grey' if todo.completed else COLORS[todo.urgency_level]
    return colorize(todo.label(), color)

def get_next_todo_id(todo_list):
    if not todo_list:
        return 1
    return max(todo.id for todo in todo_list) + 1

def get_todo_by_id(id, todo_list):
    return [todo for todo in todo_list if todo.id == id]

def save_todos(todo_list):
    data = [todo.to_data() for todo in todo_list]
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)


def list_cmd(args, options, todo_list):
    if not options.show_all:
        todo_list = [todo for todo in todo_list if not todo.completed]
    return print_todos(todo_list)

def add_cmd(args, options, todo_list):
    if not args:
        raise Exception('Todo description is missing')
    id = get_next_todo_id(todo_list)
    description = args[0]
    urgency_level = options.urgency_level
    todo_list.append(Todo(id, description, urgency_level))
    save_todos(todo_list)
    return ''

def complete_cmd(args, options, todo_list):
    if not args:
        raise Exception('Todo id is missing')
    id = int(args[0])
    todo = get_todo_by_id(id, todo_list)
    if not todo:
        raise Exception('Todo with id: '+str(id)+' not found')
    todo[0].completed = True
    save_todos(todo_list)

COMMAND_ROUTES = {
    'list': list_cmd,
    'add': add_cmd,
    'complete': complete_cmd
}
COMMANDS = COMMAND_ROUTES.keys()


class Todo(object):

    def __init__(self, id, description, urgency_level=None, completed=False):
        self.id = id
        self.description = description
        self.urgency_level = (urgency_level 
                              if urgency_level in URGENCY_LEVELS else 
                              DEFAULT_URGENCY)
        self.completed = completed

    def label(self):
        return u'{0}  {1}'.format(self.id, self.description) 

    def to_data(self):
        return {
            'id': self.id,
            'description': self.description,
            'urgency_level': self.urgency_level,
            'completed': self.completed
        }


if __name__ == '__main__':
    main()
    sys.exit(0)
