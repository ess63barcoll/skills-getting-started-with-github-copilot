# skills-getting-started-with-github-copilot
Exercise: Get started using GitHub Copilot

## Work Shift Scheduler

This repository includes a Python program that calculates work shifts for a store with the following requirements:

- **10 people** working
- **40 hours per week** per person
- **7 days a week** operation
- **Store hours**: 9 AM to 7 PM (10 hours per day)

### Features

- Automatically distributes shifts evenly across all 7 days
- Ensures each person works exactly 40 hours per week
- Limits individual work days to 8 hours maximum
- Provides rotating shift patterns for fairness
- Displays a detailed weekly schedule with hour-by-hour coverage
- Shows summary statistics including total hours and coverage

### Usage

Run the shift scheduler:

```bash
python3 shift_scheduler.py
```

### Output

The program generates:
1. A detailed weekly schedule showing which people work during each hour
2. A summary of total hours worked by each person
3. Statistics about coverage and scheduling

### Requirements

- Python 3.x (no external dependencies required)
