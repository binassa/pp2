from datetime import datetime

date1_str = input("YYYY-MM-DD HH:MM:SS: ")
date2_str = input("YYYY-MM-DD HH:MM:SS: ")

date1 = datetime.strptime(date1_str, "%Y-%m-%d %H:%M:%S")
date2 = datetime.strptime(date2_str, "%Y-%m-%d %H:%M:%S")

diff = date2 - date1
seconds = diff.total_seconds()

print(seconds)