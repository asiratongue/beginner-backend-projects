#Task Tracker, from roadmap.sh
import copy 
import json
import os

with open ('task_list.json', 'r') as file:
    try:
        task_dict = json.load(file)  
    except json.JSONDecodeError:
        task_dict = {}  

os.chdir(f'G:\\01101000111101\Programming\Projects\Backend Projects\Task Tracker')
#change directory to where Task Tracker directory is located.

def task_split(user_input): #extracting the task text

    task = user_input.split(':', 1)
    del task[0]
    taskstr = str(task[0])
    return taskstr

def add_task(user_input):                            #adding task to json file

    task_dict.update({user_input:'not done'})

    task_list_json = json.dumps(task_dict)
    with open('task_list.json', 'w') as file:     
        file.write(task_list_json)
    print(f'added task {user_input} to json file.')


def del_task(user_input):                           #deleting task from json file
    
    task_dict_copy = copy.copy(task_dict)


    with open('task_list.json', 'w') as file:

        for tasks in task_dict_copy.keys():
            if user_input in tasks:
                del task_dict[tasks]

                
        new_task_list = json.dumps(task_dict)             
        file.write(new_task_list)        

    print(f'deleted task {user_input} from json file.')


def update_task(user_input):                                     #updating task on json file


    print(f'''\nhowdy again, would you like to mark {user_input} as 'done' or 'in progress?''')
    status = input()

    if status == 'done':
        task_dict[user_input] = 'done'
    elif status == 'in progress':
        task_dict[user_input] = 'in progress'

    with open('task_list.json', 'w') as file:

        updated_task_list = json.dumps(task_dict)
        file.write(updated_task_list)

    print (f'updated the status of {user_input} to {status}')

def value_check(user_input):                                              #checking the values to print as list
     
    if user_input == "list tasks done": statuscheck = 'done' 
    elif user_input == 'list tasks not done': statuscheck = 'not done'
    elif user_input == 'list tasks in progress': statuscheck = 'in progress'

    for keys, values in task_dict.items():
        if values == statuscheck:
            print(keys, '-', values)
        else:
            continue


def list_all_tasks(user_input):                                      #listing all tasks

    with open('task_list.json', 'r') as file:
        for task in file.readlines():
            print(task)   


# Main program loop
while True:
    print(' ')
    print("howdy, what would you like to do today? (type help to print usage instructions)\n")
    user_input = input()
    print(' ')

    if user_input == 'help':

        print('''              'add task:(task)' - to add a task
              'del task:(task)' - to delete a task
              'update task:(task)' - to update a task
              'list all tasks' - to list all tasks
              'list tasks done' - to list all completed tasks
              'list tasks not done' - to list all tasks that are not completed
              'list tasks in progress' - to list all tasks that are in progress
              'stop' - to end the program''')
        continue
#####
    if user_input.startswith('add task:'):

        x = task_split(user_input)
        add_task(x)
        continue

    if user_input.startswith('del task:'):
        
        x = task_split(user_input)
        del_task(x)
        continue

    if user_input.startswith('update task:'):

        x = task_split(user_input)
        update_task(x)
        continue

    if user_input == 'list all tasks':
        list_all_tasks(user_input)
        continue

    if user_input in ('list tasks in progress', 'list tasks done', 'list tasks not done'):
        value_check(user_input)
        continue

    if user_input.startswith('stop'):
        break

    else:
        print('invalid input, please try again')
        continue