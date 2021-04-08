import datetime
import time



"""
import datetime
import time

first_time = datetime.datetime.now()
time.sleep(2)
later_time = datetime.datetime.now()
difference = later_time - first_time
seconds_in_day = 24 * 60 * 60

print(divmod(difference.days * seconds_in_day + difference.seconds, 60))
"""

"""
from datetime import date, timedelta

sdate = date(2008, 8, 15)   # start date
edate = date(2008, 9, 15)   # end date

delta = edate - sdate       # as timedelta

for i in range((delta.seconds)/3600 + 1):
    print(i)
    day = sdate + timedelta(seconds=i)
    print(day)
"""