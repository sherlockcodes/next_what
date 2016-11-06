from string import maketrans
from commons import consts

class MovieCleaner:
	def __init__(self):
		pass

	def decrapify_name(self, name):
		name = self.apply_replace_rule(name)
		name = self.remove_junk_characters(name)
		name = self.remove_release_year(name)
		return " ".join(name.split())

	def apply_replace_rule(self, name):
		trantab = maketrans(consts.REPLACE_RULE[0], consts.REPLACE_RULE[1])
		return name.translate(trantab)

	def remove_junk_characters(self,name):
		for junk_char in consts.JUNK_CHARS:
			if junk_char in name:
				if name.startswith(junk_char) and junk_char in consts.JUNK_CHARS_MAPPER:
					junk_char = consts.JUNK_CHARS_MAPPER[junk_char]
					index_of = name.index(junk_char)
					name = name[index_of+1:len(name)-1]
					continue
				index_of = name.index(junk_char)
				name = name[0:index_of]
		return name

	def remove_release_year(self, name):
		numbers = [int(s) for s in name.split() if s.isdigit()]
		for number in numbers:
			if number > 1980 and number <= 2050:
				index_of = name.index(str(number))
				name = name[0:index_of]
		return name





