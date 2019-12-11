# to run this script do:
# python3 manage.py shell
# >> exec(open('units/service/load_materials.py', encoding='utf8').read())

from units.models import Material

print("LOAD MATERIALS: this script will delete and recreate ALL data about materials (Unit.Material) Continue? (y/n)?")

if input("for continue print y: ").lower() == "y":
	Material.objects.all().delete()

	materials = [
		"абалон", "авантюрин", "агат", "ажур", "азурит", "акварель", "акрил", "алебастр", "алмаз", "альпака", "алюминий",
		"амазонит", "аметист", "аммонит", "ангора", "апатит", "атлас", "базальт", "бамбук", "бархат", "батист", "береза",
		"береста", "бетон", "бечевка", "бирюза", "бисер", "бостон", "брокат", "бронза", "бук", "букле", "бумага", "бусины",
		"бычий глаз", "бюск", "бязь", "варисцит", "вата", "ватин", "ватман", "вельвет", "велюр", "вискоза", "воск", "вуаль",
		"габардин", "гагат", "газ", "гарус", "габардин", "гель", "гематит", "гипс", "гипюр", "глина", "глиттер", "глицерин",
		"говлит", "гофробумага", "гофрокартон", "гранат", "гранит", "гранулят", "гуашь", "двп", "деворе", "деним",
		"дерево", "джерси", "джут", "диорит", "дмс", "драп", "дсп", "дуб", "дублерин", "дундага", "дюраль", "дюспо",
		"евросетка", "еврофатин", "ель", "жадеит", "жаккард", "жемчуг", "жидкое стекло", "жоржет", "замша", "зеркало",
		"змеевик", "золото", "ива", "известняк", "изолон", "изумруд", "икат", "ильм", "интерлок", "иолит", "ироко",
		"камень", "капрон", "картон", "кашемир", "кварц", "кедр", "керамика", "кианит", "клен", "ковролин", "кожа",
		"кожзам", "конфетти", "коралл", "кошачий глаз", "крепдешин", "креп-жоржер", "креп-сатин", "креп-шифон",
		"кружево", "лабрадорит", "лазурит", "латунь", "лдсп", "лен", "леска", "липа", "лоден", "лодолит", "лоза",
		"лоскут", "лунный камень", "малахит", "мдф", "медь", "мельхиор", "меринос", "металл", "мех", "мешковина",
		"микрофибра", "миткаль", "мовингу", "можжевельник", "мох", "мохер", "мрамор", "натуральные", "нейлон",
		"неопрен", "нержавейка", "нефрит", "никель", "нубук", "обсидиан", "овчина", "олово", "ольха", "оникс",
		"опал", "опилки", "оракал", "органди", "органза", "осина", "паволока", "падук", "пайетки", "пакля",
		"палисандр", "папплин", "паптит", "папье-маше", "паралон", "парафин", "парча", "патина", "пвд", "пвс", "пвх",
		"пенопласт", "перламутр", "перо", "пике", "пирит", "пластик", "плюш", "полиамид", "полим. глина", "полиэстер",
		"порфир", "проволока", "пряжа", "пух", "резина", "репс", "рибана", "рисовая бумага", "родонит", "ротанг",
		"рубин", "рутил", "сапфир", "саржа", "сатин", "сердолик", "серебро", "сетка", "сизаль", "силикон", "синтепон",
		"синтепух", "ситец", "слюда", "смальта", "смола", "содалит", "солома", "сосна", "спандекс", "сплав", "сталь",
		"стекло", "стеклярус", "стразы", "стрейч", "сукно", "сутаж", "тактел", "танзанит", "тафта", "твид", "твил",
		"твин", "темпера", "тефлон", "тигровый глаз", "титан", "ткань", "топаз", "трикотаж", "туаль", "тулит",
		"турмалин", "тутовая бумага", "тюль", "уголь", "унакит", "фанера", "фарфор", "фатин", "фаянс", "фетр",
		"фианит", "фибергласс", "фланель", "флизелин", "флис", "флок", "флюорит", "фоамиран", "халцедон", "хаулит",
		"хвоя", "хлопок", "холофайбер", "холст", "хризокола", "хризолит", "хризопраз", "хрусталь", "цинк", "циркон",
		"цитрин", "цоизит", "чароит", "чугун", "шанжан", "шевиот", "шелк", "шерсть", "шифон", "шотландка", "шпатель",
		"шунгит", "эпокс. смола", "яблоня", "янтарь", "ясень", "яшма"
	]

	for m in materials:
		Material.objects.create(name=m)