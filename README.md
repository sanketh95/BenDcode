# BenDcode

A python module for decoding bencoded data

[![Code Climate](https://codeclimate.com/repos/5566f91269568069910046e8/badges/ea390c0dd7d6d1b5e688/gpa.svg)](https://codeclimate.com/repos/5566f91269568069910046e8/feed)
[![Travis CI](https://api.travis-ci.org/sanketh95/BenDcode.svg)](https://travis-ci.org/sanketh95/BenDcode)
[![Coverage Status](https://coveralls.io/repos/sanketh95/BenDcode/badge.svg?branch=master)](https://coveralls.io/r/sanketh95/BenDcode?branch=master)
[![PyPi Version](https://img.shields.io/pypi/v/bendcode.svg)](https://pypi.python.org/pypi/bendcode)

## Bencoding

Bencoding is a meta data representation format fot the BitTorrent Protocol (BTP). 
The Augmented BNF syntax for Bencoding is given below

```
 dictionary = "d" 1*(string anytype) "e" 
   list       = "l" 1*anytype "e"
   integer    = "i" signumber "e"
   string     = number ":" <number long sequence of any CHAR>
   anytype    = dictionary / list / integer / string
   signumber  = "-" number / number
   number     = 1*DIGIT
   CHAR       = %x00-FF 
   DIGIT      = "0" / "1" / "2" / "3" / "4" /
                "5" / "6" / "7" / "8" / "9"
```
**Source:** [BTP RFC](http://jonas.nitro.dk/bittorrent/bittorrent-rfc.html)

## Installation

Using pip

`pip install bendcode`

Manual Installation

```
git clone https://github.com/sanketh95/BenDcode
cd BenDcode
python setup.py install
```

## Usage

Decoding bencoded data is simple.

```
>>> import bendcode
>>> bendcode.decode('i123e')
123
>>> bendcode.decode('4:John')
'John'
>>> bendcode.decode('li234ei123ee')
[234, 123]
>>> bendcode.decode('d1:ai123e1:bi234ee')
{'a': 123, 'b': 234}
```

You can decode invidual types too !

```
>>> import bendcode
>>> bendcode.match_string('3:abc')
('abc', '')
>>> bendcode.match_int('i-123e')
(-123, '')
>>> bendcode.match_list('li123ee')
([123], '')
>>> bendcode.match_dict('d1:a1:bei123e')
({'a': 'b'}, 'i123e')
```

**Note:** The match_* series of functions return a tuple `(first_possbile_match, remaining_unmatched_string)`

**Bendcode** can encode too 

```
>>> import bendcode
>>> bendcode.encode(123)
'i123e'
>>> bendcode.encode('John')
'4:John'
>>> bendcode.encode([123, 'bro'])
'li123e3:broe'
>>> bendcode.encode({'hello': 123})
'd5:helloi123ee'
>>> bendcode.encode(None)
''
```

You decide whether to raise an exception or not for any functions mentioned above by setting the `fail_silently` parameter to `True` or `False`

```
>>> import bendcode
>>> bendcode.match_string('abc')
(None, 'abc')
>>> bendcode.match_string('abc', fail_silently=False)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "bendcode\bendcode.py", line 39, in match_string
    raise MalformedBencodeError('Failed to match string in ' + str(raw))
bendcode.exceptions.MalformedBencodeError: Failed to match string in abc
```

## Tests

Run tests using the following code

```
>>> from bendcode import tests
>>> tests.run_tests()
..................................
----------------------------------------
Ran 34 tests in 0.015s

OK
```

## Issues

If you find any bug, feel free to create an issue [here](https://github.com/sanketh95/BenDcode/issues).

## License

BenDcode uses GNU v2 License. Read the terms of the license [here](LICENSE.txt).