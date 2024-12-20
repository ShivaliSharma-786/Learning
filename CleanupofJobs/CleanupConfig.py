import datetime
current_date=(datetime.datetime.now()-datetime.timedelta(0)).strftime('%Y-%m-%d')
Jobname="cleanupexpiredsubscribers"
LogString=rf"{current_date} .* INFO  c\.o\.h\.m\.a\.impl\.HousekeepingTaskImpl -  - Completed housekeeping task Expired subscriber housekeepping task - Deleted (\d+) expired subscribers\."
