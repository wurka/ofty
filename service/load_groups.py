# to run this script do:
# python3 manage.py shell
# >> exec(open('service/load_groups.py', encoding='utf8').read())
import os

from units.models import Group, GroupParameter

print("LOAD GROUPS: THIS script will delete ALL data from database. Do it?")


def build_from_source(source):
	Group.objects.all().delete()
	# GroupParameter очичищается автоматически, т.к. содержит ссылки на Group (not Null)
	# level = 0
	lines = source.splitlines()
	# last_level = -1
	history = [None]
	new_group_parameters = list()
	new_groups = list()

	for line_index, line in enumerate(lines):
		# пропуск пустых строк
		print(f"line {line_index+1}... {line}")
		if line.strip() == "":
			print("empty string. skipped.")
			continue
		spaces = len(line) - len(line.lstrip())

		# это фотография
		if line.strip().endswith('.png'):
			print("this is photo")
			if len(history) == 0:
				raise ValueError(f"[{line_index+1}]: photo founded without parent group")
			if len(history) <= spaces:
				raise ValueError(f"[{line_index+1}]: invalid intention")

			# применить картинку
			if line.strip().endswith('_razm.png'):  # признак того, что картинка с указанием размеров
				history[spaces].size_picture = line.strip()
				history[spaces].active = True
			else:
				history[spaces].picture = line.strip()
			history[spaces].save()

		# это параметр
		elif "=" in line:
			print('this is parameter')
			if len(history) < spaces:
				raise ValueError(f"[{line_index+1}]: can not find parent group")
			split = line.split("=")
			name = split[0].strip()
			dimension = "=".join(split[1:])
			try:
				new_parameter = GroupParameter.objects.create(
					owner=history[spaces], name=name, dimension=dimension)
			except IndexError:
				raise ValueError(f"[{line_index+1}]: invalid parameter position")
			new_group_parameters.append(new_parameter)

		# это название подгруппы
		else:
			print('this is group')
			if len(history) > 0:
				try:
					new_group = Group.objects.create(name=line.strip(), parent=history[spaces])
				except IndexError:
					raise ValueError(f'[{line_index+1}]: wrong group hierarchy')
			else:
				print('fuck up with history')
			new_groups.append(new_group)
			history = history[:spaces+1] + [new_group]
			if len(history) < spaces + 1:
				raise ValueError(f"[{line_index+1}]: invalid intention")

	return new_groups, new_group_parameters


try:
	filename = "groups_20200406.txt"
	filename = "./db_content/" + filename
	with open(filename, 'rt', encoding='utf8') as file:
		src = file.read()
		groups, parameters = build_from_source(src)
		print(f'ok. added groups: {len(groups)}; parameters: {len(parameters)}')
except FileNotFoundError:
	print("FAIL: there is no file: " + os.path.abspath(filename))



