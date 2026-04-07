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
        original = randomList[i]
        randomized = ''.join(random.sample(original, len(original)))

        while randomized == original:
            randomized = ''.join(random.sample(original, len(original)))
        randomList[i] = randomized
        
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

