from units.models import Group

print("THIS script will delete ALL data from database. Do it?")

Group.objects.create(name="vazes")
print("all done")
