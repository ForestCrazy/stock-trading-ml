import datetime
import time

# print(datetime.datetime.strptime("01022020", f'%d/%m/%y {"%H" if False else ""}{":%M" if False else ""}'))

date_time_str = '18/09/19 01:55'

date_time_obj = datetime.datetime.strptime(date_time_str, f'%d/%m/%y {"%H" if False else ""}{":%M" if False else ""}')


print("The type of the date is now",  type(date_time_obj))
print("The date is", date_time_obj)

"""
end_time = int(time.mktime(datetime.datetime.now().timetuple()))
print('start : ', end_time)
stop_time = 1620003022
start_time = end_time
while True:
    time_jump_step = 3600
    if end_time >= stop_time:
        break
    for t in range(1, 1000+1):
        end_time += time_jump_step
        if end_time >= stop_time:
            break

    # check_time = datetime.datetime.fromtimestamp(int(start_time)) + datetime.timedelta(minutes=60)
    # print('check_time', check_time)
    print(datetime.datetime.fromtimestamp(int(start_time)).strftime('%Y-%m-%d %H:%M:%S'), start_time)
    print(datetime.datetime.fromtimestamp(int(end_time)).strftime('%Y-%m-%d %H:%M:%S'), end_time)
    start_time = end_time + time_jump_step
"""

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