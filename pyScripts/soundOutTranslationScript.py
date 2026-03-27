#This is a program to automate creating lined a sound out activity I use for teaching
#Louis Faunce - made 06/20/2025 - edtied 03/27/2026 for web app version
import random
import re
from e2k import P2K #importing e2k phoneme to kana converter
from g2p_en import G2p #gets g2p library

#------------------------------------------------------------------------------
#section for basic variables
p2k = P2K() #initializing the phoneme to kana converter
g2p = G2p() #initializing the g2p converter
kanaList = [] #sets up list for pronunciations
soundOutList = [] #sets up list for words
#------------------------------------------------------------------------------
pathOut = './txtFiles/soundOutput.txt' #path to the output file, change if needed

def getWords(): #function to get words from user input

    counter = 0
    space = True

    while counter <= 17:
        
        counter += 1

        wordInput = input(f"Enter word {counter}: ") #asks user for input of words, change range if needed
        if wordInput == "": #if the user inputs nothing, it will stop asking for more words
            break
        elif space != bool(re.search(r"\s", wordInput)):
            soundOutList.append(wordInput) #adds the word to the list if there are no spaces
        else: 
            #if the user inputs a word with a space, it will ask for a new word
            print("Please enter a single word without spaces.")
            counter -= 1 #decrements the counter to allow for a new word input

    return soundOutList #returns the list of words
    
randomizeList = soundOutList.copy() #sets up list for randomized words copying og list

#-------------------------------------------------------------------------------

def randomSpelling(wordList): #self explanatory function to randomize the words in the list

    randomList = wordList.copy() #copies the original list to a new list for randomization
    for i in range(len(randomList)): #loops through each word in the list and randomizes
        randomizeList[i] = ''.join(random.sample(randomList[i],len(randomizeList[i])))

    return randomizeList #returns the randomized list

def katakanaize(wordList): #turn og list to kana

    kanaList = []
    for word in wordList:
        try:
            katakana = p2k(g2p(word))
            kanaList.append(katakana)#loops through each word in the list
        except:
            kanaList.append(word)
        
    return kanaList #returns the kana list


#------------------------------------------------------------------------------

def processWordsWithLevels(levelsDict): #section for processing words with levels

    soundOutList = [word for words in levelsDict.values() for word in words]
    kanaList = []
    randomList = soundOutList.copy()

    for level in ["level1", "level2", "level3", "level4", "level5"]:
        words_str = levelsDict.get(level, "").strip()
        if words_str:
            words = [w.strip() for w in re.split(r'[\n,;]+', words_str) if w.strip()]
            soundOutList.extend(words)
            
    #make randomize spelling and kana list
    randomList = randomSpelling(soundOutList)
    pronunciationList = katakanaize(soundOutList)
    
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

def printTests(): #tests to make sure lists work
    
    print("Sound Out Activity Words:", *soundOutList) #prints header
    print("Level 1 Words: ", *levelOneWords, *levelOneKana) #prints level 1 words
    print("Level 2 Words: ", *levelTwoWords, *levelTwoKana) #prints level 2 words
    print("Level 3 Words: ", *levelThreeWords, *levelThreeKana) #prints level 3 words
    print("Level 4 Words: ", *levelFourWords, *levelFourKana) #prints level 4 words
    print("Level 5 Words: ", *levelFiveWords, *levelFiveKana) #prints level 5 words

def printFinalText():

    with open(pathOut, "w", encoding='utf8') as file: #writes the words and kana to a new file
        file.write("level 1 words:\n")
        for i in range(len(levelOneWords)):
            levelCounter += 1 #increments the level counter
            file.write(f"{levelCounter}. {levelOneKana[i]} ・ {levelOneWords[i]}\n") #writes the level 1 words and kana to the file
            if levelCounter >= 4:
                levelCounter = 0 
        file.write("\nlevel 2 words:\n")
        for i in range(len(levelTwoWords)):
            levelCounter += 1
            file.write(f"{levelCounter}. {levelTwoKana[i]} ・ {levelTwoWords[i]}\n")
            if levelCounter >= 4:
                levelCounter = 0 
        file.write("\nlevel 3 words:\n")
        for i in range(len(levelThreeWords)):
            levelCounter += 1
            file.write(f"{levelCounter}. {levelThreeKana[i]} ・ {levelThreeWords[i]}\n")  
            if levelCounter >= 4:
                levelCounter = 0 
        file.write("\nlevel 4 words:\n")
        for i in range(len(levelFourWords)):
            levelCounter += 1
            file.write(f"{levelCounter}. {levelFourKana[i]} ・ {levelFourWords[i]}\n")
            if levelCounter >= 4:
                levelCounter = 0 
        file.write("\nlevel 5 words:\n")
        for i in range(len(levelFiveWords)):
            levelCounter += 1
            file.write(f"{levelCounter}. {levelFiveKana[i]} ・ {levelFiveWords[i]}\n")
        file.write("\n")

