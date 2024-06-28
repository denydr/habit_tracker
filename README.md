# Habit Tracker Application

This is a command-line habit tracking application able to record, track and analyze person's habits.  

It is built with Python and is using PostgreSQL server for data persistence.  

## Project Structure  

The `habit_tracker_project` has the following structure:  

```shell
habit_tracker/
├── docs/
│   ├── build/
│   └── source/
├── src/
│   ├── __init__.py
│   ├── cli.py
│   ├── data_persistence.py
│   ├── habit.py
│   ├── habit_tracker.py
│   └── sample_data.py
├── tests/
│   ├── __init__.py
│   └── test_habit_tracker.py
├── venv/
├── .gitignore
├── README.md
└── requirements.txt
```  

## Development

- The `src` directory contains the main application code.  
- The `tests` directory contains the test suite.  
- The `docs` directory contains the Sphinx documentation files.  

where:  

- the `src folder` contains the main functionality of the application:  

    - `habit.py`: Contains the Habit class
    - `data_persistence.py`: Handles database operations
    - `habit_tracker.py`: Main logic for the habit tracker
    - `cli.py`: Command-line interface  

- the `tests folder` contains the testing functionality of the application: 

  - `test_habit_tracker.py`: Pytest tests  

## Installation

### Local Development  

1. Clone this repository:  

```shell
git clone https://github.com/denydr/habit_tracker.git
cd habit_tracker
```  

2. Install the required packages:  

```shell
pip install -r requirements.txt
```  

2. Create and activate a virtual environment:  

```shell
python -m venv venv
source venv/bin/activate  # On Windows, use venv\Scripts\activate  
```  

3. Install the required packages:  

```shell
pip install -r requirements.txt
```  

4. Set up PostgreSQL:  
- Install PostgreSQL if you haven't already:  
```shell
brew install postgresql@13 
```  
- Starting the PostgreSQL:  
```shell
brew services start postgresql@13 
```  

- Set the environment:  
```shell
# Create the .zshrc file
touch ~/.zshrc
# Open the newly created file in a text editor
vi ~/.zshrc
# Add the following lines to the file
# --------
# PostgreSQL
export PATH="/opt/homebrew/opt/postgresql@13/bin:$PATH"

# If you want to customize your prompt, you can add something like this:
# export PS1='%n@%m %1~ %# '

# Any other customizations you want can go here
# --------

# Save and exit the file
wq
# Reload the new .zshrc file
source ~/.zshrc
```

- Connecting to the PostgreSQL server:  
```shell
# Connect with the postgres user
psql -h localhost -p 5432 postgres
# Create user
CREATE USER habit_tracker WITH PASSWORD 'admin'; 
# Create the "habit_tracker" database
CREATE DATABASE habit_tracker OWNER habit_tracker;
# Grant necessary privileges to the user
GRANT ALL PRIVILEGES ON DATABASE habit_tracker TO habit_tracker;
# Exit psql
\q
# Connect to the habit_tracker database
psql -h localhost -p 5432 -U habit_tracker -d habit_tracker
```
- Optional: In order to avoid being prompted for the password do as follows:  
```shell
# Create or edit the .pgpass file
vi ~/.pgpass 
# Enter in modification mode
i --> click Enter
# Add this line
localhost:5432:habit_tracker:habit_tracker:admin
# Save and close
wq --> click Enter
# Update permissions
chmod -R 0600 ~/.pgpass
```  
 
- Update the database connection details in `src/data_persistence.py`  

## Usage  

### Local Development  

Run the application using the following command:  

```shell
python -m src.cli [command] [arguments]
```  

Available commands:

- `add`: Add a new habit  
```shell
python -m src.cli add "Habit Name" "Habit Description" [daily|weekly] 
```  
- `complete`: Mark a habit as completed  
```shell
python -m src.cli complete [habit_id] 
```  
- `list`: List all habits  
```shell
python -m src.cli list 
```  
- `analyze`: Analyze habits  
```shell
python -m src.cli analyze --longest-streak
python -m src.cli analyze --habit-id [habit_id] 
```  

- Example:  
```shell
python -m src.habit_tracker add "Exercise" "Do 30 minutes of exercise" daily
python -m src.habit_tracker complete 7
python -m src.habit_tracker list
python -m src.habit_tracker analyze --longest-streak
python -m src.habit_tracker analyze --habit-id 7
```

## Loading Sample Data  

To load sample data into the database for testing and demonstration purposes, follow these steps:

1. Ensure you have set up the PostgreSQL database as described in the Installation section.

2. Update the database credentials in the `sample_data.py` script with your actual PostgreSQL username and password.

3. Run the sample data script:

```shell
python -m src.sample_data.py
```  

After running the sample_data.py script, your database will be populated with the following sample habits:

    1. Morning Exercise (daily)
    2. Read a Book (daily)
    3. Meditate (daily)
    4. Weekly Planning (weekly)
    5. Learn a New Skill (weekly)

Each habit will have completion data for the past four weeks, with daily habits being completed every other day and weekly habits being completed once a week.
This sample data will allow users to immediately start testing the application's features, such as listing habits, analyzing streaks, and adding new completions to existing habits. It provides a realistic starting point for users to understand how the application works with actual data.

## Running Tests

To run the tests, use the following command:  

```shell
pytest tests/test_habit_tracker.py
```  

## Generating Documentation

To generate the documentation, follow these steps:

1. Navigate to the `docs` directory:  

```shell
cd docs
```  

2. Build the HTML documentation:  

```shell
make html
```  

3. Open the generated documentation in your browser:  

```shell
open build/html/index.html
```  

## Contributing

Feel free to submit issues and pull requests for new features or bug fixes.

## License

This project is licensed under the MIT License.  

