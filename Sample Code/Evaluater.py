class Evaluator:
    migrations_count = 0
    deadline_misses = 0
    total_tasks = 0

    @staticmethod
    def log_evaluation():
        print(f"Total migrations:\t{Evaluator.migrations_count}")
        print(f"Total deadline misses:\t{Evaluator.deadline_misses}")
        print(f"Total tasks:\t{Evaluator.total_tasks}")

        print(f"Migration ratio:\t{Evaluator.migrations_count / Evaluator.total_tasks}")
        print(f"Deadline miss ratio:\t{Evaluator.deadline_misses / Evaluator.total_tasks}")

