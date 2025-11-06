import json

file_name = "todo_list.json"

def load_task():
    try:
        with open(file_name, 'r') as file:
            data = json.load(file)
            # ✅ Ensure data format is always correct
            if "tasks" not in data or not isinstance(data["tasks"], list):
                data = {"tasks": []}
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        return {"tasks": []}

def save_tasks(data):
    try:
        with open(file_name, 'w') as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        print("Failed to save:", e)

def create_task(data):
    description = input("Enter the task description here: ").strip()
    if description:
        data["tasks"].append({"description": description, "complete": False})
        save_tasks(data)
        print("✅ Task added successfully!")
    else:
        print("⚠️ Description cannot be empty.")


def view_task(data):
    tasks = data.get("tasks", [])
    if not tasks:
        print("📭 No tasks found.")
        return

    print("\n🗒️  Your tasks:")
    for i, t in enumerate(tasks, start=1):
        # ✅ Defensive check: skip anything that's not a dict
        if not isinstance(t, dict):
            continue
        status = "[✅]" if t.get("complete") else "[ ]"
        print(f"{i}. {status} {t.get('description', '<no description>')}")

def mark_task_complete(data):
    tasks = data.get("tasks", [])
    if not tasks:
        print("📭 No tasks to complete.")
        return

    view_task(data)
    choice = input("\nEnter the task number to mark as complete (or 'c' to cancel): ").strip()
    if choice.lower() == 'c':
        print("❌ Cancelled.")
        return

    try:
        idx = int(choice) - 1
        if idx < 0 or idx >= len(tasks):
            print("⚠️ Invalid task number.")
            return
    except ValueError:
        print("⚠️ Please enter a valid number.")
        return

    if not isinstance(tasks[idx], dict):
        print("⚠️ Invalid task format, skipping.")
        return

    if tasks[idx]["complete"]:
        print("ℹ️ Task already marked as complete.")
    else:
        tasks[idx]["complete"] = True
        save_tasks(data)
        print(f"✅ Task {idx + 1} marked complete!")

def main():
    data = load_task()
    print(f"📂 Loaded {len(data.get('tasks', []))} task(s).")

    while True:
        print("\n======================")
        print("📝  To-Do Manager Menu")
        print("======================")
        print("1. View tasks")
        print("2. Add task")
        print("3. Mark task complete")
        print("4. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            view_task(data)
        elif choice == "2":
            create_task(data)
        elif choice == "3":
            mark_task_complete(data)
        elif choice == "4":
            print("👋 Goodbye! Your tasks are saved.")
            break
        else:
            print("⚠️ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
