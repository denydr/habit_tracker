import argparse
from src.habit_tracker import HabitTracker
from src.data_persistence import DataPersistence

# TODO: Add error handling (try...except)
# TODO: Add help command
# TODO: Implement logging


class CLI:
    """ CLI class """

    @staticmethod
    def main():
        """
        Main function to run the Habit Tracker CLI.

        This function sets up the argument parser, initializes the database connection,
        and handles the different commands for interacting with the Habit Tracker.
        """
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

        # List habits
        list_parser = subparsers.add_parser("list", help="List all habits")  # noqa:

        # Analyze habits
        analyze_parser = subparsers.add_parser("analyze", help="Analyze habits")
        analyze_parser.add_argument("--longest-streak", action="store_true",
                                    help="Get the longest streak for all habits")
        analyze_parser.add_argument("--habit-id", type=int, help="Get the longest streak for a specific habit")

        # Delete habit
        delete_parser = subparsers.add_parser("delete", help="Delete habit by ID")
        delete_parser.add_argument("habit_id", type=int, help="ID of the habit to be deleted")

        args = parser.parse_args()

        # Initialize database connection
        db = DataPersistence(dbname="habit_tracker", user="your_username", password="your_password")
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

        elif args.command == "list":
            habits = habit_tracker.get_all_habits()
            if habits:
                for habit in habits:
                    print(
                        f"ID: {habit.id}, "
                        f"Name: {habit.name}, "
                        f"Periodicity: {habit.periodicity}, "
                        f"Current Streak: {habit.get_current_streak()}"
                    )
            else:
                print("No habits found")

        elif args.command == "analyze":
            if args.longest_streak:
                longest_streak, habit = habit_tracker.get_longest_streak_all_habits()
                print(f"Longest streak overall: {longest_streak} (Habit: {habit.name})")
            elif args.habit_id:
                habit = habit_tracker.get_habit_by_id(args.habit_id)
                if habit:
                    longest_streak = habit_tracker.get_longest_streak_for_habit(habit)
                    print(f"Longest streak for '{habit.name}': {longest_streak}")
                else:
                    print(f"Habit with ID {args.habit_id} not found")
            else:
                print("Please specify either --longest-streak or --habit-id")

        elif args.command == "delete":
            habit = habit_tracker.delete_habit(args.habit_id)
            if habit:
                print(f"Habit '{habit.name}' deleted")
            else:
                print(f"Habit '{habit.name}' not found")

if __name__ == "__main__":
    cli = CLI()
    cli.main()
