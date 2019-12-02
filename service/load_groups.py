# to run this script do:
# python3 manage.py shell
# >> exec(open('service/load_groups.py', encoding='utf8').read())

from units.models import Group, GroupParameter

print("LOAD GROUPS: THIS script will delete ALL data from database. Do it?")


if input("for continue print y: ").lower() == "y":
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

	arki_p = Group.objects.create(name="П-образные", picture="arki_P_obraznie.png", parent=arki)
	GroupParameter.objects.create(owner=arki_p, name='А', dimension='см')
	GroupParameter.objects.create(owner=arki_p, name='B', dimension='см')
	GroupParameter.objects.create(owner=arki_p, name='H', dimension='см')

	arki_pk = Group.objects.create(name="Полукруглые", picture="arki_polukruglie.png", parent=arki)
	GroupParameter.objects.create(owner=arki_pk, name='А', dimension='см')
	GroupParameter.objects.create(owner=arki_pk, name='B', dimension='см')
	GroupParameter.objects.create(owner=arki_pk, name='H', dimension='см')

	gamakishizlongi = Group.objects.create(name='Гамаки и шизлонги')

	gamakishizlongi_gamaki = Group.objects.create(name="Гамаки", picture="gamaki_i_shezlongi_gamaki.png", parent=gamakishizlongi)
	GroupParameter.objects.create(owner=gamakishizlongi_gamaki, name='А', dimension='см')
	GroupParameter.objects.create(owner=gamakishizlongi_gamaki, name='B', dimension='см')

	gamakishizlongi_shizlongi = Group.objects.create(name="Шезлонги", picture="gamaki_i_shezlongi_shezlongi .png", parent=arki)
	GroupParameter.objects.create(owner=gamakishizlongi_shizlongi, name='А', dimension='см')
	GroupParameter.objects.create(owner=gamakishizlongi_shizlongi, name='B', dimension='см')
	GroupParameter.objects.create(owner=gamakishizlongi_shizlongi, name='H', dimension='см')

	mebel = Group.objects.create(name='Мебель')

	mebel_divany = Group.objects.create(name="Диваны", parent=mebel)

	mebel_divany_kanape = Group.objects.create(name="Канапе", picture="mebel_divani_kanape.png", parent=mebel_divany)
	GroupParameter.objects.create(owner=mebel_divany_kanape, name='А', dimension='см')
	GroupParameter.objects.create(owner=mebel_divany_kanape, name='B', dimension='см')
	GroupParameter.objects.create(owner=mebel_divany_kanape, name='H', dimension='см')

	mebel_divany_kozetki = Group.objects.create(name="Козетки", picture="mebel_divani_kozetki.png", parent=mebel_divany)
	GroupParameter.objects.create(owner=mebel_divany_kozetki, name='А', dimension='см')
	GroupParameter.objects.create(owner=mebel_divany_kozetki, name='B', dimension='см')
	GroupParameter.objects.create(owner=mebel_divany_kozetki, name='H', dimension='см')

	mebel_divany_kushetki = Group.objects.create(name="Кушетки", picture="mebel_divani_kushetki.png", parent=mebel_divany)
	GroupParameter.objects.create(owner=mebel_divany_kushetki, name='А', dimension='см')
	GroupParameter.objects.create(owner=mebel_divany_kushetki, name='B', dimension='см')
	GroupParameter.objects.create(owner=mebel_divany_kushetki, name='H', dimension='см')

	mebel_divany_otto = Group.objects.create(name="Оттоманки", picture="mebel_divani_ottomanki.png", parent=mebel_divany)
	GroupParameter.objects.create(owner=mebel_divany_otto, name='А', dimension='см')
	GroupParameter.objects.create(owner=mebel_divany_otto, name='B', dimension='см')
	GroupParameter.objects.create(owner=mebel_divany_otto, name='H', dimension='см')

	mebel_divany_sophy = Group.objects.create(
		name="Софы", picture="mebel_divani_sofi.png", parent=mebel_divany)
	GroupParameter.objects.create(owner=mebel_divany_sophy, name='А', dimension='см')
	GroupParameter.objects.create(owner=mebel_divany_sophy, name='B', dimension='см')
	GroupParameter.objects.create(owner=mebel_divany_sophy, name='H', dimension='см')

	mebel_divany_tahty = Group.objects.create(
		name="Тахты", picture="mebel_divani_tahti.png", parent=mebel_divany)
	GroupParameter.objects.create(owner=mebel_divany_tahty, name='А', dimension='см')
	GroupParameter.objects.create(owner=mebel_divany_tahty, name='B', dimension='см')
	GroupParameter.objects.create(owner=mebel_divany_tahty, name='H', dimension='см')

	mebel_kaminy = Group.objects.create(name="Камины", parent=mebel)

	mebel_kaminy_electro = Group.objects.create(
		name="Электрические", picture="mebel_kamini_elekricheskie.png", parent=mebel_kaminy)
	GroupParameter.objects.create(owner=mebel_kaminy_electro, name='А', dimension='см')
	GroupParameter.objects.create(owner=mebel_kaminy_electro, name='B', dimension='см')
	GroupParameter.objects.create(owner=mebel_kaminy_electro, name='H', dimension='см')

	mebel_kresla = Group.objects.create(name="Кресла", parent=mebel)

	mebel_kresla_berzher = Group.objects.create(
		name="Бержер", picture="mebel_kresla_berger.png", parent=mebel_kresla)
	GroupParameter.objects.create(owner=mebel_kresla_berzher, name='А', dimension='см')
	GroupParameter.objects.create(owner=mebel_kresla_berzher, name='B', dimension='см')
	GroupParameter.objects.create(owner=mebel_kresla_berzher, name='H', dimension='см')

	mebel_kresla_berzher_pom = Group.objects.create(
		name="Бержер Помпиду", picture="mebel_kresla_berger_pompidu.png", parent=mebel_kresla)
	GroupParameter.objects.create(owner=mebel_kresla_berzher_pom, name='А', dimension='см')
	GroupParameter.objects.create(owner=mebel_kresla_berzher_pom, name='B', dimension='см')
	GroupParameter.objects.create(owner=mebel_kresla_berzher_pom, name='H', dimension='см')

	mebel_kresla_chester = Group.objects.create(
		name="Честерфилд", picture="mebel_kresla_chesterfild.png", parent=mebel_kresla)
	GroupParameter.objects.create(owner=mebel_kresla_chester, name='А', dimension='см')
	GroupParameter.objects.create(owner=mebel_kresla_chester, name='B', dimension='см')
	GroupParameter.objects.create(owner=mebel_kresla_chester, name='H', dimension='см')

	mebel_kresla_cabrio = Group.objects.create(
		name="Кабриоль", picture="mebel_kresla_kabriol.png", parent=mebel_kresla)
	GroupParameter.objects.create(owner=mebel_kresla_cabrio, name='А', dimension='см')
	GroupParameter.objects.create(owner=mebel_kresla_cabrio, name='B', dimension='см')
	GroupParameter.objects.create(owner=mebel_kresla_cabrio, name='H', dimension='см')

	mebel_kresla_cach = Group.objects.create(
		name="Качалки", picture="mebel_kresla_kachalki.png", parent=mebel_kresla)
	GroupParameter.objects.create(owner=mebel_kresla_cach, name='А', dimension='см')
	GroupParameter.objects.create(owner=mebel_kresla_cach, name='B', dimension='см')
	GroupParameter.objects.create(owner=mebel_kresla_cach, name='H', dimension='см')

	mebel_kresla_cacheli = Group.objects.create(
		name="Качели", picture="mebel_kresla_kacheli.png", parent=mebel_kresla)
	GroupParameter.objects.create(owner=mebel_kresla_cacheli, name='h', dimension='см')
	GroupParameter.objects.create(owner=mebel_kresla_cacheli, name='H', dimension='см')

	mebel_kresla_comp = Group.objects.create(
		name="Компьютерные", picture="mebel_kresla_komputernie.png", parent=mebel_kresla)
	GroupParameter.objects.create(owner=mebel_kresla_comp, name='А', dimension='см')
	GroupParameter.objects.create(owner=mebel_kresla_comp, name='B', dimension='см')
	GroupParameter.objects.create(owner=mebel_kresla_comp, name='H', dimension='см')

	mebel_kresla_krapo = Group.objects.create(
		name="Крапо", picture="mebel_kresla_krapo.png", parent=mebel_kresla)
	GroupParameter.objects.create(owner=mebel_kresla_krapo, name='А', dimension='см')
	GroupParameter.objects.create(owner=mebel_kresla_krapo, name='B', dimension='см')
	GroupParameter.objects.create(owner=mebel_kresla_krapo, name='H', dimension='см')

	mebel_kresla_markiz = Group.objects.create(
		name="Маркиз", picture="mebel_kresla_markiz.png", parent=mebel_kresla)
	GroupParameter.objects.create(owner=mebel_kresla_markiz, name='А', dimension='см')
	GroupParameter.objects.create(owner=mebel_kresla_markiz, name='B', dimension='см')
	GroupParameter.objects.create(owner=mebel_kresla_markiz, name='H', dimension='см')

	mebel_kresla_meshok = Group.objects.create(
		name="Мешок", picture="mebel_kresla_meshok.png", parent=mebel_kresla)
	GroupParameter.objects.create(owner=mebel_kresla_meshok, name='А', dimension='см')
	GroupParameter.objects.create(owner=mebel_kresla_meshok, name='H', dimension='см')

	mebel_kresla_volter = Group.objects.create(
		name="Вольтер", picture="mebel_kresla_volter.png", parent=mebel_kresla)
	GroupParameter.objects.create(owner=mebel_kresla_volter, name='h', dimension='см')
	GroupParameter.objects.create(owner=mebel_kresla_volter, name='H', dimension='см')

	mebel_kresla_yaico = Group.objects.create(
		name="Яйцо", picture="mebel_kresla_yaico.png", parent=mebel_kresla)
	GroupParameter.objects.create(owner=mebel_kresla_yaico, name='H', dimension='см')

	mebel_poofy = Group.objects.create(
		name="Пуфы", picture="mebel_pufi_pryamoygolnie.png", parent=mebel)
	GroupParameter.objects.create(owner=mebel_poofy, name='A', dimension='см')
	GroupParameter.objects.create(owner=mebel_poofy, name='H', dimension='см')

	mebel_stoly = Group.objects.create(name="Столы", parent=mebel)

	mebel_stoly_barnye = Group.objects.create(
		name="Барные", picture="mebel_stoli_barnie.png", parent=mebel_stoly)
	GroupParameter.objects.create(owner=mebel_stoly_barnye, name='А', dimension='см')
	GroupParameter.objects.create(owner=mebel_stoly_barnye, name='B', dimension='см')
	GroupParameter.objects.create(owner=mebel_stoly_barnye, name='H', dimension='см')

	mebel_stoly_zhurnal = Group.objects.create(
		name="Журнальные", picture="mebel_stoli_jurnalnie.png", parent=mebel_stoly)
	GroupParameter.objects.create(owner=mebel_stoly_zhurnal, name='А', dimension='см')
	GroupParameter.objects.create(owner=mebel_stoly_zhurnal, name='B', dimension='см')
	GroupParameter.objects.create(owner=mebel_stoly_zhurnal, name='H', dimension='см')

	mebel_stoly_comp = Group.objects.create(
		name="Компьютерные", picture="mebel_stoli_komputernie.png", parent=mebel_stoly)
	GroupParameter.objects.create(owner=mebel_stoly_comp, name='А', dimension='см')
	GroupParameter.objects.create(owner=mebel_stoly_comp, name='B', dimension='см')
	GroupParameter.objects.create(owner=mebel_stoly_comp, name='H', dimension='см')

	mebel_stoly_krug = Group.objects.create(
		name="Круглые", picture="mebel_stoli_kruglie.png", parent=mebel_stoly)
	GroupParameter.objects.create(owner=mebel_stoly_krug, name='D', dimension='см')
	GroupParameter.objects.create(owner=mebel_stoly_krug, name='H', dimension='см')

	mebel_stoly_kvadro = Group.objects.create(
		name="Квадратные", picture="mebel_stoli_kvadratnie.png", parent=mebel_stoly)
	GroupParameter.objects.create(owner=mebel_stoly_kvadro, name='A', dimension='см')
	GroupParameter.objects.create(owner=mebel_stoly_kvadro, name='H', dimension='см')

	mebel_stoly_oval = Group.objects.create(
		name="Овальные", picture="mebel_stoli_ovalnie.png", parent=mebel_stoly)
	GroupParameter.objects.create(owner=mebel_stoly_oval, name='A', dimension='см')
	GroupParameter.objects.create(owner=mebel_stoly_oval, name='B', dimension='см')
	GroupParameter.objects.create(owner=mebel_stoly_oval, name='H', dimension='см')

	mebel_stoly_podstav = Group.objects.create(
		name="Подставки", picture="mebel_stoli_podstavki.png", parent=mebel_stoly)
	GroupParameter.objects.create(owner=mebel_stoly_podstav, name='A', dimension='см')
	GroupParameter.objects.create(owner=mebel_stoly_podstav, name='B', dimension='см')
	GroupParameter.objects.create(owner=mebel_stoly_podstav, name='H', dimension='см')

	mebel_stoly_polukrug = Group.objects.create(
		name="Полукруглые", picture="mebel_stoli_polukruglie.png", parent=mebel_stoly)
	GroupParameter.objects.create(owner=mebel_stoly_polukrug, name='D', dimension='см')
	GroupParameter.objects.create(owner=mebel_stoly_polukrug, name='B', dimension='см')
	GroupParameter.objects.create(owner=mebel_stoly_polukrug, name='H', dimension='см')

	mebel_stoly_priamoug = Group.objects.create(
		name="Прямоугольные", picture="mebel_stoli_pryamougolnie.png", parent=mebel_stoly)
	GroupParameter.objects.create(owner=mebel_stoly_priamoug, name='A', dimension='см')
	GroupParameter.objects.create(owner=mebel_stoly_priamoug, name='B', dimension='см')
	GroupParameter.objects.create(owner=mebel_stoly_priamoug, name='H', dimension='см')

	mebel_stoly_servirov = Group.objects.create(
		name="Сервировочные", picture="mebel_stoli_servirovochnie.png", parent=mebel_stoly)
	GroupParameter.objects.create(owner=mebel_stoly_servirov, name='A', dimension='см')
	GroupParameter.objects.create(owner=mebel_stoly_servirov, name='B', dimension='см')
	GroupParameter.objects.create(owner=mebel_stoly_servirov, name='H', dimension='см')

	mebel_stoly_telephon = Group.objects.create(
		name="Телефонные", picture="mebel_stoli_telefonnie.png", parent=mebel_stoly)
	GroupParameter.objects.create(owner=mebel_stoly_telephon, name='A', dimension='см')
	GroupParameter.objects.create(owner=mebel_stoly_telephon, name='B', dimension='см')
	GroupParameter.objects.create(owner=mebel_stoly_telephon, name='H', dimension='см')

	mebel_stulja = Group.objects.create(name="Стулья", parent=mebel)

	mebel_stulja_barn = Group.objects.create(
		name="Барные", picture="mebel_stulya_banketnie.png", parent=mebel_stulja)
	GroupParameter.objects.create(owner=mebel_stulja_barn, name='A', dimension='см')
	GroupParameter.objects.create(owner=mebel_stulja_barn, name='B', dimension='см')
	GroupParameter.objects.create(owner=mebel_stulja_barn, name='H', dimension='см')

	mebel_stulja_zhurnal = Group.objects.create(
		name="Журнальные", picture="mebel_stulya_barnie.png", parent=mebel_stulja)
	GroupParameter.objects.create(owner=mebel_stulja_zhurnal, name='A', dimension='см')
	GroupParameter.objects.create(owner=mebel_stulja_zhurnal, name='B', dimension='см')
	GroupParameter.objects.create(owner=mebel_stulja_zhurnal, name='H', dimension='см')

	mebel_stulja_comp = Group.objects.create(
		name="Компьютерные", picture="mebel_stulya_feniks.png", parent=mebel_stulja)
	GroupParameter.objects.create(owner=mebel_stulja_comp, name='A', dimension='см')
	GroupParameter.objects.create(owner=mebel_stulja_comp, name='B', dimension='см')
	GroupParameter.objects.create(owner=mebel_stulja_comp, name='H', dimension='см')

	mebel_stulja_krug = Group.objects.create(
		name="Круглые", picture="mebel_stulya_iso.png", parent=mebel_stulja)
	GroupParameter.objects.create(owner=mebel_stulja_krug, name='D', dimension='см')
	GroupParameter.objects.create(owner=mebel_stulja_krug, name='H', dimension='см')

	mebel_stulja_kvadrat = Group.objects.create(
		name="Квадратные", picture="mebel_stulya_krossback.png", parent=mebel_stulja)
	GroupParameter.objects.create(owner=mebel_stulja_kvadrat, name='A', dimension='см')
	GroupParameter.objects.create(owner=mebel_stulja_kvadrat, name='H', dimension='см')

	mebel_stulja_oval = Group.objects.create(
		name="Овальные", picture="mebel_stulya_kyavari.png", parent=mebel_stulja)
	GroupParameter.objects.create(owner=mebel_stulja_oval, name='A', dimension='см')
	GroupParameter.objects.create(owner=mebel_stulja_oval, name='B', dimension='см')
	GroupParameter.objects.create(owner=mebel_stulja_oval, name='H', dimension='см')

	mebel_stulja_podstav = Group.objects.create(
		name="Подставки", picture="mebel_stulya_napoleon.png", parent=mebel_stulja)
	GroupParameter.objects.create(owner=mebel_stulja_podstav, name='A', dimension='см')
	GroupParameter.objects.create(owner=mebel_stulja_podstav, name='B', dimension='см')
	GroupParameter.objects.create(owner=mebel_stulja_podstav, name='H', dimension='см')

	mebel_stulja_polukrug = Group.objects.create(
		name="Полукруглые", picture="mebel_stulya_nechto.png", parent=mebel_stulja)
	GroupParameter.objects.create(owner=mebel_stulja_polukrug, name='D', dimension='см')
	GroupParameter.objects.create(owner=mebel_stulja_polukrug, name='B', dimension='см')
	GroupParameter.objects.create(owner=mebel_stulja_polukrug, name='H', dimension='см')

	mebel_stulja_priamoug = Group.objects.create(
		name="Прямоугольные", picture="mebel_stulya_panton.png", parent=mebel_stulja)
	GroupParameter.objects.create(owner=mebel_stulja_priamoug, name='A', dimension='см')
	GroupParameter.objects.create(owner=mebel_stulja_priamoug, name='B', dimension='см')
	GroupParameter.objects.create(owner=mebel_stulja_priamoug, name='H', dimension='см')

	mebel_stulja_servo = Group.objects.create(
		name="Сервировочные", picture="mebel_stulya_panton.png", parent=mebel_stulja)
	GroupParameter.objects.create(owner=mebel_stulja_servo, name='A', dimension='см')
	GroupParameter.objects.create(owner=mebel_stulja_servo, name='B', dimension='см')
	GroupParameter.objects.create(owner=mebel_stulja_servo, name='H', dimension='см')

	mebel_stulja_telephon = Group.objects.create(
		name="Пластиковые", picture="mebel_stulya_plastikovie.png", parent=mebel_stulja)
	GroupParameter.objects.create(owner=mebel_stulja_telephon, name='A', dimension='см')
	GroupParameter.objects.create(owner=mebel_stulja_telephon, name='B', dimension='см')
	GroupParameter.objects.create(owner=mebel_stulja_telephon, name='H', dimension='см')

	mebel_stulja_сomp2 = Group.objects.create(
		name="Призрак", picture="mebel_stulya_prizrak.png", parent=mebel_stulja)
	GroupParameter.objects.create(owner=mebel_stulja_сomp2, name='A', dimension='см')
	GroupParameter.objects.create(owner=mebel_stulja_сomp2, name='B', dimension='см')
	GroupParameter.objects.create(owner=mebel_stulja_сomp2, name='H', dimension='см')

	mebel_stulja_krug2 = Group.objects.create(
		name="Режисёрские", picture="mebel_stulya_rejiserskie.png", parent=mebel_stulja)
	GroupParameter.objects.create(owner=mebel_stulja_krug2, name='D', dimension='см')
	GroupParameter.objects.create(owner=mebel_stulja_krug2, name='H', dimension='см')

	mebel_stulja_selena = Group.objects.create(
		name="Cелена", picture="mebel_stulya_selena.png", parent=mebel_stulja)
	GroupParameter.objects.create(owner=mebel_stulja_selena, name='A', dimension='см')
	GroupParameter.objects.create(owner=mebel_stulja_selena, name='H', dimension='см')

	mebel_stulja_taburet = Group.objects.create(
		name="Табуреты", picture="mebel_stulya_tabureti.png", parent=mebel_stulja)
	GroupParameter.objects.create(owner=mebel_stulja_taburet, name='A', dimension='см')
	GroupParameter.objects.create(owner=mebel_stulja_taburet, name='B', dimension='см')
	GroupParameter.objects.create(owner=mebel_stulja_taburet, name='H', dimension='см')

	mebel_stulja_tere = Group.objects.create(
		name="Тере", picture="mebel_stulya_tere.png", parent=mebel_stulja)
	GroupParameter.objects.create(owner=mebel_stulja_tere, name='A', dimension='см')
	GroupParameter.objects.create(owner=mebel_stulja_tere, name='B', dimension='см')
	GroupParameter.objects.create(owner=mebel_stulja_tere, name='H', dimension='см')

	mebel_stulja_vena = Group.objects.create(
		name="Венские", picture="mebel_stulya_venskie.png", parent=mebel_stulja)
	GroupParameter.objects.create(owner=mebel_stulja_vena, name='D', dimension='см')
	GroupParameter.objects.create(owner=mebel_stulja_vena, name='B', dimension='см')
	GroupParameter.objects.create(owner=mebel_stulja_vena, name='H', dimension='см')

	mebel_stulja_versal = Group.objects.create(
		name="Версаль", picture="mebel_stulya_versal.png", parent=mebel_stulja)
	GroupParameter.objects.create(owner=mebel_stulja_versal, name='A', dimension='см')
	GroupParameter.objects.create(owner=mebel_stulja_versal, name='B', dimension='см')
	GroupParameter.objects.create(owner=mebel_stulja_versal, name='H', dimension='см')

	mebel_skaphetazh = Group.objects.create(name="Шкафы и этажерки", parent=mebel)

	mebel_skaphetazh_comod = Group.objects.create(
		name="Комоды", picture="mebel_shkafi i etagerki_komodi.png", parent=mebel_skaphetazh)
	GroupParameter.objects.create(owner=mebel_skaphetazh_comod, name='A', dimension='см')
	GroupParameter.objects.create(owner=mebel_skaphetazh_comod, name='B', dimension='см')
	GroupParameter.objects.create(owner=mebel_skaphetazh_comod, name='H', dimension='см')

	mebel_skaphetazh_krovattumba = Group.objects.create(
		name="Прикроватные тумбы", picture="mebel_shkafi i etagerki_tumbi_prikrovatnie.png", parent=mebel_skaphetazh)
	GroupParameter.objects.create(owner=mebel_skaphetazh_krovattumba, name='A', dimension='см')
	GroupParameter.objects.create(owner=mebel_skaphetazh_krovattumba, name='B', dimension='см')
	GroupParameter.objects.create(owner=mebel_skaphetazh_krovattumba, name='H', dimension='см')

	mebel_skaphetazh_priamougtumba = Group.objects.create(
		name="Прямоугольные тумбы", picture="mebel_shkafi i etagerki_tumbi_pryamougolnie.png", parent=mebel_skaphetazh)
	GroupParameter.objects.create(owner=mebel_skaphetazh_priamougtumba, name='A', dimension='см')
	GroupParameter.objects.create(owner=mebel_skaphetazh_priamougtumba, name='B', dimension='см')
	GroupParameter.objects.create(owner=mebel_skaphetazh_priamougtumba, name='H', dimension='см')

	mebel_skaphetazh_phonetumba = Group.objects.create(
		name="Телефонные тумбы", picture="mebel_shkafi i etagerki_tumbi_telefonnie.png", parent=mebel_skaphetazh)
	GroupParameter.objects.create(owner=mebel_skaphetazh_phonetumba, name='A', dimension='см')
	GroupParameter.objects.create(owner=mebel_skaphetazh_phonetumba, name='B', dimension='см')
	GroupParameter.objects.create(owner=mebel_skaphetazh_phonetumba, name='H', dimension='см')

	mebel_skaphetazh_etazherki = Group.objects.create(
		name="Этажерки", picture="mebel_shkafi i etagerki_etagerki.png", parent=mebel_skaphetazh)
	GroupParameter.objects.create(owner=mebel_skaphetazh_etazherki, name='A', dimension='см')
	GroupParameter.objects.create(owner=mebel_skaphetazh_etazherki, name='B', dimension='см')
	GroupParameter.objects.create(owner=mebel_skaphetazh_etazherki, name='H', dimension='см')

	mebel_skaphetazh_shkaphy = Group.objects.create(
		name="Шкафы", picture="mebel_shkafi i etagerki_shkafi.png", parent=mebel_skaphetazh)
	GroupParameter.objects.create(owner=mebel_skaphetazh_shkaphy, name='A', dimension='см')
	GroupParameter.objects.create(owner=mebel_skaphetazh_shkaphy, name='B', dimension='см')
	GroupParameter.objects.create(owner=mebel_skaphetazh_shkaphy, name='H', dimension='см')

	mebel_skaphetazh_stelazhy = Group.objects.create(
		name="Стеллажи", picture="mebel_shkafi i etagerki_stellagi.png", parent=mebel_skaphetazh)
	GroupParameter.objects.create(owner=mebel_skaphetazh_stelazhy, name='A', dimension='см')
	GroupParameter.objects.create(owner=mebel_skaphetazh_stelazhy, name='B', dimension='см')
	GroupParameter.objects.create(owner=mebel_skaphetazh_stelazhy, name='H', dimension='см')

	mebel_skaphetazh_trumo = Group.objects.create(
		name="Трюмо", picture="mebel_shkafi i etagerki_trumo.png", parent=mebel_skaphetazh)
	GroupParameter.objects.create(owner=mebel_skaphetazh_trumo, name='A', dimension='см')
	GroupParameter.objects.create(owner=mebel_skaphetazh_trumo, name='B', dimension='см')
	GroupParameter.objects.create(owner=mebel_skaphetazh_trumo, name='H', dimension='см')

	mebel_krovati = Group.objects.create(
		name="Кровати", parent=mebel, picture="mebel_krovati.png")
	GroupParameter.objects.create(owner=mebel_skaphetazh_trumo, name='A', dimension='см')
	GroupParameter.objects.create(owner=mebel_skaphetazh_trumo, name='B', dimension='см')
	GroupParameter.objects.create(owner=mebel_skaphetazh_trumo, name='H', dimension='см')

	podsvech = Group.objects.create(name="Подсвечники")

	podsvech_dlyatolstyh = Group.objects.create(
		name="Для толстых свечей", parent=podsvech)

	podsvech_dlyatolstyh_azhur = Group.objects.create(
		name="Ажурные", parent=podsvech_dlyatolstyh, picture="podsvechniki_dlya_tolstih_agurnie.png")
	GroupParameter.objects.create(owner=podsvech_dlyatolstyh_azhur, name='D', dimension='см')
	GroupParameter.objects.create(owner=podsvech_dlyatolstyh_azhur, name='H', dimension='см')

	podsvech_dlyatolstyh_straz = Group.objects.create(
		name="Со стразами", parent=podsvech_dlyatolstyh, picture="podsvechniki_dlya_tolstih_so_strazami.png")
	GroupParameter.objects.create(owner=podsvech_dlyatolstyh_straz, name='D', dimension='см')
	GroupParameter.objects.create(owner=podsvech_dlyatolstyh_straz, name='H', dimension='см')

	podsvech_dlyatolstyh_stojki = Group.objects.create(
		name="Стойки", parent=podsvech_dlyatolstyh, picture="podsvechniki_dlya_tolstih_stoiki.png")
	GroupParameter.objects.create(owner=podsvech_dlyatolstyh_stojki, name='D', dimension='см')
	GroupParameter.objects.create(owner=podsvech_dlyatolstyh_stojki, name='H', dimension='см')

	podsvech_dlyatolstyh_podstavki = Group.objects.create(
		name="Подставки", parent=podsvech_dlyatolstyh, picture="podsvechniki_dlya_tolstih_podstavki.png")
	GroupParameter.objects.create(owner=podsvech_dlyatolstyh_podstavki, name='D', dimension='см')

	podsvech_dlyatonkih = Group.objects.create(
		name="Для тонких свечей", parent=podsvech)

	podsvech_dlyatonkih_kandel = Group.objects.create(
		name="Канделябры", parent=podsvech_dlyatonkih, picture="podsvechniki_dlya_tonkih_svechei_kandelyabri.png")
	GroupParameter.objects.create(owner=podsvech_dlyatonkih_kandel, name='A', dimension='см')
	GroupParameter.objects.create(owner=podsvech_dlyatonkih_kandel, name='H', dimension='см')
	GroupParameter.objects.create(owner=podsvech_dlyatonkih_kandel, name='Количество свечей', dimension='шт')

	podsvech_dlyatonkih_podstav = Group.objects.create(
		name="Подставки", parent=podsvech_dlyatonkih, picture="podsvechniki_dlya_tonkih_svechei_podstavki.png")

	podsvech_dlyatonkih_vysokie = Group.objects.create(
		name="Высокие", parent=podsvech_dlyatonkih, picture="podsvechniki_dlya_tonkih_svechei_visokie.png")
	GroupParameter.objects.create(owner=podsvech_dlyatonkih_vysokie, name='H', dimension='см')

	podsvech_dlyatolstyh2 = Group.objects.create(
		name="Для толстых свечей", parent=podsvech)

	podsvech_dlyatolstyh2_akvarium = Group.objects.create(
		name="Аквариумы", parent=podsvech_dlyatolstyh2)
	GroupParameter.objects.create(owner=podsvech_dlyatolstyh2_akvarium, name='H', dimension='см')

	podsvech_dlyatolstyh2_bokal = Group.objects.create(
		name="Бокалы", parent=podsvech_dlyatolstyh2)
	GroupParameter.objects.create(owner=podsvech_dlyatolstyh2_bokal, name='H', dimension='см')

	podsvech_dlyatolstyh2_kapli = Group.objects.create(
		name="Капли", parent=podsvech_dlyatolstyh2, picture="podsvechniki_dlya_svechi_tabletki_kapli.png")
	GroupParameter.objects.create(owner=podsvech_dlyatolstyh2_kapli, name='H', dimension='см')

	podsvech_dlyatolstyh2_podstavki = Group.objects.create(
		name="Подставки", parent=podsvech_dlyatolstyh2, picture="podsvechniki_dlya_svechi_tabletki_podstavkii.png")
	GroupParameter.objects.create(owner=podsvech_dlyatolstyh2_podstavki, name='H', dimension='см')

	podsvech_dlyatolstyh2_vostok = Group.objects.create(
		name="Восточные", parent=podsvech_dlyatolstyh2, picture="podsvechniki_dlya_svechi_tabletki_vostochnie.png")
	GroupParameter.objects.create(owner=podsvech_dlyatolstyh2_vostok, name='H', dimension='см')

	posuda = Group.objects.create(name="Посуда")

	posuda_banki = Group.objects.create(
		name="Банки", parent=posuda, picture="posuda_banki.png")
	GroupParameter.objects.create(owner=posuda_banki, name='D', dimension='см')
	GroupParameter.objects.create(owner=posuda_banki, name='H', dimension='см')

	posuda_bludatort1 = Group.objects.create(
		name="Блюда для торта на ножке", parent=posuda, picture="posuda_bluda_dlya_torta_na_nogke.png")
	GroupParameter.objects.create(owner=posuda_bludatort1, name='D', dimension='см')
	GroupParameter.objects.create(owner=posuda_bludatort1, name='H', dimension='см')

	posuda_bludatort2 = Group.objects.create(
		name="Блюда для торта низкие", parent=posuda, picture="posuda_bluda_dlya_torta_nizkie.png")
	GroupParameter.objects.create(owner=posuda_bludatort2, name='D', dimension='см')
	GroupParameter.objects.create(owner=posuda_bludatort2, name='H', dimension='см')

	posuda_bokaly = Group.objects.create(
		name="Бокалы", parent=posuda, picture="posuda_bokali.png")
	GroupParameter.objects.create(owner=posuda_bokaly, name='h', dimension='см')
	GroupParameter.objects.create(owner=posuda_bokaly, name='H', dimension='см')

	posuda_botyli = Group.objects.create(
		name="Бутыли", parent=posuda, picture="posuda_butili.png")
	GroupParameter.objects.create(owner=posuda_botyli, name='D', dimension='см')
	GroupParameter.objects.create(owner=posuda_botyli, name='H', dimension='см')

	posuda_chiniki = Group.objects.create(
		name="Чайники", parent=posuda, picture="posuda_chainiki.png")

	posuda_chashki = Group.objects.create(
		name="Чашки", parent=posuda, picture="posuda_chashki.png")

	posuda_dispenser = Group.objects.create(
		name="Диспенсер", parent=posuda, picture="posuda_dispenseri.png")
	GroupParameter.objects.create(owner=posuda_dispenser, name='D', dimension='см')
	GroupParameter.objects.create(owner=posuda_dispenser, name='H', dimension='см')

	posuda_graphiny = Group.objects.create(
		name="Графины", parent=posuda, picture="posuda_grafini.png")
	GroupParameter.objects.create(owner=posuda_graphiny, name='H', dimension='см')

	posuda_kolcasalphetok = Group.objects.create(
		name="Кольца для салфеток", parent=posuda, picture="posuda_kolca_dlya_salfetok.png")
	GroupParameter.objects.create(owner=posuda_kolcasalphetok, name='A', dimension='см')
	GroupParameter.objects.create(owner=posuda_kolcasalphetok, name='D', dimension='см')

	posuda_kruzhki = Group.objects.create(
		name="Кружки", parent=posuda, picture="posuda_krugki.png")
	GroupParameter.objects.create(owner=posuda_kruzhki, name='D', dimension='см')
	GroupParameter.objects.create(owner=posuda_kruzhki, name='H', dimension='см')

	posuda_kuvshiny = Group.objects.create(
		name="Кружки", parent=posuda, picture="posuda_kuvshini.png")
	GroupParameter.objects.create(owner=posuda_kuvshiny, name='H', dimension='см')

	Group.objects.create(
		name="Наборы для торта", parent=posuda, picture="posuda_nabori_dlya_torta.png")

	posuda_podnosy = Group.objects.create(
		name="Подносы", parent=posuda, picture="posuda_podnosi.png")
	GroupParameter.objects.create(owner=posuda_podnosy, name='A', dimension='см')
	GroupParameter.objects.create(owner=posuda_podnosy, name='B', dimension='см')

	posuda_podstavki = Group.objects.create(
		name="Подставки", parent=posuda, picture="posuda_podstavki.png")
	GroupParameter.objects.create(owner=posuda_podstavki, name='D', dimension='см')
	GroupParameter.objects.create(owner=posuda_podstavki, name='H', dimension='см')

	Group.objects.create(
		name="Сахарницы", parent=posuda, picture="posuda_saharnici.png")

	posuda_stakany = Group.objects.create(
		name="Стаканы", parent=posuda, picture="posuda_saharnici.png")
	GroupParameter.objects.create(owner=posuda_stakany, name='H', dimension='см')

	Group.objects.create(
		name="Столовые приборы", parent=posuda, picture="posuda_stolovie_pribori.png")

	posuda_tarelki = Group.objects.create(
		name="Тарелки", parent=posuda, picture="posuda_tarelki.png")
	GroupParameter.objects.create(owner=posuda_tarelki, name='D', dimension='см')

	Group.objects.create(
		name="Турки", parent=posuda, picture="posuda_turki.png")

	posuda_vazy4frukt = Group.objects.create(
		name="Вазы для фруктов", parent=posuda, picture="posuda_vazi_dlya_fruktov.png")
	GroupParameter.objects.create(owner=posuda_vazy4frukt, name='D', dimension='см')
	GroupParameter.objects.create(owner=posuda_vazy4frukt, name='H', dimension='см')

	posuda_vazy4sladost = Group.objects.create(
		name="Вазы для фруктов", parent=posuda, picture="posuda_vazi_pod_sladosti.png")
	GroupParameter.objects.create(owner=posuda_vazy4sladost, name='H', dimension='см')

	shatry = Group.objects.create(name="Шатры")

	shatry_arochnye = Group.objects.create(
		name="Арочные", parent=shatry, picture="shatri_arochnie.png")
	GroupParameter.objects.create(owner=shatry_arochnye, name='A', dimension='см')
	GroupParameter.objects.create(owner=shatry_arochnye, name='B', dimension='см')
	GroupParameter.objects.create(owner=shatry_arochnye, name='h', dimension='см')
	GroupParameter.objects.create(owner=shatry_arochnye, name='H', dimension='см')

	shatry_arochnyemoduli = Group.objects.create(
		name="Арочные модули", parent=shatry, picture="shatri_arochnii_moduli.png")
	GroupParameter.objects.create(owner=shatry_arochnyemoduli, name='A', dimension='см')
	GroupParameter.objects.create(owner=shatry_arochnyemoduli, name='B', dimension='см')
	GroupParameter.objects.create(owner=shatry_arochnyemoduli, name='H', dimension='см')

	shatry_pagoda = Group.objects.create(
		name="Пагода", parent=shatry, picture="shatri_pagoda.png")
	GroupParameter.objects.create(owner=shatry_pagoda, name='A', dimension='см')
	GroupParameter.objects.create(owner=shatry_pagoda, name='B', dimension='см')
	GroupParameter.objects.create(owner=shatry_pagoda, name='h', dimension='см')
	GroupParameter.objects.create(owner=shatry_pagoda, name='H', dimension='см')

	shatry_sphera = Group.objects.create(
		name="Пагода", parent=shatry, picture="shatri_sfera.png")
	GroupParameter.objects.create(owner=shatry_sphera, name='A', dimension='см')
	GroupParameter.objects.create(owner=shatry_sphera, name='D', dimension='см')
	GroupParameter.objects.create(owner=shatry_sphera, name='h', dimension='см')
	GroupParameter.objects.create(owner=shatry_sphera, name='H', dimension='см')

	shatry_tentpavil = Group.objects.create(
		name="Тентовые павильоны", parent=shatry, picture="shatri_tentovie_paviloni.png")
	GroupParameter.objects.create(owner=shatry_tentpavil, name='A', dimension='см')
	GroupParameter.objects.create(owner=shatry_tentpavil, name='B', dimension='см')
	GroupParameter.objects.create(owner=shatry_tentpavil, name='h', dimension='см')
	GroupParameter.objects.create(owner=shatry_tentpavil, name='H', dimension='см')

	shatry_zvezda = Group.objects.create(
		name="Звезда", parent=shatry, picture="shatri_zvezda.png")
	GroupParameter.objects.create(owner=shatry_zvezda, name='A', dimension='см')
	GroupParameter.objects.create(owner=shatry_zvezda, name='B', dimension='см')
	GroupParameter.objects.create(owner=shatry_zvezda, name='h', dimension='см')
	GroupParameter.objects.create(owner=shatry_zvezda, name='H', dimension='см')

	skamejki = Group.objects.create(name="Скамейки")

	skamejki_banketki = Group.objects.create(
		name="Банкетки", parent=skamejki, picture="skameiki_banketki.png")
	GroupParameter.objects.create(owner=skamejki_banketki, name='A', dimension='см')
	GroupParameter.objects.create(owner=skamejki_banketki, name='B', dimension='см')
	GroupParameter.objects.create(owner=skamejki_banketki, name='H', dimension='см')

	skamejki_lavki = Group.objects.create(
		name="Лавки", parent=skamejki, picture="skameiki_lavki.png")
	GroupParameter.objects.create(owner=skamejki_lavki, name='A', dimension='см')
	GroupParameter.objects.create(owner=skamejki_lavki, name='B', dimension='см')
	GroupParameter.objects.create(owner=skamejki_lavki, name='H', dimension='см')

	skamejki_skami = Group.objects.create(
		name="Скамьи", parent=skamejki, picture="skameiki_skami.png")
	GroupParameter.objects.create(owner=skamejki_skami, name='A', dimension='см')
	GroupParameter.objects.create(owner=skamejki_skami, name='B', dimension='см')
	GroupParameter.objects.create(owner=skamejki_skami, name='H', dimension='см')

	stojki = Group.objects.create(name="Стойки")

	stojki_kolonna = Group.objects.create(
		name="Колонны", parent=stojki, picture="stoiki_kolonni.png")
	GroupParameter.objects.create(owner=stojki_kolonna, name='A', dimension='см')
	GroupParameter.objects.create(owner=stojki_kolonna, name='B', dimension='см')
	GroupParameter.objects.create(owner=stojki_kolonna, name='H', dimension='см')

	stojki_kolonna = Group.objects.create(
		name="Крючки", parent=stojki, picture="stoiki_kruchki.png")
	GroupParameter.objects.create(owner=stojki_kolonna, name='H', dimension='см')

	stojki_kruglye = Group.objects.create(
		name="Круглые", parent=stojki, picture="stoiki_kruglie.png")
	GroupParameter.objects.create(owner=stojki_kruglye, name='D', dimension='см')
	GroupParameter.objects.create(owner=stojki_kruglye, name='H', dimension='см')

	stojki_kvadrat = Group.objects.create(
		name="Квадратные", parent=stojki, picture="stoiki_kvadratnie.png")
	GroupParameter.objects.create(owner=stojki_kvadrat, name='A', dimension='см')
	GroupParameter.objects.create(owner=stojki_kvadrat, name='B', dimension='см')
	GroupParameter.objects.create(owner=stojki_kvadrat, name='H', dimension='см')

	stojki_podsvet = Group.objects.create(
		name="Подсвечники", parent=stojki, picture="stoiki_podsvechniki.png")
	GroupParameter.objects.create(owner=stojki_podsvet, name='D', dimension='см')
	GroupParameter.objects.create(owner=stojki_podsvet, name='H', dimension='см')

	stojki_priamoug = Group.objects.create(
		name="Прямоугольные", parent=stojki, picture="stoiki_pryamougolnie.png")
	GroupParameter.objects.create(owner=stojki_priamoug, name='A', dimension='см')
	GroupParameter.objects.create(owner=stojki_priamoug, name='B', dimension='см')
	GroupParameter.objects.create(owner=stojki_priamoug, name='H', dimension='см')

	svechi = Group.objects.create(name="Свечи")

	svechi_napolnye = Group.objects.create(
		name="Напольные", parent=svechi, picture="svechi_napolnie.png")
	GroupParameter.objects.create(owner=stojki_priamoug, name='D', dimension='см')
	GroupParameter.objects.create(owner=stojki_priamoug, name='H', dimension='см')

	svechi_nasypnye = Group.objects.create(
		name="Насыпные", parent=svechi, picture="svechi_nasipnie.png")
	GroupParameter.objects.create(owner=svechi_nasypnye, name='D', dimension='см')
	GroupParameter.objects.create(owner=svechi_nasypnye, name='H', dimension='см')

	svechi_plavajushie = Group.objects.create(
		name="Плавающие", parent=svechi, picture="svechi_plavauschie.png")
	GroupParameter.objects.create(owner=svechi_plavajushie, name='D', dimension='см')
	GroupParameter.objects.create(owner=svechi_plavajushie, name='H', dimension='см')

	svechi_tabletki = Group.objects.create(
		name="Таблетки", parent=svechi, picture="svechi_tabletki.png")
	GroupParameter.objects.create(owner=svechi_tabletki, name='D', dimension='см')
	GroupParameter.objects.create(owner=svechi_tabletki, name='H', dimension='см')

	svechi_tolstye = Group.objects.create(
		name="Толстые", parent=svechi, picture="svechi_tolstie.png")
	GroupParameter.objects.create(owner=svechi_tolstye, name='D', dimension='см')
	GroupParameter.objects.create(owner=svechi_tolstye, name='H', dimension='см')

	svechi_tonkie = Group.objects.create(
		name="Тонкие", parent=svechi, picture="svechi_tonkie.png")
	GroupParameter.objects.create(owner=svechi_tonkie, name='D', dimension='см')
	GroupParameter.objects.create(owner=svechi_tonkie, name='H', dimension='см')

	tekstil = Group.objects.create(name="Текстиль")

	tekstil_stul = Group.objects.create(name="Текстиль для стульев", parent=tekstil)

	tekstil_stul_chehol = Group.objects.create(name="Чехлы", parent=tekstil_stul)

	tekstil_stul_chehol_banty = Group.objects.create(
		name="Банты", parent=tekstil_stul_chehol, picture="tekstil_tekstil_dlya_stulev_chehli_banti.png")

	tekstil_stul_chehol_zhakety = Group.objects.create(
		name="Жакеты", parent=tekstil_stul_chehol, picture="tekstil_tekstil_dlya_stulev_chehli_jaketi.png")
	GroupParameter.objects.create(owner=tekstil_stul_chehol_zhakety, name='A', dimension='см')
	GroupParameter.objects.create(owner=tekstil_stul_chehol_zhakety, name='H', dimension='см')

	Group.objects.create(
		name="Жакеты c хвостами", parent=tekstil_stul_chehol,
		picture="tekstil_tekstil_dlya_stulev_chehli_jaketi_hvosti.png")

	Group.objects.create(
		name="Получехлы", parent=tekstil_stul_chehol,
		picture="tekstil_tekstil_dlya_stulev_chehli_poluchehli.png")

	tekstil_stul_chehol_priamo = Group.objects.create(
		name="Чехлы прямые", parent=tekstil_stul_chehol,
		picture="tekstil_tekstil_dlya_stulev_chehli_pryamie.png")
	GroupParameter.objects.create(owner=tekstil_stul_chehol_priamo, name='A', dimension='см')
	GroupParameter.objects.create(owner=tekstil_stul_chehol_priamo, name='B', dimension='см')
	GroupParameter.objects.create(owner=tekstil_stul_chehol_priamo, name='h', dimension='см')
	GroupParameter.objects.create(owner=tekstil_stul_chehol_priamo, name='H', dimension='см')

	tekstil_stul_chehol_jubka = Group.objects.create(
		name="Чехлы с юбкой", parent=tekstil_stul_chehol,
		picture="tekstil_tekstil_dlya_stulev_chehli_pryamie.png")
	GroupParameter.objects.create(owner=tekstil_stul_chehol_jubka, name='A', dimension='см')
	GroupParameter.objects.create(owner=tekstil_stul_chehol_jubka, name='B', dimension='см')
	GroupParameter.objects.create(owner=tekstil_stul_chehol_jubka, name='h', dimension='см')
	GroupParameter.objects.create(owner=tekstil_stul_chehol_jubka, name='H', dimension='см')

	Group.objects.create(
		name="Стрэйчбант", parent=tekstil_stul_chehol,
		picture="tekstil_tekstil_dlya_stulev_chehli_streichbanti.png")

	Group.objects.create(
		name="Стрэйч", parent=tekstil_stul_chehol,
		picture="tekstil_tekstil_dlya_stulev_chehli_streitch.png")

	Group.objects.create(
		name="Чехлы универсальные", parent=tekstil_stul_chehol,
		picture="tekstil_tekstil_dlya_stulev_chehli_yniversalnie.png")

	Group.objects.create(
		name="Подушки на стул", parent=tekstil_stul,
		picture="tekstil_tekstil_dlya_stulev_podushki_na_stul.png")

	tekstil_stol = Group.objects.create(name="Текстиль на столы", parent=tekstil)

	tekstil_stol_naperon = Group.objects.create(name="Напероны", parent=tekstil_stol)

	tekstil_stol_naperon_krug = Group.objects.create(
		name="Круглые", parent=tekstil_stol_naperon,
		picture="tekstil_tekstil_na_stoli_naperoni_kruglie.png")
	GroupParameter.objects.create(owner=tekstil_stol_naperon_krug, name='D', dimension='см')

	tekstil_stol_naperon_priamoug = Group.objects.create(
		name="Прямоугольные", parent=tekstil_stol_naperon,
		picture="tekstil_tekstil_na_stoli_naperoni_pryamougolnie.png")
	GroupParameter.objects.create(owner=tekstil_stol_naperon_priamoug, name='A', dimension='см')
	GroupParameter.objects.create(owner=tekstil_stol_naperon_priamoug, name='B', dimension='см')

	tekstil_stol_runner = Group.objects.create(name="Раннеры", parent=tekstil_stol)

	tekstil_stol_runner_priamoj = Group.objects.create(
		name="Прямые", parent=tekstil_stol_runner,
		picture="tekstil_tekstil_na_stoli_ranneri_pryamie")
	GroupParameter.objects.create(owner=tekstil_stol_runner_priamoj, name='A', dimension='см')
	GroupParameter.objects.create(owner=tekstil_stol_runner_priamoj, name='B', dimension='см')

	tekstil_stol_skatert = Group.objects.create(name="Скатерти", parent=tekstil_stol)

	tekstil_stol_skatert_krug = Group.objects.create(
		name="Круглые", parent=tekstil_stol_skatert,
		picture="tekstil_tekstil_na_stoli_skaterti_kryglie.png")
	GroupParameter.objects.create(owner=tekstil_stol_skatert_krug, name='D', dimension='см')

	tekstil_stol_skatert_priamoug = Group.objects.create(
		name="Прямоугольные", parent=tekstil_stol_skatert,
		picture="tekstil_tekstil_na_stoli_skaterti_pryamoygolnie.png")
	GroupParameter.objects.create(owner=tekstil_stol_skatert_priamoug, name='A', dimension='см')
	GroupParameter.objects.create(owner=tekstil_stol_skatert_priamoug, name='B', dimension='см')

	Group.objects.create(
		name="Стрейч", parent=tekstil_stol_skatert,
		picture="tekstil_tekstil_na_stoli_skaterti_streich.png")

	Group.objects.create(
		name="Прямоугольные стрэйч", parent=tekstil_stol_skatert,
		picture="tekstil_tekstil_na_stoli_skaterti_streich_pryamougolnie.png")

	tekstil_stol_jubki = Group.objects.create(name="Юбки", parent=tekstil_stol)

	tekstil_stol_jubki_hvost = Group.objects.create(
		name="С хвостами", parent=tekstil_stol_jubki,
		picture="tekstil_tekstil_na_stoli_ubki_s_hvostami.png")
	GroupParameter.objects.create(owner=tekstil_stol_jubki_hvost, name='A', dimension='см')
	GroupParameter.objects.create(owner=tekstil_stol_jubki_hvost, name='B', dimension='см')

	tekstil_stol_jubki_volna = Group.objects.create(
		name="С волнами", parent=tekstil_stol_jubki,
		picture="tekstil_tekstil_na_stoli_ubki_s_volanami.png")
	GroupParameter.objects.create(owner=tekstil_stol_jubki_volna, name='A', dimension='см')
	GroupParameter.objects.create(owner=tekstil_stol_jubki_volna, name='B', dimension='см')

	tekstil_stol_jubki_skladki = Group.objects.create(
		name="Со складками", parent=tekstil_stol_jubki,
		picture="tekstil_tekstil_na_stoli_ubki_so_skladkami.png")
	GroupParameter.objects.create(owner=tekstil_stol_jubki_skladki, name='A', dimension='см')
	GroupParameter.objects.create(owner=tekstil_stol_jubki_skladki, name='B', dimension='см')

	tekstil_stol_salphetki = Group.objects.create(
		name="Салфетки", parent=tekstil_stol,
		picture="tekstil_tekstil_na_stoli_salfetki.png")
	GroupParameter.objects.create(owner=tekstil_stol_salphetki, name='A', dimension='см')

	tekstil_dorozhki = Group.objects.create(
		name="Дорожки", parent=tekstil, picture="tekstil_dorogki.png")
	GroupParameter.objects.create(owner=tekstil_dorozhki, name='A', dimension='см')
	GroupParameter.objects.create(owner=tekstil_dorozhki, name='B', dimension='см')

	tekstil_kovry = Group.objects.create(
		name="Ковры", parent=tekstil, picture="tekstil_kovri.png")
	GroupParameter.objects.create(owner=tekstil_kovry, name='A', dimension='см')
	GroupParameter.objects.create(owner=tekstil_kovry, name='B', dimension='см')

	tekstil_kovry = Group.objects.create(
		name="Пледы (рис)", parent=tekstil, picture="tekstil_kovri.png")
	GroupParameter.objects.create(owner=tekstil_kovry, name='A', dimension='см')
	GroupParameter.objects.create(owner=tekstil_kovry, name='B', dimension='см')

	tekstil_podushki = Group.objects.create(
		name="Подушки", parent=tekstil, picture="tekstil_podushki.png")
	GroupParameter.objects.create(owner=tekstil_podushki, name='A', dimension='см')
	GroupParameter.objects.create(owner=tekstil_podushki, name='B', dimension='см')

	tekstil_tkani = Group.objects.create(
		name="Ткани", parent=tekstil, picture="tekstil_tkani.png")
	GroupParameter.objects.create(owner=tekstil_tkani, name='A', dimension='см')
	GroupParameter.objects.create(owner=tekstil_tkani, name='B', dimension='см')
