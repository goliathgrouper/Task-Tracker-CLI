#! ..\venv\Scripts\python.exe 
import sys, json, datetime
from tabulate import tabulate

TASKLIST = "tasklist.json"


def main():
    ensure_tasklist()

    arguments = sys.argv[1:]
    argc = len(arguments)

    # Handle general number of arguments
    if argc == 0:
        sys.exit("No arguments provided")
    elif argc > 3:
        sys.exit("Too many arguments provided")

    # Add handler
    if arguments[0] == "add" and argc == 2:
        add_task(choose_id(), arguments[1])
        if argc != 2:
            sys.exit("Incorrect usage!")

    if arguments[0] == "list":
        if argc == 1:
            list_tasks()

    if arguments[0] == 'mark-in-progress':
        if argc != 2:
            sys.exit('Incorrect usage!')
        mark_in_progress(arguments[1])
        
            
        
        


    # Wait for input before closing
    input()


# Add todo task
def add_task(aid: int, description: str):
    with open(TASKLIST, "r") as readfile:
        data = json.load(readfile)
    now = datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
    data.append(
        {
            "id": aid,
            "description": description,
            "status": "todo",
            "created_at": now,
            "updated_at": now,
        }
    )
    with open(TASKLIST, "w") as writefile:
        json.dump(data, writefile)
    print(f"Task added successfully (ID: {aid})")


def list_tasks():
    with open(TASKLIST, "r") as file:
        tasks = json.load(file)
    for task in tasks:
        print(
            tabulate(
                [
                    ["id", task["id"]],
                    ["description", task["description"]],
                    ["status", task["status"]],
                    ["created at", task["created_at"]],
                    ["updated at", task["updated_at"]],
                ]
            )
        )


# Choose unused id
def choose_id():
    with open(TASKLIST, "r") as readfile:
        data = json.load(readfile)
    used_ids = []
    for task in data:
        used_ids.append(task["id"])

    for aid in range(1, 101):
        if aid not in used_ids:
            return aid


def ensure_tasklist():
    try:
        tasklist = open(TASKLIST, "x")
        json.dump([], tasklist)
        tasklist.close()
    except FileExistsError:
        pass

# Returns True if id is used else False
def check_for_id(aid): # its 'aid' not 'id' because of std function id in python
    with open(TASKLIST, 'r') as rf:
        data = json.load(rf)
    used_ids = []
    for task in data:
        used_ids.append(task["id"])
    return aid in used_ids

def mark_in_progress(aid):
    try:
        aid = int(aid)
        if aid <= 0:
            sys.exit('Id should be a positive integer')
    except ValueError:
        sys.exit('Id should be a positive integer')
    if not(check_for_id(aid)):
        sys.exit('No task with this id')
    with open(TASKLIST, 'r') as rf:
        data = json.load(rf)
    for i in range(len(data)):
        if data[i]['id'] == aid:
            data[i]['status'] = 'in-progress'
    with open(TASKLIST, 'w') as wf:
        json.dump(data, wf)
        



if __name__ == "__main__":
    main()
