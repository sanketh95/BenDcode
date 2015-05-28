from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.rst')) as f:
	long_description = f.read()

setup(
	name='bendcode',
	version='1.1.0',

	description='Python module to decode Bencoded data',
	long_description=long_description,
	url='https://github.com/sanketh95/BenDcode',

	author='Sanketh Mopuru',
	author_email='sanketh.mopuru@gmail.com',

	license='GPLv2',

	keywords=['bencoding', 'bittorrent', 'decoding', 'encoding'],
	packages=['bendcode'],


	classifiers=[
		'Development Status :: 5 - Production/Stable',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
	]

)