import argparse
import json
import os

file_path = "todos.json"

def initialize_file():
    """Initialize the JSON file if it doesn't exist."""
    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            json.dump({"items": []}, f)

def addItem():
    """Add a new item to the todo list."""
    todo = [args.add[0], 0]

    initialize_file()

    with open(file_path, "r") as f:
        data = json.load(f)

    if any(item[0] == todo[0] for item in data['items']):
        print("ERROR: Item already exists")
    else:
        data['items'].append(todo)
        with open(file_path, "w") as f:
            json.dump(data, f, indent=2)
        print(f"Added: {todo[0]}")

def listItems():
    """List items in the todo list based on the specified filter."""
    initialize_file()

    with open(file_path, "r") as f:
        data = json.load(f)

    filter_option = args.list[0]
    
    filtered_items = {
        "all": data['items'],
        "progress": [item for item in data['items'] if item[1] == 1],
        "todo": [item for item in data['items'] if item[1] == 0],
        "done": [item for item in data['items'] if item[1] == 2]
    }.get(filter_option, [])

    if not filtered_items:
        print("No items to display.")
    else:
        for item in filtered_items:
            status = ["Todo", "In-progress", "Done"][item[1]]
            print(f"{item[0]} - Status: {status}")

def updateItem(opt):
    """Update an existing item based on the specified option."""
    initialize_file()

    with open(file_path, "r") as f:
        data = json.load(f)

    try:
        index = int(args.update[0])
        if opt == "update":
            name = args.update[1]
            data['items'][index][0] = name
            print(f"Updated item at index {index} to '{name}'")
        elif opt == "mark_progress":
            data['items'][index][1] = 1
            print(f"Marked item at index {index} as In-progress")
        elif opt == "mark_done":
            data['items'][index][1] = 2
            print(f"Marked item at index {index} as Done")
    except (ValueError, IndexError) as e:
        print(f"ERROR: Invalid index ({e}). Please provide a valid index.")

    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)

def deleteItem():
    """Delete an item from the todo list."""
    initialize_file()

    with open(file_path, "r") as f:
        data = json.load(f)

    try:
        index = int(args.delete[0])
        removed_item = data['items'].pop(index)
        print(f"Deleted item: {removed_item[0]}")
    except (ValueError, IndexError) as e:
        print(f"ERROR: Unable to remove item ({e}). Please provide a valid index.")

    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)

def validate_add_argument(arg):
    """Validate the argument for adding a new todo item."""
    if not isinstance(arg, str) or arg.strip() == "" or arg.isdigit():
        raise ValueError("Invalid argument. Expecting a non-empty string.")

parser = argparse.ArgumentParser(
    description="A simple command-line Todo application to manage tasks.",
)

group = parser.add_mutually_exclusive_group(required=True)

group.add_argument('--add', nargs=1, type=str,
                   help='Add a new task to the todo list. Provide task name as a string.')
group.add_argument('--list', nargs=1, type=str,
                   choices=['all', 'progress', 'todo', 'done'],
                   help='List tasks based on their status. Options: all, progress, todo, done.')
group.add_argument('--update', nargs=2, type=str,
                   help='Update an existing task. Provide index and new task name.')
group.add_argument('--mark_progress', nargs=1, type=str,
                   help='Mark an existing task as in-progress. Provide index of the task.')
group.add_argument('--mark_done', nargs=1, type=str,
                   help='Mark an existing task as done. Provide index of the task.')
group.add_argument('--delete', nargs=1, type=str,
                   help='Delete an existing task. Provide index of the task.')

args = parser.parse_args()

if args.add:
    try:
        validate_add_argument(args.add[0])
        addItem()
    except ValueError as e:
        print(f"ERROR: {e}")
elif args.list:
    listItems()
elif args.update:
    updateItem("update")
elif args.mark_progress:
    updateItem("mark_progress")
elif args.mark_done:
    updateItem("mark_done")
elif args.delete:
    deleteItem()