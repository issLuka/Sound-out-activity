from PIL import Image, ImageDraw, ImageFont
import math
import copy

soundOutDesign = Image.open("../png/soundoutActivityBulbasaur.png")
draw = ImageDraw.Draw(soundOutDesign)


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
boxDistanceListY1 = [634, 644, 630, 646] 
levelFiveToLevelOneYDistance = 2560

def drawTextBox(questionsDictionary, DistanceListy1):
    
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
            for i in range(4):
                i += 1
                #print("level1 " + str(i))
                draw.rectangle(levelsBoxes[i], outline="black")
            for i in range(2):
                i += 1
                levelFiveBoxes = {1: [(levelsBoxes[1][0][0], levelsBoxes[1][0][1] + levelFiveToLevelOneYDistance), (levelsBoxes[1][1][0], levelsBoxes[1][1][1] + levelFiveToLevelOneYDistance)],
                                2: [(levelsBoxes[2][0][0], levelsBoxes[2][0][1] + levelFiveToLevelOneYDistance), (levelsBoxes[2][1][0], levelsBoxes[2][1][1] + levelFiveToLevelOneYDistance)]}
                draw.rectangle(levelFiveBoxes[i], outline="black")
        elif boxCount >= 3 and boxCount <= 15: #FOR LEVELS 2 3 AND 4
            while boxCount >=4 and boxCount <= 7:
                boxCount += 1
                boxNKey = boxCount - 4 #the value of the key the for the box that needs (lowkey jank but works so leave, goes 1 2 3 4)
                level2YCoord = [levelsBoxes[boxNKey][0][1] + questionDistancesY1[0], levelsBoxes[boxNKey][1][1] + questionDistancesY1[0]]
                levelsBoxes[boxNKey] = [(levelsBoxes[boxNKey][0][0], level2YCoord[0]), (levelsBoxes[boxNKey][1][0], level2YCoord[1])]
                levelTwoBoxes = copy.copy(levelsBoxes)
                draw.rectangle(levelsBoxes[boxNKey], outline="black")
            while boxCount >= 8 and boxCount <= 11:
                boxCount += 1
                boxNKey = boxCount - 8
                level3YCoord = [levelsBoxes[boxNKey][0][1] + questionDistancesY1[1], levelsBoxes[boxNKey][1][1] + questionDistancesY1[1]]
                levelsBoxes[boxNKey] = [(levelsBoxes[boxNKey][0][0], level3YCoord[0]), (levelsBoxes[boxNKey][1][0], level3YCoord[1])]
                levelThreeBoxes = copy.copy(levelsBoxes)
                draw.rectangle(levelsBoxes[boxNKey], outline="black")
            while boxCount >= 12 and boxCount <= 15:
                boxCount += 1
                boxNKey = boxCount - 12
                level4YCoord = [levelsBoxes[boxNKey][0][1] + questionDistancesY1[2], levelsBoxes[boxNKey][1][1] + questionDistancesY1[2]]
                levelsBoxes[boxNKey] = [(levelsBoxes[boxNKey][0][0], level4YCoord[0]), (levelsBoxes[boxNKey][1][0], level4YCoord[1])]
                levelFourBoxes = copy.copy(levelsBoxes)
                draw.rectangle(levelsBoxes[boxNKey], outline="black")
    return levelTwoBoxes, levelThreeBoxes, levelFourBoxes, levelFiveBoxes

drawTextBox(questionBoxDict, boxDistanceListY1)
#print(levelOneBoxes, "\n", levelTwoBoxes, "\n", levelThreeBoxes, "\n", levelFourBoxes, "\n", levelFiveBoxes)

def fitSingleLine(draw, text, box, font_path, maxSize=100):
    (x1, y1), (x2, y2) = box
    box_width = x2 - x1
    box_height = y2 - y1

    font_size = maxSize

    while font_size > 5:
        font = ImageFont.truetype(font_path, font_size)

        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        if text_width <= box_width and text_height <= box_height:
            return font, text_width, text_height

        font_size -= 1

    return font, text_width, text_height
    
def drawText(words):

    wordsList = words
    testWord = wordsList[0]
    box = questionBoxDict[1]

    
    fontSize = 100
    font, textWidth, textHeight = fitSingleLine(draw, testWord, box, "../japaneseMonospace.ttf", maxSize = 100)

    (x1, y1), (x2, y2) = box

    x = box[0][0]
    y = box[0][1]
    

    #drawTextBox(questionBoxDict, boxDistanceListY1)

    draw.text((x, y), testWord, font = font, fill = "black", encoding = "UTF-8")

wordTestList = ["ネーバリング - bihnirnggeooooooooo", "test"]
drawText(wordTestList)



soundOutDesign.save("../png/soundoutActivityBulbasaurWithText.png")
