from datetime import datetime, timedelta

current = datetime.now().date()
new = current - timedelta(days=5)

print("Current date:", current)
print("Date 5 days ago:", new)