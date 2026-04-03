from PIL import Image, ImageDraw, ImageFont
import copy

imageBulb = Image.open("../png/soundoutActivityBulbasaur.png")
imageChar = Image.open("../png/soundoutActivityCharmander.png")
imageSquirt = Image.open("../png/soundoutActivitySquirtle.png")

def userChoice(input):

    if input == "styleBulb":
        soundoutDesign = imageBulb
        return soundoutDesign
    elif input == "styleCharmander":
        soundoutDesign = imageChar
        return soundoutDesign
    elif input == "styleSquirtle":
        soundoutDesign = imageSquirt
        return soundoutDesign


textBoxWidth, textBoxHeight = 1010, 70 
questionBoxDict = {1: [(275, 497), (275 + textBoxWidth, 497 + textBoxHeight)], 
                2: [(1375, 497), (1375 + textBoxWidth, 497 + textBoxHeight)], 
                3: [(275, 817), (275 + textBoxWidth, 817 + textBoxHeight)], 
                4: [(1375, 817), (1375 + textBoxWidth, 817 + textBoxHeight)]}

levelOneBoxes = copy.deepcopy(questionBoxDict)
levelTwoBoxes = {}
levelThreeBoxes = {}
levelFourBoxes = {}
levelFiveBoxes = {}

#0 is levelOne to levelTwo, 1 is levelTwo to levelThree, 2 is levelThree to levelFour, 3 is levelFour to levelFive
boxDistanceListY1 = [634, 644, 625, 646] 
levelFiveToLevelOneYDistance = 2555

def drawTextBox(questionsDictionary, DistanceListy1, draw):
    
    global levelTwoBoxes
    global levelThreeBoxes
    global levelFourBoxes
    global levelFiveBoxes

    boxCount = 0

    questionDistancesY1 = DistanceListy1.copy()

    levelsBoxes = copy.deepcopy(questionsDictionary)

    while boxCount <= 15:
        boxCount += 1
        if boxCount <= 3: #FOR LEVELS 1 AND 5
            #for i in range(4):
                #i += 1
                #print("level1 " + str(i))
                #draw.rectangle(levelsBoxes[i])
            for i in range(2):
                i += 1
                levelFiveBoxes = {1: [(levelsBoxes[1][0][0], levelsBoxes[1][0][1] + levelFiveToLevelOneYDistance), (levelsBoxes[1][1][0], levelsBoxes[1][1][1] + levelFiveToLevelOneYDistance)],
                                2: [(levelsBoxes[2][0][0], levelsBoxes[2][0][1] + levelFiveToLevelOneYDistance), (levelsBoxes[2][1][0], levelsBoxes[2][1][1] + levelFiveToLevelOneYDistance)]}
                draw.rectangle(levelFiveBoxes[i])
        elif boxCount >= 3 and boxCount <= 15: #FOR LEVELS 2 3 AND 4
            while boxCount >=4 and boxCount <= 7:
                boxCount += 1
                boxNKey = boxCount - 4 #the value of the key the for the box that needs (lowkey jank but works so leave, goes 1 2 3 4)
                level2YCoord = [levelsBoxes[boxNKey][0][1] + questionDistancesY1[0], levelsBoxes[boxNKey][1][1] + questionDistancesY1[0]]
                levelsBoxes[boxNKey] = [(levelsBoxes[boxNKey][0][0], level2YCoord[0]), (levelsBoxes[boxNKey][1][0], level2YCoord[1])]
                levelTwoBoxes = copy.copy(levelsBoxes)
                draw.rectangle(levelsBoxes[boxNKey])
            while boxCount >= 8 and boxCount <= 11:
                boxCount += 1
                boxNKey = boxCount - 8
                level3YCoord = [levelsBoxes[boxNKey][0][1] + questionDistancesY1[1], levelsBoxes[boxNKey][1][1] + questionDistancesY1[1]]
                levelsBoxes[boxNKey] = [(levelsBoxes[boxNKey][0][0], level3YCoord[0]), (levelsBoxes[boxNKey][1][0], level3YCoord[1])]
                levelThreeBoxes = copy.copy(levelsBoxes)
                draw.rectangle(levelsBoxes[boxNKey])
            while boxCount >= 12 and boxCount <= 15:
                boxCount += 1
                boxNKey = boxCount - 12
                level4YCoord = [levelsBoxes[boxNKey][0][1] + questionDistancesY1[2], levelsBoxes[boxNKey][1][1] + questionDistancesY1[2]]
                levelsBoxes[boxNKey] = [(levelsBoxes[boxNKey][0][0], level4YCoord[0]), (levelsBoxes[boxNKey][1][0], level4YCoord[1])]
                levelFourBoxes = copy.copy(levelsBoxes)
                draw.rectangle(levelsBoxes[boxNKey])
    return levelTwoBoxes, levelThreeBoxes, levelFourBoxes, levelFiveBoxes


def fitSingleLine(draw, text, box, font_path, maxSize=100):
    (x1, y1), (x2, y2) = box
    box_width = x2 - x1
    box_height = y2 - y1

    font_size = maxSize

    while font_size > 10:
        font = ImageFont.truetype(font_path, font_size)

        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        if text_width <= box_width and text_height <= box_height:
            return font, text_width, text_height

        font_size -= 1

    return font, text_width, text_height
    
def drawText(words, draw, soundoutDesign):

    drawTextBox(questionBoxDict, boxDistanceListY1, soundoutDesign)

    levelsDict = {(i+1):v for i, v in enumerate([questionBoxDict, levelTwoBoxes, levelThreeBoxes, levelFourBoxes, levelFiveBoxes])}

    wordsList = words

    for dictCount in range(len(levelsDict)): #loops thru all boxes

        dictCount += 1
        box = levelsDict[dictCount]

        for i in range(len(wordsList["Level"+str(dictCount)])): #loops thru each level

            key = i + 1
            testWord = wordsList["Level"+str(dictCount)][i]
            boxList = box[key]
            font, textWidth, textHeight = fitSingleLine(draw, testWord, boxList, "../japaneseMonospace.ttf", maxSize = 100)

            x = boxList[0][0]
            y = boxList[1][1]
            
            draw.text((x, y), testWord, font = font, anchor = "ls", fill = "black", encoding = "UTF-8")

    

def imageGeneration(input, words):

    soundoutDesign = userChoice(input)

    draw = ImageDraw.Draw(soundoutDesign)

    drawText(words, draw, soundoutDesign)
    soundoutDesign.save("../png/soundoutActivityFinal.png")



