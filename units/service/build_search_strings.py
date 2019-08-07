# rescan all units and build search strings
# to run this script do:
# python3 manage.py shell
# >> exec(open('units/service/build_search_strings.py', encoding='utf8').read())
from units.models import Unit
from datetime import datetime, timedelta


print("rebuilding of search strings... please wait")
units = Unit.objects.filter(is_deleted=False)
total = len(units)
now = datetime.now()
start = datetime.now()
for indx, unit in enumerate(units):
	if datetime.now() - now > timedelta(seconds=0.3) or indx == total - 1:
		print(f"done: {indx+1}/{total}")
		now = datetime.now()
	unit.build_search_string()

print(f"all done in {int((datetime.now() - start).total_seconds())} seconds")
