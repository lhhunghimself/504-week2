# CLI Task Manager

A simple command-line task manager built with Python. Manage your to-do list from the terminal with automatic JSON persistence.

## Quick Start

```bash
python tasks.py
```

No dependencies required—just Python 3.6+.

## Features

- **Add, view, complete, and delete tasks** via interactive menu
- **Persistent storage** in JSON format
- **Atomic saves** protect against data corruption
- **Input validation** with helpful error messages
- **Delete confirmation** prevents accidental removal

## Usage

### Interactive Menu

```
--- Task Manager ---
1. Add Task
2. View Tasks
3. Mark Task Complete
4. Delete Task
5. Exit

Enter choice (1-5):
```

### Task Display

```
Tasks (2 of 3 completed):
1. [ ] Buy groceries
2. [x] Walk the dog
3. [x] Call mom
```

### Custom Storage Location

```bash
python tasks.py --file /path/to/my_tasks.json
```

## Project Structure

```
504-week2/
├── tasks.py      # Main CLI application
├── tasks.json    # Task data (auto-created)
├── README.md     # This file
└── TECHNICAL.md  # Technical documentation
```

## Documentation

See [TECHNICAL.md](TECHNICAL.md) for architecture details, implementation notes, and development history.

## License

MIT
