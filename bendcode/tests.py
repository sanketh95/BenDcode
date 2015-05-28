import unittest
from .bendcode import match_string, match_int, match_dict, match_list, decode, encode
from .exceptions import MalformedBencodeError

class TestDecoder(unittest.TestCase):
	# Test normal int
	def test_int(self):
		self.assertEqual(match_int('i200e')[0], 200)

	# Test empty integer
	# It is the same as zero
	def test_empty_int(self):
		self.assertEqual(match_int('ie')[0], 0)

	# Test proper string
	def test_string(self):
		self.assertEqual(match_string('7:Pallavi')[0], 'Pallavi')

	# Test empty string
	def test_empty_string(self):
		self.assertEqual(match_string('0:')[0], '')

	# Test malformed string
	def test_malformed_string_raising_exception(self):
		with self.assertRaises(MalformedBencodeError):
			match_string(':', False)

	def test_small_string(self):
		with self.assertRaises(MalformedBencodeError):
			match_string('3:ab', False)

	# Malformed string without raising exception
	def test_malformed_string_fail_silent(self):
		self.assertEqual(match_string('jsdha')[0], None)

	# Test empty list
	def test_empty_list(self):
		self.assertEqual(match_list('le')[0], [])

	# Test normal list
	def test_list(self):
		self.assertEqual(match_list('li20e3:123e')[0], [20, '123'])

	# Test nested empty lists
	def test_nested_empty_lists(self):
		self.assertEqual(match_list('llee')[0], [[]])

	# Test nested normal lists
	def test_nested_lists(self):
		self.assertEqual(match_list('lli20eee')[0], [[20]])

	# Test empty dicts
	def test_empty_dict(self):
		self.assertEqual(match_dict('de')[0], {})

	# Test nested empty dicts
	def test_nested_empty_dicts(self):
		self.assertEqual(match_dict('d1:adee')[0], {'a':{}})

	# Test normal dict
	def test_dict(self):
		self.assertEqual(match_dict('d1:ai123ee')[0], {'a': 123})

	# Test dict with a list value
	def test_dict_list(self):
		self.assertEqual(match_dict('d1:ali20e2:abee')[0], {'a': [20, 'ab']})

	# Test list with higher levels of nesting
	def test_high_nesting_list(self):
		self.assertEqual(match_list('lllleeee')[0], [[[[]]]])

	# Test dict with integer key
	def test_dict_with_int_key(self):
		with self.assertRaises(MalformedBencodeError):
			match_dict('di12ei23ee', False)

	# Test decode int
	def test_decode_int(self):
		self.assertEqual(decode('i23e'), 23)

	# Decode complex bencode
	def test_decode_complex(self):
		self.assertEqual(decode('d7:pallavilli1234eei90e3:123ee'), {'pallavi': [[1234], 90, '123']})

	# Encode int
	def test_encode_int(self):
		self.assertEqual(encode(123), 'i123e')

	# Encode string
	def test_encode_string(self):
		self.assertEqual(encode('abc'), '3:abc')

	# Encode empty list
	def test_encode_empty_list(self):
		self.assertEqual(encode([]), 'le')

	# Encode nested empty lists
	def test_encode_nested_empty_lists(self):
		self.assertEqual(encode([[]]), 'llee')

	# Encode normal nested lists
	def test_encode_nested_lists(self):
		self.assertEqual(encode([[123]]), 'lli123eee')

	# Encode empty dict
	def test_encode_empty_dict(self):
		self.assertEqual(encode({}), 'de')

	# Encode nested empty dicts
	def test_encode_nested_empty_dicts(self):
		self.assertEqual(encode({'a':{}}), 'd1:adee')

	# Encode complex bencode
	def test_encode_complex(self):
		self.assertEqual(encode({'abc': [1, [234]]}), 'd3:abcli1eli234eeee')

	# Encode empty string
	def test_encode_empty_string(self):
		self.assertEqual(encode(''), '0:')

	# Encode zero int
	def test_encode_zero(self):
		self.assertEqual(encode(0), 'i0e')

	# Encode incompatible type
	def test_encode_wrong_type(self):
		with self.assertRaises(MalformedBencodeError):
			encode(None, False)

	# Decode silently
	def test_decode_malformed_silent(self):
		self.assertEqual(decode('abc'), None)

	# Decode malformed bencode raising an exception
	def test_decode_malformed_raise(self):
		with self.assertRaises(MalformedBencodeError):
			decode('rai', False)

	# Negative Number
	def test_negative_int(self):
		self.assertEqual(match_int('i-123e')[0], -123)

	# Encode dictionary with non string keys
	def test_encode_dict_non_string_key(self):
		with self.assertRaises(MalformedBencodeError):
			encode({123: '123'}, False)

def run_tests():
	unittest.main(module=__name__)
