#! python -i
import sys, json, datetime

TASKLIST = "tasklist.json"


def main():
    ensure_tasklist()

    arguments = sys.argv[1:]
    argc = len(arguments)

    if argc == 0:
        sys.exit("No arguments provided")
    elif argc > 3:
        sys.exit("Too many arguments provided")

    if arguments[0] == "add" and argc == 2:
        with open(TASKLIST, "a") as tasklist:
            add_task(choose_id(), arguments[1], "dingdong")
    elif arguments[0] == "list":
        list_tasks()
    


def add_task(id: int, description: str, status: str):
    with open(TASKLIST, "r") as readfile:
        data = json.load(readfile)
    now = datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
    data.append(
        {
            "id": id,
            "description": description,
            "status": status,
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
    print(tasks)


def choose_id():
    with open(TASKLIST, "r") as readfile:
        data = json.load(readfile)
    used_ids = []
    for task in data:
        used_ids.append(task['id'])

    # Choose unused id
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
