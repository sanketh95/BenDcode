from .exceptions import *

def encode(ps, fail_silently=True):
	try:
		if isinstance(ps, str):
			return ''.join([str(len(ps)), ':', ps])
		if isinstance(ps, int):
			return ''.join(['i',str(ps),'e'])
		if isinstance(ps, list):
			return 'l'+''.join([encode(i) for i in ps]) + 'e'
		if isinstance(ps, dict):
			for key, value in ps.items():
				if not isinstance(key, str):
					raise MalformedBencodeError()
			return 'd'+''.join([encode(key)+encode(value) for key, value in ps.items()])+'e'
		raise MalformedBencodeError()
	except Exception:
		raise
		if not fail_silently:
			raise MalformedBencodeError('Failed to encode ' + str(ps))
		return ''

def match_string(raw, fail_silently=True):
	raw_copy = raw
	try:
		if raw == '':
			raise MalformedBencodeError()
		int(raw[0])
		l = 0
		for i, r in enumerate(raw):
			if r == ':':
				raw = raw[i+1:]
				break
			l = (l * 10) + int(r)
		if (len(raw) < l):
			raise MalformedBencodeError()
		return raw[:l], raw[l:]
	except Exception:
		if not fail_silently:
			raise MalformedBencodeError('Failed to match string in ' + str(raw))
		return None, raw_copy

def match_int(raw, fail_silently=True):
	raw_copy = raw
	try:
		if raw == '' or raw[0] != 'i':
			raise MalformedBencodeError()
		raw, val = raw[1:], ''
		for i, r in enumerate(raw):
			if r == 'e':
				return (0 if val == '' else int(val)), raw[i+1:]
			else:
				val = val + r
		raise MalformedBencodeError()
	except Exception:
		if not fail_silently:
			raise MalformedBencodeError('Failed to match int in ' + str(raw))
		return None, raw_copy

def match_list(raw, fail_silently=True):
	raw_copy = raw
	try:
		if raw == '' or raw[0] != 'l':
			raise MalformedBencodeError()
		raw, val = raw[1:], []
		while raw != '' and raw[0] != 'e':
			rvs = [func(raw) for func in match_type_funcs]
			chosen = [(v, raw) for v,raw in rvs if v is not None]
			if not chosen:
				raise MalformedBencodeError()
			val.append(chosen[0][0])
			raw = chosen[0][1]
		if raw == '':
			raise MalformedBencodeError()
		return val, raw[1:]
	except Exception:
		if not fail_silently:
			raise MalformedBencodeError('Failed to match list in ' + str(raw))
		return None, raw_copy

def match_dict(raw, fail_silently=True):
	raw_copy = raw
	try:
		if raw == '' or raw[0] != 'd':
			raise MalformedBencodeError()
		raw, val = raw[1:], {}
		while raw != '' and raw[0] != 'e':
			key, raw = match_string(raw)
			if not key:
				raise MalformedBencodeError()
			rvs = [func(raw) for func in match_type_funcs]
			chosen = [(v, raw) for v, raw in rvs if v is not None]
			if not chosen:
				raise MalformedBencodeError()
			val[key] = chosen[0][0]
			raw = chosen[0][1]
		if raw == '':
			raise MalformedBencodeError()
		return val, raw[1:]
	except Exception:
		if not fail_silently:
			raise MalformedBencodeError('Failed match dict in ' + str(raw))
		return None, raw_copy

def _decode(raw, fail_silently=True):
	try:
		rvs = [func(raw) for func in match_type_funcs]
		chosen = [(val, raw) for val, raw in rvs if val is not None]
		if not chosen:
			raise MalformedBencodeError()
		return chosen[0]
	except Exception:
		if not fail_silently:
			raise MalformedBencodeError('Failed to decode ' + str(raw))
		return (None, raw)

def decode(raw, fail_silently=True):
	return _decode(raw, fail_silently)[0]

match_type_funcs = [match_list, match_dict, match_string, match_int]