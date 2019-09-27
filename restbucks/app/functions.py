def convert_to_text(items):
	"""
	Takes list of items, join them and returns a text as a result.

	e.g.
		convert_to_text(['Latte']) -> "Latte"
		convert_to_text(['Latte', 'Cappuccino']) -> "Latte and Cappuccino"
		convert_to_text(['Latte', 'Cappuccino', 'Espresso']) -> "Latte, Cappuccino and Espresso"

	:param items: list of items
	:return: joined list using "and" and "," as a text
	"""
	text = ''
	for i, item in enumerate(items):
		sep = ''
		if text:
			# check to use "and" or ","
			sep = ' and ' if i + 1 == len(items) else ', '
		text += "%s'%s'" % (sep, item)
	return text
