# to run this script do:
# python3 manage.py shell
# >> exec(open('service/load_city.py', encoding='utf8').read())
from location.models import City

print("load city: THIS script will delete ALL city data from database. Do it?")


if input("for continue print y: ").lower() == "y":
	City.objects.all().delete()

	cities = [
		{
			"name": "Москва"
		},
		{
			"name": "Вязьма"
		}
	]

	for c in cities:
		City.objects.create(name=c["name"])
		print(f"adding city {c['name']}")

	print(f"City total added: {len(cities)}")
