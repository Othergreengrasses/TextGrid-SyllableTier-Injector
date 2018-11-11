# TextGrid-SyllableTier-Injector
This library takes an English Forced Aligned textgrid and adds a Syllable tier beased on the phones present in it.  

## Project Scope  
Speach to Text Forced Aligner tools like [Montreal Forced Aligner](https://github.com/MontrealCorpusTools/Montreal-Forced-Aligner) generates output as a [TextGrid](http://www.fon.hum.uva.nl/praat/manual/TextGrid_file_formats.html) file which can be viewed using [Pratt](http://projects.chass.utoronto.ca/ngn/pdf/TextGrid_creation_Praat.pdf).

Generally Forced Aligned TextGrid contains information about phones. However, for prosidic analysis of speech corpus **syllable** information in the forced align TextGrid becaomes very useful. 

This library allows users to add an extra tier in Forced Aligned textgrid that contains Syllable information. The library currently works for english.

## Getting Started

Clone the project and refer [how_to_use.py](how_to_use.py) for sample code of how to use. 

You can also use the following code for the same.

```
# Sample python script to demonstrate how to use the Text Grid Syllable Tier Injector Tool
from textGridSyllableTierInjector import insertSyllableTierInTextGrid

#insertSyllableTierInTextGrid('TextGrid/sample-librispeech.TextGrid','TextGrid/sample-librispeech.withSyllableTier.TextGrid')
insertSyllableTierInTextGrid('<Input Forced Aligned TextGrid file name>','<Output TextGrid file name>')

```

### Prerequisites

This library depends on the following libraries

- [tqdm](https://pypi.org/project/tqdm/)
- [TextGrid](https://github.com/kylebgorman/textgrid)

### Installing

Intall tqdm - 
```
pip install tqdm
```
Intall TextGrid

```
pip install textgrid
```

End with an example of getting some data out of the system or using it for a little demo

## Running the script

Execute the how to use python file.

```
python how_to_use.py
```

## Authors

**Arundhati Sengupta** - *Initial work* - [Othergreengrasses](https://github.com/Othergreengrasses)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Ackowledgements
[CMU Dict](https://webdocs.cs.ualberta.ca/~kondrak/cmudict.html) - Susan Bartlett, Grzegorz Kondrak and Colin Cherry. On the Syllabification of Phonemes. NAACL-HLT 2009
[TextGrid]()

