from .exceptions import *

def encode(ps):
	if isinstance(ps, basestring):
		return ''.join([str(len(ps)), ':', ps])
	if isinstance(ps, int):
		return ''.join(['i'+str(ps)+'e'])
	if isinstance(ps, list):
		return 'l'+''.join([encode(i) for i in ps]) + 'e'
	if isinstance(ps, dict):
		return 'd'+''.join([encode(key)+encode(value) for key, value in ps.items()])+'e'

def match_string(raw, fail_silently=True):
	raw_copy = raw
	try:
		if raw == '':
			raise MalformedBencodeError()
		l = 0
		for i, r in enumerate(raw):
			if r == ':':
				raw = raw[i+1:]
				break
			l = (l * 10) + int(r)
		return raw[:l], raw[l:]
	except Exception, e:
		if not fail_silently:
			raise MalformedBencodeError()
		return None, raw_copy

def match_int(raw, fail_silently=True):
	raw_copy = raw
	try:
		if raw == '' or raw[0] != 'i':
			raise MalformedBencodeError()
		raw, val = raw[1:], 0
		for i, r in enumerate(raw):
			if r == 'e':
				return val, raw[i+1:]
			else:
				val = (val*10) + int(r)
		raise MalformedBencodeError()
	except Exception, e:
		if not fail_silently:
			raise MalformedBencodeError()
		return None, raw_copy

def match_list(raw, fail_silently=True):
	raw_copy = raw
	try:
		if raw == '' or raw[0] != 'l':
			raise MalformedBencodeError()
		raw, val = raw[1:], []
		while raw != '' and raw[0] != 'e':
			rvs = [func(raw) for func in match_type_funcs]
			chosen = [(v, raw) for v,raw in rvs if v]
			if not chosen:
				raise MalformedBencodeError()
			val.append(chosen[0][0])
			raw = chosen[0][1]
		if raw == '':
			raise MalformedBencodeError()
		return val, raw[1:]
	except Exception, e:
		if not fail_silently:
			raise MalformedBencodeError()
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
			chosen = [(v, raw) for v, raw in rvs if v]
			if not chosen:
				raise MalformedBencodeError()
			val[key] = chosen[0][0]
			raw = chosen[0][1]
		if raw == '':
			raise MalformedBencodeError()
		return val, raw[1:]
	except Exception, e:
		if not fail_silently:
			raise MalformedBencodeError()
		return None, raw_copy

def _decode(raw):
	rvs = [func(raw) for func in match_type_funcs]
	chosen = [(val, raw) for val, raw in rvs if val]
	if not chosen:
		raise MalformedBencodeError()
	return chosen[0]

def decode(raw):
	return _decode(raw)[0]

match_type_funcs = [match_list, match_dict, match_string, match_int]