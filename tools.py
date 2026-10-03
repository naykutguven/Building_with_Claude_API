from datetime import datetime, timedelta
from typing import Literal

from anthropic import beta_tool

# @beta_tool is the most convenient way to define tools: it builds the tool schema
# (name, description, input_schema) from the function itself, so there is no JSON
# to write or keep in sync by hand. For that to work, each decorated function needs:
#   - type hints on every parameter (Literal[...] becomes an enum; parameters with
#     defaults become optional)
#   - a docstring: the summary becomes the tool description, and the "Args:" section
#     becomes the per-parameter descriptions the model relies on
#   - a string (or content block) return value, since that is sent back as the result
# Pass the decorated functions to client.beta.messages.tool_runner(tools=[...]),
# or call .to_dict() on one to inspect the generated schema.


@beta_tool
def get_current_datetime(date_format: str = "%Y-%m-%d %H:%M:%S") -> str:
    """Returns the current date and time as a string.

    Args:
        date_format: A strftime format string for the output.
    """
    if not date_format:
        raise ValueError("date_format cannot be empty")
    return datetime.now().strftime(date_format)


@beta_tool
def add_duration_to_datetime(
    datetime_str: str,
    duration: int = 0,
    unit: Literal[
        "seconds", "minutes", "hours", "days", "weeks", "months", "years"
    ] = "days",
    input_format: str = "%Y-%m-%d",
) -> str:
    """Adds a duration to a datetime string and returns the result in input_format.

    Args:
        datetime_str: The starting datetime, formatted as input_format.
        duration: How many units to add (negative to subtract).
        unit: The unit of time that duration is expressed in.
        input_format: strftime format used to parse and format the datetime.
    """
    date = datetime.strptime(datetime_str, input_format)

    if unit == "seconds":
        new_date = date + timedelta(seconds=duration)
    elif unit == "minutes":
        new_date = date + timedelta(minutes=duration)
    elif unit == "hours":
        new_date = date + timedelta(hours=duration)
    elif unit == "days":
        new_date = date + timedelta(days=duration)
    elif unit == "weeks":
        new_date = date + timedelta(weeks=duration)
    elif unit == "months":
        # timedelta has no months, so roll the month/year over by hand
        month = date.month - 1 + duration
        year = date.year + month // 12
        month = month % 12 + 1
        day = min(date.day, _days_in_month(year, month))
        new_date = date.replace(year=year, month=month, day=day)
    elif unit == "years":
        year = date.year + duration
        day = min(date.day, _days_in_month(year, date.month))
        new_date = date.replace(year=year, day=day)
    else:
        raise ValueError(f"Unsupported time unit: {unit}")

    return new_date.strftime(input_format)


def _days_in_month(year, month):
    # first day of the next month minus one day
    next_month = datetime(year + month // 12, month % 12 + 1, 1)
    return (next_month - timedelta(days=1)).day


@beta_tool
def set_reminder(content: str, timestamp: str) -> str:
    """Sets a reminder. Stub for the lesson: it only prints the reminder.

    Args:
        content: What to be reminded about.
        timestamp: When the reminder should fire, e.g. "2026-10-02 08:00".
    """
    print(f"Setting the following reminder for {timestamp}: {content}")
    return "Reminder set"


tools = [get_current_datetime, add_duration_to_datetime, set_reminder]


if __name__ == "__main__":
    print(get_current_datetime())
    print(add_duration_to_datetime("2026-01-31", 1, "months"))
    print(add_duration_to_datetime("2026-10-01 09:00", 90, "minutes", "%Y-%m-%d %H:%M"))
    set_reminder("Take out the trash", "2026-10-02 08:00")
    print(add_duration_to_datetime.to_dict())
