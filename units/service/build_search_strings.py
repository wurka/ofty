# rescan all units and build search strings
# to run this script do:
# python3 manage.py shell
# >> exec(open('units/service/build_search_strings.py', encoding='utf8').read())
from units.models import Unit
from datetime import timedelta
from django.utils import timezone


print("rebuilding of search strings... please wait")
units = Unit.objects.filter(is_deleted=False)
total = len(units)
now = timezone.now()
start = timezone.now()
for index, unit in enumerate(units):
	if timezone.now() - now > timedelta(seconds=0.3) or index == total - 1:
		print(f"done: {index + 1}/{total}")
		now = timezone.now()
	unit.build_search_string()

print(f"all done in {int((timezone.utc() - start).total_seconds())} seconds")
