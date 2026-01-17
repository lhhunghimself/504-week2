#!/usr/bin/env python3
"""
CLI Task Manager - Add, view, complete, and delete tasks saved to JSON.
"""

import json
import sys
import argparse
from pathlib import Path


def get_tasks_file(file_path=None):
    """Get the path to the tasks JSON file."""
    if file_path:
        return Path(file_path)
    # Default: tasks.json in the same directory as this script
    return Path(__file__).parent / "tasks.json"


def load_tasks(tasks_file):
    """Load tasks from JSON file. Return empty list if missing or invalid."""
    if not tasks_file.exists():
        return []

    try:
        with open(tasks_file, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                print(f"Warning: {tasks_file} is empty. Starting fresh.")
                return []
            raw = json.loads(content)

        if not isinstance(raw, list):
            print(f"Warning: {tasks_file} is invalid (not a list). Starting fresh.")
            return []

        # Sanitize / normalize entries to avoid KeyError later
        tasks = []
        for item in raw:
            if not isinstance(item, dict):
                continue
            if "id" not in item or "title" not in item or "completed" not in item:
                continue
            try:
                task_id = int(item["id"])
            except Exception:
                continue
            title = str(item["title"]).strip()
            if not title:
                continue
            tasks.append({"id": task_id, "title": title, "completed": bool(item["completed"])})

        return tasks
    except json.JSONDecodeError:
        print(f"Warning: {tasks_file} is corrupt. Starting fresh.")
        return []
    except Exception as e:
        print(f"Warning: Error loading tasks from {tasks_file}: {e}. Starting fresh.")
        return []


def save_tasks(tasks, tasks_file):
    """Atomically save tasks to JSON file (write to .tmp, then rename)."""
    try:
        # Optional: ensure parent dir exists for --file PATH
        tasks_file.parent.mkdir(parents=True, exist_ok=True)

        tmp_file = Path(str(tasks_file) + ".tmp")
        with open(tmp_file, "w", encoding="utf-8") as f:
            json.dump(tasks, f, indent=2, ensure_ascii=False)
        # Atomic rename
        tmp_file.replace(tasks_file)
    except Exception as e:
        print(f"Error saving tasks: {e}")


def get_next_id(tasks):
    """Return the next available task ID."""
    if not tasks:
        return 1
    # Defensive: tolerate missing/invalid ids
    ids = []
    for t in tasks:
        try:
            ids.append(int(t.get("id")))
        except Exception:
            pass
    return (max(ids) + 1) if ids else 1


def add_task(tasks, tasks_file):
    """Prompt for a task title and add it to the list."""
    while True:
        title = input("Enter task title (or 'q' to cancel): ").strip()
        if title.lower() == 'q':
            return
        if not title:
            print("Task title cannot be empty. Please try again.")
            continue
        break
    
    new_task = {
        'id': get_next_id(tasks),
        'title': title,
        'completed': False
    }
    tasks.append(new_task)
    save_tasks(tasks, tasks_file)
    print(f"Task added: '{title}'")


def view_tasks(tasks):
    """Display all tasks with checkbox indicators and summary."""
    if not tasks:
        print("\nNo tasks yet!")
        return
    
    completed_count = sum(1 for t in tasks if t['completed'])
    total_count = len(tasks)
    
    print(f"\nTasks ({completed_count} of {total_count} completed):")
    for i, task in enumerate(tasks, 1):
        checkbox = "[x]" if task['completed'] else "[ ]"
        print(f"{i}. {checkbox} {task['title']}")
    print()


def mark_complete(tasks, tasks_file):
    """Select a task by list number and mark it complete."""
    if not tasks:
        print("No tasks to complete.")
        return
    
    view_tasks(tasks)
    
    while True:
        try:
            choice = input("Enter task number to mark complete (or 'q' to cancel): ").strip()
            if choice.lower() == 'q':
                return
            task_num = int(choice)
            if 1 <= task_num <= len(tasks):
                tasks[task_num - 1]['completed'] = True
                save_tasks(tasks, tasks_file)
                print(f"Task marked complete: '{tasks[task_num - 1]['title']}'")
                return
            else:
                print(f"Invalid task number. Please enter 1-{len(tasks)}.")
        except ValueError:
            print("Invalid input. Please enter a number or 'q'.")


def delete_task(tasks, tasks_file):
    """Select a task by list number and delete it with confirmation."""
    if not tasks:
        print("No tasks to delete.")
        return
    
    view_tasks(tasks)
    
    while True:
        try:
            choice = input("Enter task number to delete (or 'q' to cancel): ").strip()
            if choice.lower() == 'q':
                return
            task_num = int(choice)
            if 1 <= task_num <= len(tasks):
                task_to_delete = tasks[task_num - 1]
                confirm = input(
                    f"Delete '{task_to_delete['title']}'? (y/N): "
                ).strip().lower()
                if confirm == 'y':
                    tasks.pop(task_num - 1)
                    save_tasks(tasks, tasks_file)
                    print("Task deleted.")
                else:
                    print("Deletion cancelled.")
                return
            else:
                print(f"Invalid task number. Please enter 1-{len(tasks)}.")
        except ValueError:
            print("Invalid input. Please enter a number or 'q'.")


def main():
    """Main interactive menu loop."""
    parser = argparse.ArgumentParser(
        description="CLI Task Manager",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Tasks are stored in tasks.json (or specify --file PATH)"
    )
    parser.add_argument(
        '--file',
        type=str,
        help='Path to tasks JSON file (default: tasks.json in script directory)'
    )
    args = parser.parse_args()
    
    tasks_file = get_tasks_file(args.file)
    tasks = load_tasks(tasks_file)
    
    while True:
        print("\n--- Task Manager ---")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Mark Task Complete")
        print("4. Delete Task")
        print("5. Exit")
        print()
        
        choice = input("Enter choice (1-5): ").strip()
        
        if choice == '1':
            add_task(tasks, tasks_file)
        elif choice == '2':
            view_tasks(tasks)
        elif choice == '3':
            mark_complete(tasks, tasks_file)
        elif choice == '4':
            delete_task(tasks, tasks_file)
        elif choice == '5':
            print("Goodbye!")
            sys.exit(0)
        else:
            print("Invalid choice. Please enter 1-5.")


if __name__ == '__main__':
    main()
