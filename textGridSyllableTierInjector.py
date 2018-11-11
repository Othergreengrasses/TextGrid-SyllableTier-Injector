
# coding: utf-8

# In[5]:


from textgrid import TextGrid, Interval, IntervalTier
import glob, os
from tqdm import tqdm
import re
from datetime import datetime
#
# Copyright (c) 2018 Arundhati Sengupta, asengupta2@gradcenter.cuny.edu
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

word_not_found = {}
utterence_not_found = {}


class WordSyllablePhone(object):
    """
    This class hold a word and Syllable / Phone mapping for its multiple 
    utterences. 1 object of this class is created for each word in Dictonry file
    and a separate map has been created to hold wordText -> Object mapping.
    
    This has a function named getSyllebleFromPhones which does all the magic. 
    Send a list of Interval objects generated from Phone Tier in Text and it will 
    return you another list of Syllable tier. The return object can then be saved in Text grid 
    to create another layer.
    
    Data Structure
    
    word --
         |---- Utterence 1
                    |----- List of Phone Text (including Syllable Marker)
         |---- Utterence 2
                    |----- List of Phone Text (including Syllable Marker)
      
    """

    # Constructor. takes a word and list of phones for the first Utterence.
    def __init__(self,word,phoneList):
        self.word = word
        self.utterences = []
        self.utterences.append(removeInvalidPhones(phoneList))
        
    # If a word have more than one utterence, add that in the same word.    
    def addUtterence(self,phoneList):
        self.utterences.append(removeInvalidPhones(phoneList))

    # send the Interval list of phones and it will return another Interval list of Syllables. 
    def getSyllebleFromPhones(self,phones, fileNm):
        syllabelList = []
        global utterence_not_found
        if (len(phones) == 0):
            print "Some issues with file, blank phone ", fileNm
            return syllabelList
        
        for utterence in self.utterences:
            #print "Trying to match phone:", phones, " with Utterence", utterence 
            syllabelList = []
            dict_phone_index = 0
            txGrd_phone_index = 0
            start_time  = phones[0].minTime
            end_time  = 0.0
            syllableName = ''
            matchFail = False
            
            while (dict_phone_index  < len(utterence)):
                dictPhone  = utterence[dict_phone_index]
                
                #if syllable marker found, create a new Interval with start time, end time and combined mark
                if (dictPhone == '-'):
                    sylInterval = Interval(start_time, end_time, syllableName)
                    syllabelList.append(sylInterval)
                    syllableName = ''
                    dict_phone_index+=1
                    dictPhone  = utterence[dict_phone_index]
                    start_time = txGrdPhone.maxTime
                
                if (txGrd_phone_index >= len(phones)):
                    print "Some issues with file ", fileNm, " around the place", phones
                else:
                    txGrdPhone = phones[txGrd_phone_index]
                
                if (txGrdPhone.mark.strip() == dictPhone.strip()):
                    end_time = txGrdPhone.maxTime
                    syllableName += dictPhone
                else:
                    matchFail = True
                    break
                
                dict_phone_index+=1
                txGrd_phone_index+=1
            
            if (not matchFail):
                end_time = phones[len(phones)-1].maxTime
                sylInterval = Interval(start_time, end_time, syllableName)
                syllabelList.append(sylInterval)
                break #matched utterence
        
        if (matchFail):
            print "Could not match word", self.word , " with phone ", phones , " with Utterence", utterence, fileNm
            utterence_not_found[self.word] = phones
            start_time = phones[0].minTime 
            end_time = phones[len(phones)-1].maxTime
            syllabelList = [(Interval(start_time, end_time, self.word + '_unMatched'))]
          
        return syllabelList


#If any of the phone is blank, this removes that from list
def removeInvalidPhones(phones):
        cleanPhoneList = [p for p in phones if len(p) > 0]
        return cleanPhoneList
    
                
#Check whether the interval is marked as pause or not"
def isValidPhrase(minT,maxT,mak,maxTime):
    if mark == 'sp':
        if minT > 0.0 and maxT < maxTime:
            return True
    
    return False

# Takes a word and search in Text Grid file to return all phones (by searching Phone Tier) that 
# falls with in the minTime and maxTime of the Word
def getPhonesForWord(word, gridobj):
    #Search boundary in Phone Tier
    startTime = word.minTime
    endTime   = word.maxTime
    
    phones = [] 
    
    # Setting phone teir 
    phoneTier = gridobj.getFirst('phones')
    
    # Searching phone that falls with in that interval  
    for phone in phoneTier.intervals:
        if ((phone.minTime >= startTime) and (phone.maxTime <= endTime) and (len(phone.mark) > 0)):
            phones.append(phone)
            
        if phone.minTime > endTime:
            break
     
    return phones

