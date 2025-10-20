#!/usr/bin/env python3
"""
Work Shift Scheduler
Calculates work shifts for 7 days a week with 10 people.
Each person works 40 hours per week.
Store hours: 9 AM to 7 PM (10 hours per day)
"""

from datetime import datetime, timedelta
import random

# Configuration
NUM_PEOPLE = 10
HOURS_PER_PERSON = 40
DAYS_IN_WEEK = 7
STORE_OPEN_HOUR = 9  # 9 AM
STORE_CLOSE_HOUR = 19  # 7 PM
HOURS_PER_DAY = STORE_CLOSE_HOUR - STORE_OPEN_HOUR

# Days of the week
DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# People names
PEOPLE = [f'Person {i+1}' for i in range(NUM_PEOPLE)]


def calculate_shifts():
    """
    Calculate work shifts for the week.
    
    Strategy:
    - Each person works 40 hours per week
    - Distribute shifts evenly across 7 days (approximately 5.7 hours per day)
    - Each shift is assigned to cover store hours (9 AM - 7 PM)
    - Rotate people through different time slots for fairness
    """
    
    # Initialize schedule: {day: {hour: [people]}}
    schedule = {day: {hour: [] for hour in range(STORE_OPEN_HOUR, STORE_CLOSE_HOUR)} 
                for day in DAYS}
    
    # Track hours worked by each person per day
    hours_worked = {person: 0 for person in PEOPLE}
    daily_hours = {person: {day: 0 for day in DAYS} for person in PEOPLE}
    
    # Target hours per person per day (40 hours / 7 days ≈ 5.7)
    # We'll aim for 5-6 hours per day per person
    target_hours_per_day = HOURS_PER_PERSON / DAYS_IN_WEEK
    
    # For each time slot, assign workers in a rotating pattern
    person_offset = 0
    
    for day in DAYS:
        for hour in range(STORE_OPEN_HOUR, STORE_CLOSE_HOUR):
            # Determine how many people to assign to this hour
            # We want good coverage, so let's assign multiple people
            workers_this_hour = []
            
            for i in range(NUM_PEOPLE):
                person_idx = (person_offset + i) % NUM_PEOPLE
                person = PEOPLE[person_idx]
                
                # Check if this person can work this hour
                can_work = (
                    hours_worked[person] < HOURS_PER_PERSON and
                    daily_hours[person][day] < 8  # Max 8 hours per day
                )
                
                if can_work:
                    # Check if we should assign this person based on target hours
                    # Try to keep people close to their target hours per day
                    if daily_hours[person][day] < target_hours_per_day + 1:
                        workers_this_hour.append(person)
                        hours_worked[person] += 1
                        daily_hours[person][day] += 1
                        
                        # We want about 5-6 workers per hour for good coverage
                        if len(workers_this_hour) >= 6:
                            break
            
            schedule[day][hour] = workers_this_hour
            person_offset += 1  # Rotate starting person for next hour
    
    # Second pass: fill in remaining hours for people who haven't reached 40 hours
    for person in PEOPLE:
        while hours_worked[person] < HOURS_PER_PERSON:
            # Find a slot where this person can work
            assigned = False
            for day in DAYS:
                if assigned:
                    break
                if daily_hours[person][day] >= 8:
                    continue
                    
                for hour in range(STORE_OPEN_HOUR, STORE_CLOSE_HOUR):
                    if person not in schedule[day][hour]:
                        schedule[day][hour].append(person)
                        hours_worked[person] += 1
                        daily_hours[person][day] += 1
                        assigned = True
                        break
            
            # If we couldn't find a slot, we need to break to avoid infinite loop
            if not assigned:
                break
    
    return schedule, hours_worked


def print_schedule(schedule, hours_worked):
    """Print the weekly schedule in a readable format."""
    
    print("\n" + "="*80)
    print("WEEKLY WORK SHIFT SCHEDULE")
    print("="*80)
    print(f"Store Hours: {STORE_OPEN_HOUR}:00 AM - {STORE_CLOSE_HOUR-12}:00 PM")
    print(f"Total People: {NUM_PEOPLE}")
    print(f"Hours per Person: {HOURS_PER_PERSON}")
    print("="*80 + "\n")
    
    # Print schedule by day
    for day in DAYS:
        print(f"\n{day.upper()}")
        print("-" * 80)
        
        for hour in range(STORE_OPEN_HOUR, STORE_CLOSE_HOUR):
            # Format hour
            if hour < 12:
                time_str = f"{hour}:00 AM"
            elif hour == 12:
                time_str = "12:00 PM"
            else:
                time_str = f"{hour-12}:00 PM"
            
            # Get people working this hour
            workers = schedule[day][hour]
            if workers:
                workers_str = ", ".join(workers)
            else:
                workers_str = "No one scheduled"
            
            print(f"  {time_str:10} | {workers_str}")
    
    # Print summary of hours worked
    print("\n" + "="*80)
    print("HOURS WORKED SUMMARY")
    print("="*80)
    
    for person in PEOPLE:
        hours = hours_worked[person]
        print(f"  {person:12} | {hours:2} hours")
    
    # Calculate total coverage
    total_hours_scheduled = sum(hours_worked.values())
    total_store_hours = DAYS_IN_WEEK * HOURS_PER_DAY
    
    print("\n" + "="*80)
    print("STATISTICS")
    print("="*80)
    print(f"  Total hours scheduled: {total_hours_scheduled}")
    print(f"  Total store hours per week: {total_store_hours}")
    print(f"  Average coverage per hour: {total_hours_scheduled / total_store_hours:.2f} people")
    print("="*80 + "\n")


def main():
    """Main function to run the shift scheduler."""
    print("\nGenerating work shift schedule...\n")
    
    schedule, hours_worked = calculate_shifts()
    print_schedule(schedule, hours_worked)
    
    # Verify all people have 40 hours
    all_correct = all(hours == HOURS_PER_PERSON for hours in hours_worked.values())
    
    if all_correct:
        print("✓ Success! All people have exactly 40 hours assigned.")
    else:
        print("⚠ Warning: Not all people have exactly 40 hours assigned.")
        for person, hours in hours_worked.items():
            if hours != HOURS_PER_PERSON:
                print(f"  {person}: {hours} hours (expected {HOURS_PER_PERSON})")


if __name__ == "__main__":
    main()
