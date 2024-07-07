import argparse
from dotenv import load_dotenv
import logging
from src.habit_tracker import HabitTracker
from src.data_persistence import DataPersistence
import os

# Setting the logger
logger = logging.getLogger("CLI Logger")
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


class CLI:
    """ CLI class """

    @staticmethod
    def main():
        """
        Main function to run the Habit Tracker CLI.

        This function sets up the argument parser, initializes the database connection,
        and handles the different commands for interacting with the Habit Tracker.
        """

        try:
            parser = argparse.ArgumentParser(description="Habit Tracking Application")
            subparsers = parser.add_subparsers(dest="command", help="Available commands")

            # Add habit
            add_parser = subparsers.add_parser("add", help="Add a new habit")
            add_parser.add_argument("name", help="Name of the habit")
            add_parser.add_argument("description", help="Description of the habit")
            add_parser.add_argument("periodicity", choices=["daily", "weekly"], help="Periodicity of the habit")

            # Complete habit
            complete_parser = subparsers.add_parser("complete", help="Mark a habit as completed")
            complete_parser.add_argument("habit_id", type=int, help="ID of the habit to complete")

            # Analyze habits
            analyze_parser = subparsers.add_parser("analyze", help="Analyze habits")
            analyze_parser.add_argument("--list", action="store_true",
                                        help="List all currently tracked habits")
            analyze_parser.add_argument("--longest-streak", action="store_true",
                                        help="Get the longest streak for all habits")
            analyze_parser.add_argument("--habit-id", type=int,
                                        help="Get the longest streak for a specific habit")
            analyze_parser.add_argument("--daily-or-weekly", type=str,
                                        help="Get habits by periodicity [daily|weekly]")

            # Delete habit
            delete_parser = subparsers.add_parser("delete", help="Delete habit by ID")
            delete_parser.add_argument("habit_id", type=int, help="ID of the habit to be deleted")

            # Custom help command
            help_parser = subparsers.add_parser("help", help="Show help for a command")
            help_parser.add_argument("subcommand", nargs="?", help="The subcommand to show help for")

            args = parser.parse_args()

            # Initialize database connection
            db = DataPersistence(
                dbname=os.getenv("DATABASE_NAME"),
                user=os.getenv("DATABASE_USER"),
                password=os.getenv("DATABASE_PASSWORD"),
                host=os.getenv("DATABASE_HOST"),
                port=os.getenv("DATABASE_PORT")
            )
            habit_tracker = HabitTracker(db)

            if args.command == "add":
                habit = habit_tracker.add_habit(args.name, args.description, args.periodicity)
                print(f"Habit '{habit.name}' added successfully with ID {habit.id}")

            elif args.command == "complete":
                habit = habit_tracker.complete_habit(args.habit_id)
                if habit:
                    print(f"Habit '{habit.name}' marked as completed")
                else:
                    print(f"Habit with ID {args.habit_id} not found")

            elif args.command == "analyze":
                # noinspection PyTypeHints
                if args.list:
                    habits = habit_tracker.get_all_habits()
                    if habits:
                        for habit in habits:
                            print(
                                f"ID: {habit.id}, "
                                f"Name: {habit.name}, "
                                f"Periodicity: {habit.periodicity}, "
                                f"Current Streak: {habit.get_accumulated_streak()}"
                            )
                    else:
                        print("No habits found")
                elif args.longest_streak:
                    longest_streak, habit = habit_tracker.get_longest_streak_all_habits()
                    print(f"Longest streak overall: {longest_streak} (Habit: {habit.name})")
                elif args.habit_id:
                    habit = habit_tracker.get_habit_by_id(args.habit_id)
                    if habit:
                        longest_streak = habit_tracker.get_longest_streak_for_habit(habit)
                        print(f"Longest streak for '{habit.name}': {longest_streak}")
                    else:
                        print(f"Habit with ID {args.habit_id} not found")
                elif args.daily_or_weekly:
                    habits_list = habit_tracker.get_habits_by_periodicity(periodicity=args.daily_or_weekly)
                    if len(habits_list) > 0:
                        for habit in habits_list:
                            print(f"{habit.name} - {habit.periodicity} habit ")
                    else:
                        print(f"There are no habits with {args.daily_or_weekly} periodicity")
                else:
                    print("Please specify either --longest-streak or --habit-id")

            elif args.command == "delete":
                habit = habit_tracker.delete_habit(args.habit_id)
                if habit:
                    print(f"Habit '{habit.name}' deleted")
                else:
                    print(f"Habit '{habit.name}' not found")

            elif args.command == "help":
                if args.subcommand:
                    if args.subcommand in subparsers.choices:
                        subparsers.choices[args.subcommand].print_help()
                    else:
                        print(f"No help found for '{args.subcommand}'")
                else:
                    parser.print_help()

        except Exception as e:
            logger.error(f"CLI failed, {e}", exc_info=True)


if __name__ == "__main__":
    cli = CLI()
    cli.main()
