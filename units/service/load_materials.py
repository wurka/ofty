# to run this script do:
# python3 manage.py shell
# >> exec(open('units/service/load_materials.py', encoding='utf8').read())

from units.models import Material

print("LOAD MATERIALS: this script will delete and recreate ALL data about materials (Unit.Material) Continue? (y/n)?")

if input("for continue print y: ").lower() == "y":
	Material.objects.all().delete()

	materials = [
		"гавно", "палки", "прана", "масло конопляное", "живица", "волшебные бобы",
		"надежда", "астральные кирпичи"
	]

	for m in materials:
		Material.objects.create(name=m)
