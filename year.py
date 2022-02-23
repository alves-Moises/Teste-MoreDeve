def is_leap(year):
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

def days_in_month(year_c, month_c):
  return ([31, 29 if is_leap(year_c) == True else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31])[month_c - 1]
  