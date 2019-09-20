def convert_to_text(item_list):
	text = ''
	for i, item in enumerate(item_list):
		sep = ''
		if text:
			sep = ' and ' if i + 1 == len(item_list) else ', '
		text += '%s"%s"' % (sep, item)
	return text
