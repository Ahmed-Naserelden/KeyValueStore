# Key-Value Store

A command-line based key-value store implementation with namespace and table support, persistence, and compaction features.

## Features

- Namespace and table management
- CRUD operations (Create, Read, Update, Delete)
- Data persistence with flush operations
- Table compaction
- Interactive command-line interface
- TTL (Time To Live) support for key-value pairs

## Requirements

- Python 3.9 or higher

## Installation

1. Clone the repository
2. Navigate to the project directory
3. Run `python3 cli.py`

## Usage

The key-value store provides an interactive shell with the following commands:

### Namespace Management
- `create-namespace <namespace>` - Create a new namespace
- `use-namespace <namespace>` - Switch to a namespace
- `list-namespaces` - List all available namespaces

### Table Management
- `create-table <table>` - Create a new table in current namespace
- `list-tables` - List all tables in current namespace

### Data Operations
- `set <table>:<key>:<value> [ttl]` - Set a key-value pair (optional TTL)
- `get <table>:<key>` - Retrieve a value by key
- `delete <table>:<key>` - Delete a key-value pair
- `flush <table>` - Flush table data to disk
- `compact <table>` - Compact table files

### Example Session

```bash
kvstore> create-namespace iti
[OK] Created namespace: iti

kvstore> use-namespace iti
[OK] Using namespace: iti

kvstore> create-table collaborators
[OK] Created table: iti:collaborators

kvstore> set collaborators:collaborator1:sief
[OK] Set collaborator1 in iti:collaborators

kvstore> get collaborators:collaborator1
[HIT] iti:collaborators:collaborator1 = sief

kvstore> flush collaborators
[OK] Flushed iti:collaborators to disk.
```

## Project Structure

```
key_value_store/
├── cli.py              # Command-line interface
├── kvstore/           # Core implementation
│   ├── engine.py      # Main storage engine
│   ├── store/         # Storage implementation
│   └── wal.py         # Write-ahead logging
└── testcases.txt      # Example usage scenarios
```

## Commands Reference

- `exit` - Exit the interactive shell
- `create-namespace <namespace>` - Create a new namespace
- `use-namespace <namespace>` - Switch to a namespace
- `list-namespaces` - List all namespaces
- `create-table <table>` - Create a new table
- `list-tables` - List all tables in current namespace
- `set <table>:<key>:<value> [ttl]` - Set a key-value pair
- `get <table>:<key>` - Get a value by key
- `delete <table>:<key>` - Delete a key-value pair
- `flush <table>` - Flush table to disk
- `compact <table>` - Compact table files

