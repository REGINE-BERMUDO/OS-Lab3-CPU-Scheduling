# EARLIEST DEADLINE FIRST (EDF)
# Preemptive dynamic-priority scheduling

tasks = [
    {"id": "T1", "C": 1, "T": 4, "D": 4},
    {"id": "T2", "C": 1, "T": 5, "D": 5},
    {"id": "T3", "C": 2, "T": 10, "D": 10}
]

SIMULATION_TIME = 20

jobs = []
gantt = []

def add_segment(pid, start, end):
    if gantt and gantt[-1][0] == pid and gantt[-1][2] == start:
        gantt[-1] = (pid, gantt[-1][1], end)
    else:
        gantt.append((pid, start, end))

# Generate periodic task instances
for task in tasks:
    release = 0
    while release < SIMULATION_TIME:
        jobs.append({
            "id": task["id"],
            "release": release,
            "deadline": release + task["D"],
            "remaining": task["C"],
            "completion": None
        })
        release += task["T"]

# Simulate the processor in 1 ms intervals
for time in range(SIMULATION_TIME):
    ready = [
        job for job in jobs
        if job["release"] <= time
        and job["remaining"] > 0
        and job["deadline"] > time
    ]

    if ready:
        # Earliest absolute deadline has highest priority
        running = min(
            ready,
            key=lambda j: (
                j["deadline"],
                j["release"],
                j["id"]
            )
        )
        add_segment(running["id"], time, time + 1)
        running["remaining"] -= 1

        if running["remaining"] == 0:
            running["completion"] = time + 1
    else:
        add_segment("IDLE", time, time + 1)

# Determine deadline status at the simulation horizon
for job in jobs:
    job["status"] = (
        "MET" if job["completion"] is not None
        and job["completion"] <= job["deadline"]
        else "MISSED" if job["deadline"] <= SIMULATION_TIME
        else "PENDING"
    )

utilization = sum(task["C"] / task["T"] for task in tasks)

print("\nEARLIEST DEADLINE FIRST SCHEDULING")
print("\nCPU Utilization:", round(utilization * 100, 2), "%")
print("Classical EDF Utilization Test:",
      "PASS" if utilization <= 1 else "NOT PASSED")

print("\nGANTT CHART")
for pid, start, end in gantt:
    print(f"| {pid} [{start}-{end}] ", end="")
print("|")

print("\nTASK INSTANCE RESULTS")
print("Task\tRelease\tDeadline\tCompletion\tStatus")

misses = 0
for job in sorted(jobs, key=lambda j: (j["release"], j["id"])):
    if job["status"] == "MISSED":
        misses += 1
    completion = job["completion"] if job["completion"] is not None else "-"
    print(f'{job["id"]}\t{job["release"]}\t{job["deadline"]}\t'
          f'{completion}\t\t{job["status"]}')

print("\nDeadline Misses:", misses)
