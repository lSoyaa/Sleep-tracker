
#  Sleep Tracker Telegram Bot

A Telegram bot developed in Python to track sleep sessions, calculate sleep duration, save personal notes, and display sleep statistics.

The project uses the **aiogram** framework for Telegram interactions and **SQLite** for storing sleep data.

##  Features

-  **Start Sleep** — Record the time when a user goes to sleep.
-  **Wake Up** — End a sleep session and calculate its duration.
-  **Add Note** — Add a personal note to the current sleep session.
-  **Statistics** — View total sessions, average, minimum, and maximum sleep duration.
-  **Last Session** — Display the most recent sleep session, including timestamps and notes.
-  **Inline Keyboard** — Navigate the bot using interactive buttons.

Sleep records are stored separately for each Telegram user.

##  Technologies

- **Python** — Main programming language
- **aiogram 3** — Asynchronous Telegram Bot framework
- **SQLite3** — Local relational database
- **asyncio** — Asynchronous event processing
- **datetime** — Time tracking and duration calculations
- **python-dotenv** — Environment variable management

##  Project Structure

```text
Sleep-tracker/
├── bot.py           # Main Telegram bot
├── db.py            # SQLite database operations
├── .env             # Bot token (not uploaded to GitHub)
├── .gitignore       # Ignored files
├── README.md        # Project documentation
└── sleep.db         # Database (created automatically)
```

##  Bot Commands

| Command | Description |
|---------|-------------|
| `/start` | Start the bot and display the main menu |
| `/sleep` | Start a sleep session |
| `/wake` | Finish the current sleep session |
| `/note` | Add a note to the sleep session |
| `/last` | Show the latest recorded sleep session |
| `/stat` | Display sleep statistics |

All main features are also accessible through inline buttons.

##  Database

The bot uses SQLite to store completed sleep sessions.

### Table: `sleep_sessions`

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Unique session identifier |
| user_id | INTEGER | Telegram user identifier |
| start_time | TEXT | Sleep start timestamp |
| end_time | TEXT | Wake-up timestamp |
| duration_minutes | INTEGER | Sleep duration in minutes |
| note | TEXT | Optional personal note |

The database supports:

- Inserting new sleep sessions
- Retrieving the latest session for a user
- Calculating statistics using SQL aggregate functions (`COUNT`, `AVG`, `MIN`, `MAX`)

##  Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/Sleep-tracker.git
cd Sleep-tracker
```

Replace `YOUR_USERNAME` with your GitHub username.

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Install dependencies

```bash
python -m pip install "aiogram>=3,<4" python-dotenv
```

### 4. Configure the bot token

Create a `.env` file in the project directory:

```env
BOT_TOKEN=your_telegram_bot_token
```

You can obtain a token from **@BotFather** on Telegram.

Never publish your real bot token.

### 5. Run the bot

On Windows:

```powershell
.\.venv\Scripts\python.exe bot.py
```

The bot will start polling for Telegram updates.

##  Example Usage

### Start a sleep session

User:
```text
/sleep
```

Bot:
```text
Sleep started
```

### Add a note

User:
```text
/note Had difficulty falling asleep
```

Bot:
```text
Note saved 📝
```

### Finish the session

User:
```text
/wake
```

Bot:
```text
Your sleep time 8h 20m ☀️
Note: Had difficulty falling asleep 📝
```

### View statistics

User:
```text
/stat
```

Example response:
```text
Statistic
Total sessions: 10
Avarage duration of sleep: 7h 35m
Minimum duration: 5h 40m
Maximum duration: 9h 15m
```

##  How It Works

1. The user starts a sleep session using a command or inline button.
2. The bot records the start time in an in-memory dictionary.
3. The user can optionally add a note.
4. When the user wakes up, the bot calculates the duration.
5. The completed session is saved in the SQLite database.
6. The user can retrieve the latest session or view overall statistics.

The bot uses asynchronous handlers to process Telegram messages and callback queries.

##  Current Limitations

- Active sleep sessions are stored in memory and are lost when the bot restarts.
- Sleep duration is calculated using the computer's local time.
- Statistics are calculated across all recorded sessions.
- The bot does not automatically detect sleep or wake-up events.
- The application is intended for personal sleep tracking, not medical diagnosis.

##  Future Improvements

- Weekly and monthly statistics
- Sleep duration charts
- Persistent storage for active sleep sessions
- Sleep reminders
- User time zone settings
- Improved error handling

##  Project Purpose

This project was created to practice Python programming and backend development.

During development, I worked with:

- Asynchronous programming
- Telegram Bot API
- SQL queries and relational databases
- User-specific data storage
- Event handlers and callback queries
- Environment variables for managing secrets

The project demonstrates the development of a small interactive application with persistent data storage and statistical calculations.
