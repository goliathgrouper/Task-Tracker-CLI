import sys, json, datetime

TASKLIST = 'tasklist.json'


def main():
    ensure_tasklist()


    arguments = sys.argv[1:]
    argc = len(arguments)
    
    if argc == 0:
        sys.exit('No arguments provided')
    elif argc > 3:
        sys.exit('Too many arguments provided')
    
    if arguments[0] == 'add' and argc == 2:
        with open(TASKLIST, 'w') as tasklist:
            json.dump(add_task(2, arguments[1], 'dingdong'), tasklist)

    

    

def add_task(id: int, description: str, status: str):
    now = datetime.datetime.now().strftime('%d/%m/%Y, %H:%M:%S')
    print(f'Task added successfully (ID: {id})')
    return json.dumps({'id': id, 
                       'description': description, 
                       'status':status, 
                       'created_at':now, 
                       'updated_at':now})

def choose_id(): 
    with open(TASKLIST, 'r') as tasklist:
        tasks = json.loads(tasklist)
    print(tasks)

def ensure_tasklist():
    try:
        tasklist = open(TASKLIST, 'x')
        tasklist.close()
    except FileExistsError:
        pass

if __name__ == '__main__':
    main()