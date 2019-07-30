# to run this script do:
# python3 manage.py shell
# >> exec(open('units/service/load_colors.py', encoding='utf8').read())

from units.models import Color

print("this script will delete and recreate ALL data about colors presets (Unit.Color). Continue? (y/n)?")

if input("for continue print y: ").lower() == "y":
	Color.objects.all().delete()

	# исходные данные для заполнения базы
	group_1 = [  # яркие цвета
		'23f81d', 'f465ea', 'd2cd8a', '7b4c93', 'f68592',
		'aeac64', '06d415', '221393', 'bd1426', '111f42',
		'bbef7e', 'f84c3f', '43e721', 'b8d250', '316a00',
		'd1e87a', '4b0f47', 'cbae48', '9f0134', '212b10'
	]

	group_2 = [  # тусклые цвета
		'd5d9c9', '03e3d1', 'e2d174', 'f987ac', 'da8eb9',
		'b084ca', 'a3fac0', 'fd2aab', 'ea9076', 'd65eae',
		'47ea69', '48f348', '6784e9', '9c3785', '89c74f',
		'e2692c', '9b4001', '5ac053', '87d964', '9af1a5'
	]

	group_3 = ['e8f862', 'b03d80', '88c14c', '947435', 'f2614a']  # цвета кожи скальпа

	# group_4 = [f"wood{i+1:02}" for i in range(10)]  # дерево
	group_4 = [
		"whiterdoob.jpg", "venge.jpg", "italianoreh.jpg", "redwood.jpg",
		"naturaldoob.jpg", "palicandr.jpg", "whiteoreh.jpg", "darkdoob.jpg", "clearwood.jpg"
	]

	# group_5 = [f"metal{i+1:02}" for i in range(10)]  # металл
	group_5 = [
		"bronze.jpg", "gold.jpg", "krak.jpg", "craft.jpg", "coper.jpg",
		"patina.jpg", "rust.jpg", "silver.jpg", "oldgold.jpg", "hz.jpg"
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