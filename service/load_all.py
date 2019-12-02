# totally fill empty base with presets
# to run this script do:
# python3 manage.py shell
# >> exec(open('service/load_all.py', encoding='utf8').read())

import service.load_groups
import service.load_colors
import service.load_materials
import service.load_city