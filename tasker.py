#! ..\venv\Scripts\python.exe
import sys, json, datetime
from tabulate import tabulate

TASKLIST = "tasklist.json"
INPROGRESS = "in-progress"
TODO = "todo"
DONE = "done"
COMMANDS = ['list', 'delete', 'update', 'mark-done', 'mark-todo', 'mark-in-progress', 'add']


def main():
    ensure_tasklist()

    arguments = sys.argv[1:]
    argc = len(arguments)

    # Handle general number of arguments
    if argc == 0:
        sys.exit("No arguments provided")
    elif argc > 3:
        sys.exit("Too many arguments provided")
    if arguments[0] not in COMMANDS:
        sys.exit("No such command!")

    # Add command handler
    if arguments[0] == "add" and argc == 2:
        add_task(choose_id(), arguments[1])
        if argc != 2:
            sys.exit("Incorrect usage!")

    # List command handler
    if arguments[0] == "list":
        if argc == 1:
            list_tasks()
        elif argc == 2:
            if arguments[1] not in ["in-progress", "todo", "done"]:
                sys.exit("To list tasks by status use: in-progress, todo or done")
            list_tasks(arguments[1])
        else:
            sys.exit("Too many arguments for list command!")

    # Different mark command handlers
    if arguments[0] == "mark-in-progress":
        if argc != 2:
            sys.exit("Incorrect usage! Provide an id.")
        mark_task(arguments[1], INPROGRESS)
    if arguments[0] == "mark-done":
        if argc != 2:
            sys.exit("Incorrect usage! Provide an id.")
        mark_task(arguments[1], DONE)
    if arguments[0] == "mark-todo":
        if argc != 2:
            sys.exit("Incorrect usage! Provide an id.")
        mark_task(arguments[1], TODO)

    # Delete command handler
    if arguments[0] == 'delete':
        if argc != 2:
            sys.exit('Incorrect usage! Try: delete <id>')
        delete_task(arguments[1])

    # Wait for input before closing
    #input()


# Add todo task
def add_task(id: int, description: str):
    with open(TASKLIST, "r") as readfile:
        data = json.load(readfile)
    now = datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
    data.append(
        {
            "id": id,
            "description": description,
            "status": "todo",
            "created_at": now,
            "updated_at": now,
        }
    )
    with open(TASKLIST, "w") as writefile:
        json.dump(data, writefile)
    print(f"Task added successfully (ID: {id})")


def list_tasks(spec=""):
    with open(TASKLIST, "r") as file:
        tasks = json.load(file)
    if not spec:

        for task in tasks:
            print(
                tabulate(
                    [
                        ["id", task["id"]],
                        ["description", task["description"]],
                        ["status", task["status"]],
                        ["created at", task["created_at"]],
                        ["updated at", task["updated_at"]],
                    ],
                    tablefmt="double_outline",
                )
            )
    elif spec not in ["todo", "in-progress", "done"]:
        sys.exit("Incorrect usage!")
    else:
        for task in tasks:
            if task["status"] == spec:
                print(
                    tabulate(
                        [
                            ["id", task["id"]],
                            ["description", task["description"]],
                            ["status", task["status"]],
                            ["created at", task["created_at"]],
                            ["updated at", task["updated_at"]],
                        ],
                        tablefmt="double_outline",
                    )
                )


# Choose unused id
def choose_id():
    with open(TASKLIST, "r") as readfile:
        data = json.load(readfile)
    used_ids = []
    for task in data:
        used_ids.append(task["id"])

    for id in range(1, 101):
        if id not in used_ids:
            return id


def ensure_tasklist():
    try:
        tasklist = open(TASKLIST, "x")
        json.dump([], tasklist)
        tasklist.close()
    except FileExistsError:
        pass


# Returns True if id is used else False
def check_for_id(id):
    with open(TASKLIST, "r") as rf:
        data = json.load(rf)
    used_ids = []
    for task in data:
        used_ids.append(task["id"])
    return id in used_ids


def mark_task(id, spec):
    if spec not in ["todo", "in-progress", "done"]:
        sys.exit("No such option for mark_task function")
    try:
        id = int(id)
        if id <= 0:
            sys.exit("Id should be a positive integer")
    except ValueError:
        sys.exit("Id should be a positive integer")
    if not (check_for_id(id)):
        sys.exit("No task with this id")
    with open(TASKLIST, "r") as rf:
        data = json.load(rf)
    tasktoprint = {}
    for i in range(len(data)):
        if data[i]["id"] == id:
            data[i]["status"] = spec
            tasktoprint = data[i]
            break
    with open(TASKLIST, "w") as wf:
        json.dump(data, wf)
        print("Task:")
        print(
            tabulate(
                [
                    ["id", tasktoprint["id"]],
                    ["description", tasktoprint["description"]],
                    ["status", tasktoprint["status"]],
                    ["created at", tasktoprint["created_at"]],
                    ["updated at", tasktoprint["updated_at"]],
                ],
                tablefmt="double_outline",
            )
        )
        print(f"Successfully marked {spec}")

def delete_task(id):
    try:
        id = int(id)
        if id <= 0:
            sys.exit('Id should be a positive integer!')
    except ValueError:
        sys.exit('Id should be a positive integer!')
    if not check_for_id(id):
        sys.exit('Didn\'t find task with the provided id! Use list command to see all tasks.')
    with open(TASKLIST, 'r') as rf:
        data = json.load(rf)
    for i in range(len(data)):
        if data[i]['id'] == id:
            tasktodelete = data[i]
            del data[i]
            
            break
    with open(TASKLIST, 'w') as wf:
        json.dump(data, wf)
    print("Task:")
    print(
        tabulate(
            [
                ["id", tasktodelete["id"]],
                ["description", tasktodelete["description"]],
                ["status", tasktodelete["status"]],
                ["created at", tasktodelete["created_at"]],
                ["updated at", tasktodelete["updated_at"]],
            ],
            tablefmt="double_outline",
        )
    )
    print(f"Successfully deleted")






if __name__ == "__main__":
    main()
