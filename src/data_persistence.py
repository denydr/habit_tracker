import os
from dotenv import load_dotenv
import logging
import psycopg2
from psycopg2 import sql
from datetime import datetime
from src.habit import Habit

# Setting the logger
logger = logging.getLogger("Data Persistence Logger")
logger.setLevel(logging.INFO)
logger_console_handler = logging.StreamHandler()
logger_console_handler.setLevel(logging.INFO)
logger_formatter = logging.Formatter(
     fmt="%(asctime)s - %(module)s - line %(lineno)d - %(levelname)s - %(message)s",
     datefmt="%Y-%m-%d %H:%M:%S"
)
logger.addHandler(logger_console_handler)

# Load environment variables from .env file
load_dotenv()


class DataPersistence:
    """
    Handles database operations for the Habit Tracker application.

    This class manages the connection to the PostgreSQL database and provides
    methods for creating, reading, updating, and deleting habits and their completions.
    """

    def __init__(
            self,
            dbname: object,
            user: object,
            password: object,
            host: object,
            port: object
    ) -> object:
        """
        Initialize the database connection.

        Args:
            dbname (str): Name of the database.
            user (str): Username for database connection.
            password (str): Password for database connection.
            host (str, optional): Database host. Defaults to 'localhost'.
            port (str, optional): Database port. Defaults to '5432'.
        """

        try:
            self.conn = psycopg2.connect(
                dbname=dbname,
                user=user,
                password=password,
                host=host,
                port=port
            )
            self.cur = self.conn.cursor()
            self.create_tables()
        except Exception as e:
            logger.error(f"Failed to connect to the database: {e}", exc_info=True)
            self.conn = None
            self.cur = None

    def create_tables(self):
        """Create the necessary tables if they don't exist."""

        if self.conn is None or self.cur is None:
            logger.error("Database connection is not established.")
            return

        try:
            self.cur.execute("""
                CREATE TABLE IF NOT EXISTS habits (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    description TEXT,
                    periodicity VARCHAR(10) NOT NULL,
                    creation_date TIMESTAMP NOT NULL,
                    is_broken BOOLEAN DEFAULT FALSE
                )
            """)
            self.cur.execute("""
                CREATE TABLE IF NOT EXISTS completions (
                    id SERIAL PRIMARY KEY,
                    habit_id INTEGER REFERENCES habits(id),
                    completion_date TIMESTAMP NOT NULL
                )
            """)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            logger.error(f"Creating tables failed, {e}", exc_info=True)

    def save_habit(self, habit):
        """
        Save a new habit to the database.

        Args:
            habit (Habit): The habit object to be saved.

        Returns:
            int: The ID of the newly saved habit.
        """

        if self.conn is None or self.cur is None:
            logger.error("Database connection is not established.")
            return

        try:
            self.cur.execute("""
                INSERT INTO habits (name, description, periodicity, creation_date)
                VALUES (%s, %s, %s, %s)
                RETURNING id
            """, (habit.name, habit.description, habit.periodicity, habit.creation_date))
            habit_id = self.cur.fetchone()[0]
            for completion_date in habit.completed_dates:
                if completion_date:
                    self.cur.execute("""
                        INSERT INTO completions (habit_id, completion_date)
                        VALUES (%s, %s)
                    """, (habit_id, completion_date))
            self.conn.commit()
            return habit_id
        except Exception as e:
            self.conn.rollback()
            logger.error(f"Save new habit to db failed, {e}", exc_info=True)

    def load_habits(self):
        """
        Load all habits from the database.

        Returns:
            list: A list of Habit objects.
        """

        if self.cur is None:
            logger.error("Database connection is not established.")
            return

        try:
            self.cur.execute("SELECT * FROM habits")
            habits = []
            for row in self.cur.fetchall():
                habit = Habit(row[1], row[2], row[3], id=row[0], creation_date=row[4])
                self.cur.execute("SELECT completion_date FROM completions WHERE habit_id = %s", (habit.id,))
                habit.completed_dates = [completion[0] for completion in self.cur.fetchall()]
                habits.append(habit)
            return habits
        except Exception as e:
            logger.error(f"Loading habits from db failed, {e}", exc_info=True)

    def update_habit(self, habit):
        """
        Update an existing habit in the database.

        Args:
            habit (Habit): The habit object to be updated.
        """

        if self.conn is None or self.cur is None:
            logger.error("Database connection is not established.")
            return

        try:
            self.cur.execute("""
                UPDATE habits
                SET name = %s, description = %s, periodicity = %s
                WHERE id = %s
            """, (habit.name, habit.description, habit.periodicity, habit.id))
            self.cur.execute("DELETE FROM completions WHERE habit_id = %s", (habit.id,))
            for completion_date in habit.completed_dates:
                self.cur.execute("""
                    INSERT INTO completions (habit_id, completion_date)
                    VALUES (%s, %s)
                """, (habit.id, completion_date))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            logger.error(f"Update existing habit in db failed, {e}", exc_info=True)

    def delete_habit(self, habit_id):
        """
        Remove a habit and its completions from the database.

        Args:
            habit_id (int): The ID of the habit to be deleted.
        """

        if self.conn is None or self.cur is None:
            logger.error("Database connection is not established.")
            return

        try:
            self.cur.execute(f"DELETE FROM completions WHERE habit_id = {habit_id}")
            self.cur.execute(f"DELETE FROM habits WHERE id = {habit_id}")
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            logger.error(f"Delete habit from db failed, {e}", exc_info=True)

    def __del__(self):
        """Close the database connection when the object is destroyed."""

        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()