def parseWordName(wordParam):
    word = re.sub(r"\([\d+]\)$",'', wordParam)
    return word
    
def generatePhoneSyllableRelationship(gridobj, dictMap, fileNm):
    syllable = []
    global word_not_found
    wordTier = gridobj.getFirst('words')
    
    #Get all the words and their associated times
    for word in wordTier.intervals:
        if not word.mark ==  '':
            phoneList = getPhonesForWord(word,gridobj) 
            word_text = word.mark.upper()
            if word_text in dictMap:
                wspObj = dictMap[word.mark.upper()]
                #Returns List of Syllables by mathing Time info from text grid with 
                # Syllable info from Dictionary
                sylIntervals = wspObj.getSyllebleFromPhones(phoneList, fileNm) 
                for interval in sylIntervals:
                    syllable.append(interval)
            else:
                word_not_found[word_text] = [p.mark for p in phoneList] # the word is not found in syllable dict.  
                syllable.append(Interval(word.minTime, word.maxTime,word_text+'_unknown'))
        
    return syllable
        
# Construct a WordPhoneSyllable Object for each row in Dict File.
# If there are more than one utterence of a word, existing word is reused.
def loadWordPhoneSyllableMap(dictFileName):
    dictFile = open(dictFileName)
    
    dictMap = {}
    
    for line in dictFile.readlines():
        line = line.strip('\n')
        if not line.startswith('#'):
            section = line.split(' ')
            word = parseWordName(section[0])
            phones = section[1:]
            
            if word in dictMap:
                wspObj = dictMap[word]
                wspObj.addUtterence(phones)
            else:        
                wspObj = WordSyllablePhone(word,phones)
            
            dictMap[word] = wspObj
     
    return dictMap


def saveSyllableInTextGrid(sylIntervals,gridobj,f):
    
    if len(sylIntervals)== 0: #No interval to save
        return
    
    minTime = sylIntervals[0].minTime                   #getting the min time for syllable tier
    maxTime = sylIntervals[len(sylIntervals)-1].maxTime #getting the max time for syllable tier
    
    syllableTier = IntervalTier('Syllable',minTime,maxTime)  #creating Tier 
    for interval in sylIntervals:
        syllableTier.addInterval(interval)
        
    gridobj.append(syllableTier) #appending Tier in text grid 
    gridobj.write(f)             # writing the new Text Grid 

#Reports the words and utterences that was not found in dictionary
def reportMissingWords(word_missing, utterence_missing, textGridFile):
    missingWordCount = len(word_missing)
    missingUtterenceCount = len(utterence_missing)
    report = ''
    
    if ((missingWordCount + missingUtterenceCount) > 0):
        report += "Time:" + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " File:" + textGridFile + '\n'
        
    if (missingWordCount > 0):
        report += 'Number of missing words:' + str(missingWordCount) + '\n'
        report += 'You can add these pairs in dict file (at proper place as the dict file maintains information in sorted order) and rerun the tool \n'
        for key, value in word_missing.iteritems():
            report += key + '\t' + ' '.join(value) + '\n'

    if (missingUtterenceCount > 0): 
        report += 'Number of words with unmatched utterence:', missingUtterenceCount, '\n'
        report += 'Following are the words and their different utterence (phone list) as encountered in text grid \n'
        for key, value in utterence_missing.iteritems():
            report += key + '\t' + ' '.join(value) + '\n'
           
    with open("missingWords.log", "a") as text_file:
        text_file.write(report)
    
    
def insertSyllableTierInTextGrid(inputFileName, outputFileName):
    global word_not_found
    global utterence_not_found

    # Step 1: Create the TextGrid Object
    gridobj = TextGrid().fromFile(inputFileName)

    # Step 2: Create the word to Dictionary information map
    dictMap = loadWordPhoneSyllableMap('dict/cmudict.rep')

    # Step 3: Combine the Text Grid Information and Dictionary Map to create Map( word -> List(syllable))  
    sylIntervals = generatePhoneSyllableRelationship(gridobj,dictMap, inputFileName)
    
    # Step 4: Add a new Tier in Text Grid file and Save it.
    saveSyllableInTextGrid(sylIntervals,gridobj, outputFileName)

    # Step 5: Generate log of missing words / phone
    reportMissingWords(word_not_found, utterence_not_found, inputFileName)

    
def insertSyllableTierForFilesInFolder(folderPath,outFolderPath):
    os.chdir(folderPath)
    for fileName in tqdm(glob.glob("*.TextGrid")):
        outfileName = outFolderPath + '/' + fileName + '.out.TextGrid'
        fileName = folderPath + '/'+fileName
        insertSyllableTierInTextGrid(fileName, outfileName )

