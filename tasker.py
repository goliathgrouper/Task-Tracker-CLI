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

    if arguments[0] == "add" and argc == 2:
        add_task(choose_id(), arguments[1])
        if argc != 2:
            sys.exit("Incorrect usage!")

    if arguments[0] == "list" and argc == 1:
        list_tasks()
    # Wait for input before closeing
    input()


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


if __name__ == "__main__":
    main()
