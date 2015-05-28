class MalformedBencodeError(ValueError):
	def __init__(self, msg=''):
		super(MalformedBencodeError, self).__init__(msg)
