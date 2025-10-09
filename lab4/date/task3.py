from datetime import datetime
current_date = datetime.now()
date = current_date.replace(microsecond=0)
print("Current date: " , current_date)
print("Current date without microsecond: ", date)