from datetime import datetime, timedelta
first_date = datetime(2024, 2, 14, 14, 30, 45)
second_date = datetime(2024, 2, 16, 23, 45, 59)
sub = second_date - first_date
diff = sub.total_seconds()
print("result: ", diff)