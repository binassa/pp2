from datetime import datetime

now = datetime.now()

drop = now.replace(microsecond=0)

print("with microseconds:", now)
print("without microseconds:", drop)