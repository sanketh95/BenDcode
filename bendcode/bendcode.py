def encode(ps):
	benstring = ''
	if isinstance(ps, basestring):
		return ''.join([str(len(ps)), ':', ps])
	if isinstance(ps, int):
		return ''.join(['i'+str(ps)+'e'])
	if isinstance(ps, list):
		return 'l'+''.join([encode(i) for i in ps]) + 'e'
	if isinstance(ps, dict):
		return 'd'+''.join([encode(key)+encode(value) for key, value in ps.items()])+'e'

def _decode(raw):
	if len(raw) == 0:
		return None, ''
	f = raw[0]
	if f == 'l':
		rv, remstr = None, raw[1:]
		val = []
		while(remstr != '' and remstr[0] != 'e'):
			rv, remstr = _decode(remstr)
			val.append(rv)
		if remstr == '':
			raise ValueError()
		return val, remstr[1:]

	elif f == 'i':
		val = 0
		ind = 0
		for i, r in enumerate(raw[1:]):
			if r == 'e':
				return val, raw[1:][i+1:]
			else:
				val = (val*10) + int(r)
		raise ValueError('')
	elif f in [str(i) for i in range(10)]:
		val = 0
		for i,r in enumerate(raw):
			if r == ':':
				raw = raw[i+1:]
				break
			else:
				val = (10 * val) + int(r)
		s = raw[:val]
		raw = raw[val:]
		return s, raw
	elif f == 'd':
		rv, remstr = None, raw[1:]
		val = {}
		while remstr != '' and remstr[0] != 'e':
			rv, remstr = _decode(remstr)
			rv1, remstr = _decode(remstr)
			val[rv] = rv1
		if remstr == '':
			raise ValueError()
		return val, remstr[1:]

def decode(raw):
	return _decode(raw)