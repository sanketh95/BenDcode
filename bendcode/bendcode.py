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
