#This is a program to automate creating lined a sound out activity I use for teaching
#Louis Faunce - made 06/20/2025 - edtied 03/27/2026 for web app version
import random
import re
from collections.abc import Sequence
from pyApp import logger

#------------------------------------------------------------------------------
#section for basic variables
p2k = None #initializing the phoneme to kana converter
g2p = None #initializing the g2p converter (assists with converting words to phonemes for the p2k converter)
kanaList = [] 
soundOutList = [] 
#-------------------------------------------------------------------------------
def getConvert():
    global g2p, p2k
    if g2p is None:
        from g2p_en import G2p 
        g2p = G2p()
    if p2k is None:
        from e2k import P2K #importing e2k phoneme to kana converter
        p2k = P2K()
    return g2p, p2k

def randomSpelling(wordList): 

    randomList = wordList.copy() #copies the original list to a new list for randomization
    for i in range(len(randomList)): 
        original = randomList[i]
        try: #should handle errors.. right..
            if not isinstance(original, Sequence) or not original:
                raise ValueError(f"Invalid input: {original}")

            randomized = ''.join(random.sample(original, len(original)))
            attempts = 0
            while randomized == original:
                randomized = ''.join(random.sample(original, len(original)))
                attempts += 1
            
            randomList[i] = randomized
        
        except Exception as e:
            logger.error(f"randomSpelling failed with word '{original}' at index {i}: {e}")
            randomList[i] = original
        
    return randomList

def katakanaize(wordList): #turn og list to kana
    g2p, p2k = getConvert()
    kanaList = []
    for word in wordList:
        try:
            phonemes = g2p(word)
            katakana = p2k(phonemes)
            kanaList.append(katakana)
        except Exception as e:
            #print(f"DEBUG: Failed to convert '{word}': {e}")
            kanaList.append(word)
        
    return kanaList 


#------------------------------------------------------------------------------

def processWordsWithLevels(levelsDict): #for processing words with levels

    soundOutList = []
    kanaList = []
    randomList = soundOutList.copy()

    for level in ["level1", "level2", "level3", "level4", "level5"]:
        wordStr = levelsDict.get(level, "").strip()
        if wordStr:
            words = [w.strip() for w in re.split(r'[\n,;]+', wordStr) if w.strip()]
            soundOutList.extend(words)
            
    #make randomize spelling and kana list
    randomList = randomSpelling(soundOutList)
    kanaList = katakanaize(soundOutList)
    
    return{
        "level1":{
            "randomizedWords": randomList[0:4],
            "kana": kanaList[0:4]
        },
        "level2":{
            "randomizedWords": randomList[4:8],
            "kana": kanaList[4:8]  
        },
        "level3":{
            "randomizedWords": randomList[8:12],
            "kana": kanaList[8:12]
        },
        "level4":{
            "randomizedWords": randomList[12:16],
            "kana": kanaList[12:16]
        },
        "level5":{
            "randomizedWords": randomList[16:18],
            "kana": kanaList[16:18]
        }
    }

def formatTextOutput(results): #sets the text up for the results page
    lines = []

    levels = [ 
        ("level1", "Level 1:"),
        ("level2", "Level 2:"),
        ("level3", "Level 3:"),
        ("level4", "Level 4:"),
        ("level5", "Level 5:")
    ]

    for key, title in levels:
        lines.append(title)
        words = results[key]["randomizedWords"]
        kana = results[key]["kana"]
        for i, (word, kana_text) in enumerate(zip(words, kana), start = 1):
            lines.append(f"{kana_text} - {word}")
        lines.append("") #adds blank line

    return "\n".join(lines)

