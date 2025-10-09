from datetime import datetime, timedelta
first_date = datetime(2025, 10, 9, 10, 59, 45)
second_date = datetime(2025, 10, 10, 23, 59, 59)
sub = second_date - first_date
diff = sub.total_seconds()
print("result: ", diff)
