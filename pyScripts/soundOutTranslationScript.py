#This is a program to automate creating lined a sound out activity I use for teaching
#Louis Faunce - made 06/20/2025 - edtied 03/27/2026 for web app version
import random
import re
from e2k import P2K #importing e2k phoneme to kana converter
from g2p_en import G2p 

#------------------------------------------------------------------------------
#section for basic variables
p2k = P2K() #initializing the phoneme to kana converter
g2p = G2p() #initializing the g2p converter (assists with converting words to phonemes for the p2k converter)
kanaList = [] 
soundOutList = [] 
#-------------------------------------------------------------------------------

def randomSpelling(wordList): 

    randomList = wordList.copy() #copies the original list to a new list for randomization
    for i in range(len(randomList)): 
        randomList[i]= ''.join(random.sample(randomList[i],len(randomList[i]))) #randomizes the spelling of each word in the list by shuffling the letters

    return randomList

def katakanaize(wordList): #turn og list to kana

    kanaList = []
    for word in wordList:
        try:
            katakana = p2k(g2p(word))
            kanaList.append(katakana)
        except:
            kanaList.append(word)
        
    return kanaList 


#------------------------------------------------------------------------------

def processWordsWithLevels(levelsDict): #for processing words with levels

    soundOutList = []
    kanaList = []
    randomList = soundOutList.copy()

    for level in ["level1", "level2", "level3", "level4", "level5"]:
        words_str = levelsDict.get(level, "").strip()
        if words_str:
            words = [w.strip() for w in re.split(r'[\n,;]+', words_str) if w.strip()]
            soundOutList.extend(words)
            
    #make randomize spelling and kana list
    randomList = randomSpelling(soundOutList)
    kanaList = katakanaize(soundOutList)
    
    return{
        "levelOne":{
            "randomizedWords": randomList[0:4],
            "kana": kanaList[0:4]
        },
        "levelTwo":{
            "randomizedWords": randomList[4:8],
            "kana": kanaList[4:8]  
        },
        "levelThree":{
            "randomizedWords": randomList[8:12],
            "kana": kanaList[8:12]
        },
        "levelFour":{
            "randomizedWords": randomList[12:16],
            "kana": kanaList[12:16]
        },
        "levelFive":{
            "randomizedWords": randomList[16:18],
            "kana": kanaList[16:18]
        }
    }

def formatTextOutput(results): #sets the text up for the results page
    lines = []

    levels = [ 
        ("levelOne", "level 1 words:"),
        ("levelTwo", "level 2 words:"),
        ("levelThree", "level 3 words:"),
        ("levelFour", "level 4 words:"),
        ("levelFive", "level 5 words:")
    ]

    for key, title in levels:
        lines.append(title)
        words = results[key]["randomizedWords"]
        kana = results[key]["kana"]
        for i, (word, kana_text) in enumerate(zip(words, kana), start = 1):
            lines.append(f"{i}. {kana_text} - {word}")
        lines.append("") #adds blank line

    return "\n".join(lines)

