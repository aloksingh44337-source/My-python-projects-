from datetime import datetime, timedelta

DATE_FMT = "%d-%m-%Y"
DATE_ERR = "Invalid date. Please enter the date as DD-MM-YYYY."


def parse_date(text):
    """Return a date object, or None if the format/date is invalid."""
    try:
        return datetime.strptime(text.strip(), DATE_FMT).date()
    except ValueError:
        return None


def validate_subjects(subjects):
    """Return an error message, or None if the subject list is valid."""
    if not subjects:
        return "At least one subject is required."
    seen = set()
    for s in subjects:
        key = s.lower()
        if key in seen:
            return f"Duplicate subject: {s}."
        seen.add(key)
    return None


def generate_timetable(subjects, start_date, holidays):
    """One exam per day, in order; skip Sundays and holidays."""
    schedule = []  # list of dictionaries
    current = start_date
    for subject in subjects:
        while current.weekday() == 6 or current in holidays:  # 6 = Sunday
            current += timedelta(days=1)
        schedule.append({
            "subject": subject,
            "date": current.strftime(DATE_FMT),
            "day": current.strftime("%A"),
        })
        current += timedelta(days=1)
    return schedule


def main():
    raw_subjects = input("Enter subjects (comma separated): ")
    subjects = [s.strip() for s in raw_subjects.split(",") if s.strip()]

    start_text = input("Enter start date (DD-MM-YYYY): ")
    raw_holidays = input("Enter holidays (DD-MM-YYYY, comma separated, or 'none'): ")

    # Validate start date
    start_date = parse_date(start_text)
    if start_date is None:
        print(DATE_ERR)
        return

    # Validate subjects
    error = validate_subjects(subjects)
    if error:
        print(error)
        return

    # Validate holidays
    holidays = set()
    if raw_holidays.strip() and raw_holidays.strip().lower() != "none":
        for h in raw_holidays.split(","):
            d = parse_date(h)
            if d is None:
                print(DATE_ERR)
                return
            holidays.add(d)

    for entry in generate_timetable(subjects, start_date, holidays):
        print(f"{entry['subject']} : {entry['date']} ({entry['day']})")


if __name__ == "__main__":
    main()
