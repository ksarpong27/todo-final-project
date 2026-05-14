import json
import argparse
import os

#Creates a default todo list if one isn't specified
DEFAULT_FILE = "TODO.json"

#Loads the tasks from the JSON file
def load_tasks(filename):
    if not os.path.exists(filename):
        return[]
    with open(filename, "r") as file:
        return json.load(file)

#Saves the updated task back to the json file   
def save_tasks(filename, tasks):
    with open(filename, "w") as file:
        json.dump(tasks, file, indent=4)

#Adds a new task to the todo list
def add_task(filename, category, description):
    tasks = load_tasks(filename)
    new_id = len(tasks) +1

    task = {
        "id": new_id,
        "category": category,
        "description": description,
        "status": "incomplete"
    }

    tasks.append(task)
    save_tasks(filename, tasks)
    print("Task added successfully")

#Displays all the tasks in the todo list
def view_tasks(filename):
    tasks = load_tasks(filename)
    if len(tasks) == 0:
        print("No tasks found")
        return
    
    for task in tasks:
        print("-----------------")
        print("ID:", task["id"])
        print("Category:", task["category"])
        print("Description:", task["description"])
        print("Status:", task["status"])

#Changes yhe status of the task
def update_status(filename, task_id, new_status):
    if new_status not in ["incomplete", "in progress", "complete"]:
        print("Invalid status")
        return
    tasks = load_tasks(filename)

    for task in tasks:
        if task["id"] == task_id:
            task["status"] = new_status
            save_tasks(filename, tasks)
            print("Status updated")
            return
    print("Task not found")

#Edits the description of an existing task
def edit_task(filename, task_id, new_description):
    tasks = load_tasks(filename)

    for task in tasks:
        if task["id"] == task_id:
            task["description"] = new_description
            save_tasks(filename, tasks)
            print("Task updated")
            return
    print("Task not found")

#Allows the user type in the terminal and creates subcommands
parser = argparse.ArgumentParser()
parser.add_argument("--list-name", default=DEFAULT_FILE)
subparsers = parser.add_subparsers(dest="command")

add_parser = subparsers.add_parser("add")
add_parser.add_argument("category")
add_parser.add_argument("description")

view_parser = subparsers.add_parser("view")
status_parser = subparsers.add_parser("status")
status_parser.add_argument("id", type=int)
status_parser.add_argument("status")

edit_parser = subparsers.add_parser("edit")
edit_parser.add_argument("id", type=int)
edit_parser.add_argument("description")

#Reads all comman line inputs and stores the filename the user wants to put
args = parser.parse_args()
filename = args.list_name

if args.command == "add":
    add_task(filename, args.category, args.description)
elif args.command == "view":
    view_tasks(filename)
elif args.command == "status":
    update_status(filename, args.id, args.status)
elif args.command == "edit":
    edit_task(filename, args.id, args.description)
else:
    print("Invalid command")
