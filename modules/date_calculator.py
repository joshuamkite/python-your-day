

import os
import sys


def is_leap_year(year):
    # This function should return True if the given year is a leap year
    # Otherwise, it should return False
    # A leap year is a multiple of 4, but not a multiple of 100
    # However, a leap year is a multiple of 400
    if year % 4 == 0:
        if year % 100 == 0:
            if year % 400 == 0:
                return True
            else:
                return False
        else:
            return True
    else:
        return False


def month_code(month, year):
    # This function should return the month code for the given month and year

    month_code_always = {
        0: 0,
        3: 4,
        4: 0,
        5: 2,
        6: 5,
        7: 0,
        8: 3,
        9: 6,
        10: 1,
        11: 4,
        12: 6,
    }

    month_code_leap = {
        1: 0,
        2: 3,
    }

    month_code_normal = {
        1: 1,
        2: 4,
    }

   # check for leap year
    if is_leap_year(year):
        month_code_always.update(month_code_leap)
    else:
        month_code_always.update(month_code_normal)

    return month_code_always[month]


def get_day_of_week(date):
    # This function should return the day of the week for the given date
    # The date will be in the format 'YYYY-MM-DD'
    # The returned value should be a string, e.g. 'Monday'
    # get the year, month, and day from the date
    year, month, day = date.split('-')
    # convert the year, month, and day to integers
    year = int(year)
    month = int(month)
    day = int(day)

    if year < 1754:
        print("The date provided is before the Gregorian calendar was adopted")
        os.sys.exit(1)

    # get last two digits of the year
    last_two_digits = year % 100
    # get 1/4 of sum of these digits
    running_value = last_two_digits // 4
    running_value += last_two_digits
    # add the day of the month
    running_value += day
    # add the month code

    running_value += month_code(month, year)

    century = year // 100
    century_code = (3 - (century % 4)) * 2
    running_value += century_code

    weekday = running_value % 7
    # get the day of the week
    days = {
        0: "Saturday",
        1: "Sunday",
        2: "Monday",
        3: "Tuesday",
        4: "Wednesday",
        5: "Thursday",
        6: "Friday"
    }

    return days[weekday]
