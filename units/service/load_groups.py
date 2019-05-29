# to run this script do:
# python3 manage.py shell
# >> exec(open('units/service/load_groups.py', encoding='utf8').read())

from units.models import Group, GroupParameter

print("THIS script will delete ALL data from database. Do it?")


if input("for continue print y: ") == "y":
	Group.objects.all().delete()

	arki = Group.objects.create(name='Арки')

	anfilada = Group.objects.create(name='Анфилада', picture='arki_anfilada.png', parent=arki)
	GroupParameter.objects.create(owner=anfilada, name='А', dimension='см')
	GroupParameter.objects.create(owner=anfilada, name='H', dimension='см')

	serdce = Group.objects.create(name='Сердце', picture='arki_anfilada.png', parent=arki)
	GroupParameter.objects.create(owner=serdce, name='А', dimension='см')
	GroupParameter.objects.create(owner=serdce, name='H', dimension='см')

	arki_chetyre = Group.objects.create(name="Четырехугольные", picture="arki_chetirehugolnie.png", parent=arki)
	GroupParameter.objects.create(owner=arki_chetyre, name='А', dimension='см')
	GroupParameter.objects.create(owner=arki_chetyre, name='H', dimension='см')

	arki_duga = Group.objects.create(name="Дуга", picture="arki_chetirehugolnie.png", parent=arki)
	GroupParameter.objects.create(owner=arki_duga, name='А', dimension='см')
	GroupParameter.objects.create(owner=arki_duga, name='B', dimension='см')
	GroupParameter.objects.create(owner=arki_duga, name='H', dimension='см')

	arki_kruglye = Group.objects.create(name="Круглые", picture="arki_kruglie.png", parent=arki)
	GroupParameter.objects.create(owner=arki_chetyre, name='А', dimension='см')
	GroupParameter.objects.create(owner=arki_chetyre, name='H', dimension='см')
