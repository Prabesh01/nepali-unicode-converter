# Nepali Unicode Converter

A tool to convert Romanized text to corresponding Nepali unicode and vice versa.



## Installation

`pip install git+https://github.com/Prabesh01/nepali-unicode-converter`



## Usage
```python
from nepali_unicode_converter.convert import Converter
from nepali_unicode_converter.convert import ReverseConverter
from nepali_unicode_converter.convert import ReverseConverterV2

converter = Converter()
rev = ReverseConverter()
rev2 = ReverseConverterV2()

mystring = 'ke chha hajura?'
print(converter.convert(mystring))  ## Output: 'के छ हजुर?'

mystring = 'फेरी आयो यो भालु! '
print(rev.convert(mystring)) ## Output: 'feree aayo yo vaalu!'
print(rev2.convert(mystring)) ## Output: 'pheree aayo yo bhaalu!'

# smart mode. insprired from https://github.com/isDipesh/nepali-romanization
smart_rev = ReverseConverter(smart=True)
smart_rev2 = ReverseConverterV2(smart=True)
print(smart_rev.convert(mystring)) ## Output: 'feri aayo yo vaalu'
print(smart_rev.convert(mystring)) ## Output: 'pheri aayo yo bhaalu'
```


## Mapping Table

### Basic vowels
| Roman | Unicode | Roman | Unicode |
|------:|--------:|------:|--------:|
|   a   | अ       |   oo  | ऊ       |
|   aa  | आ       |   Ri  | ॠ       |
|   ee  | ई       |   Ree | ॠ       |
|   i   | इ       |   e   | ए       |
|   u   | उ       |   ai  | ऐ       |
|   o   | ओ       |


### Basic Akaars
| Roman | Unicode | Roman | Unicode | Roman | Unicode |
|------:|--------:|------:|--------:|------:|--------:|
|  ka   |   क     |  Ta   |   ट     |  pa   |   प     |
|  kha  |   ख     |  Tha  |   ठ     |  pha  |   फ     |
|  ga   |   ग     |  Da   |   ड     |  fa   |   फ     |
|  gha  |   घ     |  Dha  |   ढ     |  ba   |   ब     |
|  Nga  |   ङ     |  Na   |   ण     |  bha  |   भ     |
|  NGa  |   ङ्ग    |  ta   |   त     |  va   |   भ     |
|  cha  |   च     |  tha  |   थ     |  ma   |   म     |
|  chha |   छ     |  da   |   द     |  ya   |   य     |
|  ja   |   ज     |  dha  |   ध     |  ra   |   र     |
|  jha  |   झ     |  na   |   न     |  la   |   ल     |
|  yNa  |   ञ     |  pa   |   प     |  sha  |   श     |
|  wa   |   व     |  sa   |   स     |  Sha  |   ष     |
|  ha   |   ह     |  ksha |   क्ष    |  tra  |   त्र    |
|  gya  |   ज्ञ    |  gYa  |   ग्य    |

### Halantas
Just omit the 'a' at the end.


### Kaar and other suffixes
| Roman | Unicode |
|-------:|-------:|
|   kaa  | का      |
|   ki   | कि      |
|   kee  | की      |
|   ku   | कु      |
|   koo  | कू      |
|   ke   | के      |
|   kai  | कै      |
|   ko   | को      |
|   kau  |  कौ     |
|   kaM  | कं      |
|   kaNN | कँ      |
|   ka:  | क:     |
|   mRI  | मृ      |


### Numbers
There is a natural mapping.


## TODO
- [ ] Make it more intelligent.
