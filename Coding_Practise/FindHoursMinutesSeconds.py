# Given a nos of seconds & find hours, min & seconds
'''
1hr=60min
1 min=60 sec
1hr=60min=60*60 = 3600 secs
'''

def HrsMinSec(val):
    hrs=val//3600
    min=(val%3600) // 60
    sec=(val%3600) % 60
    print("Hrs are:",hrs)
    print("Minutes are:",min)
    print("Sec are: ",sec)

HrsMinSec(9806)

