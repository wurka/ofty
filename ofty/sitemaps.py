from django.contrib.sitemaps import Sitemap
from django.contrib.sitemaps import reverse
from units.models import Unit


# обычные страницы
class GeneralMap(Sitemap):
	def items(self):
		return ['index']

	def location(self, item):
		return reverse(item)


class UnitsMap(Sitemap):
	def items(self):
		return Unit.objects.filter(is_deleted=False)


ofty_maps = {
	'general': GeneralMap,
	'units': UnitsMap
}
