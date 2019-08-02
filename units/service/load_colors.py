# to run this script do:
# python3 manage.py shell
# >> exec(open('units/service/load_colors.py', encoding='utf8').read())

from units.models import Color

print("LOAD COLORS: this script will delete and recreate ALL data about colors presets (Unit.Color). Continue? (y/n)?")

if input("for continue print y: ").lower() == "y":
	Color.objects.all().delete()

	# исходные данные для заполнения базы
	group_1 = [  # яркие цвета
		'FF0600', 'FF0063', 'DA00FF', '6400FF', '0025FF',
		'0057FF', '00A4FF', '0ADEEC', '00F4AB', '00D622',
		'89F900', 'CDEA00', 'FFEB00', 'FFB900', 'FF8700',
		'F85900', '75554A', '9C9C9C', '677077', '000000'
	]

	group_2 = [  # тусклые цвета
		'FFB5B3', 'FFB3D1', 'F4B3FF', 'D1B3FF', 'B3BEFF',
		'B3CDFF', 'B3E4FF', 'B6F6FA', 'B3FCE6', 'B3F3BD',
		'DCFEB3', 'F0F9B3', 'FFFAB3', 'FFEBB3', 'FFDCB3',
		'FDCEB3', 'D6CCC9', 'E2E2E2', 'D2D5D7', 'FFFFFF'
	]

	group_3 = ['F2EADD', 'F7E3CB', 'FFF3DB', 'FFF9E7', 'FFF4F3']  # цвета кожи скальпа

	# group_4 = [f"wood{i+1:02}" for i in range(10)]  # дерево
	group_4 = [
		"whiterdoob.jpg", "clearwood.jpg", "naturaldoob.jpg", "whiteoreh.jpg", "italianoreh.jpg",
		"redwood.jpg", "palicandr.jpg", "darkdoob.jpg", "venge.jpg", "craft.jpg"
	]

	# group_5 = [f"metal{i+1:02}" for i in range(10)]  # металл
	group_5 = [
		"silver.jpg", "gold.jpg", "krak.jpg", "coper.jpg", "rust.jpg",
		"hz.jpg", "oldgold.jpg", "krak.jpg", "patina.jpg", "glas.jpg"
	]

	for g in group_1:
		Color.objects.create(
			color_group="group1",
			rgb_hex=g,
			texture=""
		)
	for g in group_2:
		Color.objects.create(
			color_group="group2",
			rgb_hex=g,
			texture=""
		)
	for g in group_3:
		Color.objects.create(
			color_group="group3",
			rgb_hex=g,
			texture=""
		)
	for g in group_4:
		Color.objects.create(
			color_group="group4",
			rgb_hex="",
			texture=g
		)
	for g in group_5:
		Color.objects.create(
			color_group="group5",
			rgb_hex=g,
			texture=g
		)