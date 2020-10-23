from itsdangerous import URLSafeSerializer
import pandas as pd
from datetime import datetime
ts= URLSafeSerializer('you-will-never-guess')

def split_time_ranges(from_time, to_time, frequency):
    '''
    this function is to separate the time available to different time slot

    args:

        from_time(datetime):start of available time

        to_time(datetime): end of available time

        frequency(int): length of meeting

    return:
        a list of time slots  
    '''
    time_range = list(pd.date_range(from_time, to_time, freq='%sS' % frequency))
    time_range=[item.time().strftime("%H:%M:%S") for item in time_range]
    time_ranges = []
    for i in range(len(time_range)-1):
        f_time = time_range[i]
        t_time = time_range[i+1]
        time_ranges.append([f_time+" "+t_time,f_time+" "+t_time])
    to_time=to_time.strftime("%H:%M:%S")
    if time_range is None:
        from_time=from_time.strftime("%H:%M:%S")
        time_ranges.append([from_time+" "+to_time,from_time+" "+to_time])
    elif to_time!=time_range[-1]:
        time_ranges.append([time_range[-1]+" "+to_time,time_range[-1]+" "+to_time])
    return time_ranges
 


def cmp(a, b):
    '''
    this function is to compare the datetime in the list

    args:

        a(appinment object):appintment a

        b(appinment object):appinment b

    return:
        the number 0,1,-1  
    '''
    a=datetime.combine(a.Date,a.start_time)
    b=datetime.combine(b.Date,b.start_time)
    if b < a:
        return 1
    if a < b:
        return -1
    return 0


