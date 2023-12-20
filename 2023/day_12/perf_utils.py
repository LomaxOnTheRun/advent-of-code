import time


LOG_TIME_NS = {}
LOG_COUNTS = {}


def timeit(method):
    def timed(*args, **kwargs):
        start_time = time.perf_counter_ns()
        result = method(*args, **kwargs)
        end_time = time.perf_counter_ns()

        name = method.__name__
        if name not in LOG_TIME_NS:
            LOG_TIME_NS[name] = 0
        LOG_TIME_NS[name] += end_time - start_time

        if name not in LOG_COUNTS:
            LOG_COUNTS[name] = 0
        LOG_COUNTS[name] += 1

        return result

    return timed


def print_logged_times():
    """
    Show how long each function has taken to run.
    """
    sorted_times = reversed(sorted(LOG_TIME_NS.items(), key=lambda kv: kv[1]))
    print("\nFunction run times (ns):\n")
    for name, time_in_ns in sorted_times:
        time_in_seconds = time_in_ns / 1e9
        count = LOG_COUNTS[name]
        per_call = f"{(time_in_ns / count):.2f}"
        time_space = 9 - len(str(time_in_seconds))
        count_space = 8 - len(str(count))
        avg_time_space = 13 - len(str(per_call))
        print(
            f"{time_in_seconds:.2f} s{' ' * time_space} x {count}{' ' * count_space} "
            f"(avg: {per_call} ns){' ' * avg_time_space}{name}"
        )
