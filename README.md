# Board Game Tracker

A Python and MySQL command-line project by Jarrell Warren, adapted from a university assignment.

## Features

- Add board game records, player limits, results, and scores
- View saved records
- Delete records by game name with confirmation
- Parameterized SQL queries and basic input validation
- Database settings from environment variables, with a hidden password prompt

## Setup

Requires Python 3.9+ and a running MySQL server. Create a new database named `board_game_tracker` and a MySQL account with CREATE, SELECT, INSERT, and DELETE permissions on that database. This project creates the table automatically; it does not create the database or account.

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export DB_HOST=localhost
export DB_USER=boardgame_user
export DB_NAME=board_game_tracker
export DB_PORT=3306
python3 board_game_tracker.py
```

On Windows PowerShell, activate with `.venv\Scripts\Activate.ps1` and set variables using `$env:DB_USER="boardgame_user"` (and the same pattern for other settings).

Enter your database password when prompted. Alternatively set `DB_PASSWORD` in the process environment. Never commit passwords. A `.env` file is not automatically loaded.

## Menu

| Option | Action |
| --- | --- |
| o | Output saved records |
| a | Add a record |
| d | Delete all records with the specified game name, after confirmation |
| q | Quit |

## Database fields

The `boardgame` table stores an auto-increment ID, game name (20 characters), maximum players, result (50 characters), maximum score, and timestamps. The original `gameduration` column is retained for assignment compatibility: it stores the time the record was entered, **not elapsed play time**. `created` is assigned by MySQL.

Use a fresh database for this demo. Existing tables are not migrated automatically.

## Project structure

- `board_game_tracker.py`: connection, table creation, and interactive menu
- `requirements.txt`: MySQL connector dependency
- `.gitignore`: excludes local environments and configuration

## Validation

Python syntax and input-validation paths were checked locally. Live MySQL integration was not tested in the preparation environment.
