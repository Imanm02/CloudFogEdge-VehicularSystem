class Evaluater:
    migrations_count = 0
    deadline_misses = 0
    total_tasks = 0

    @staticmethod
    def log_evaluation():
        print(f"Total migrations:\t{Evaluater.migrations_count}")
        print(f"Total deadline misses:\t{Evaluater.deadline_misses}")
        print(f"Total tasks:\t{Evaluater.total_tasks}")

        print(f"Migration ratio:\t{Evaluater.migrations_count / Evaluater.total_tasks}")
        print(f"Deadline miss ratio:\t{Evaluater.deadline_misses / Evaluater.total_tasks}")

