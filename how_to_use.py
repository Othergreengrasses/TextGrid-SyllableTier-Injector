# Sample python script to demonstrate how to use the Text Grid Syllable Tier Injector Tool
from textGridSyllableTierInjector import insertSyllableTierInTextGrid

#insertSyllableTierInTextGrid('TextGrid/sample-librispeech.TextGrid','TextGrid/sample-librispeech.withSyllableTier.TextGrid')
insertSyllableTierInTextGrid('TextGrid/missingWords.TextGrid','TextGrid/missingWords.withSyllableTier.TextGrid')
