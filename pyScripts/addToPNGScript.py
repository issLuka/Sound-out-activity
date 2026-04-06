from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import copy, os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PNG_DIR = os.path.join(SCRIPT_DIR,"..", "png")
FONT_PATH = os.path.join(SCRIPT_DIR, "..", "KFhimaji.otf")

def userChoice(input):
    paths = {
        "styleBulb": os.path.join(PNG_DIR, "soundoutActivityBulbasaur.png"),
        "styleCharmander": os.path.join(PNG_DIR, "soundoutActivityCharmander.png"),
        "styleSquirtle": os.path.join(PNG_DIR, "soundoutActivitySquirtle.png")
    }
    if input not in paths:
        raise ValueError(f"Unkonwn design choice: {input}")
    return Image.open(paths[input]).copy()

textBoxWidth, textBoxHeight = 1010, 70 
questionBoxDict = {
    1: [(275, 497), (275 + textBoxWidth, 497 + textBoxHeight)], 
    2: [(1375, 497), (1375 + textBoxWidth, 497 + textBoxHeight)], 
    3: [(275, 817), (275 + textBoxWidth, 817 + textBoxHeight)], 
    4: [(1375, 817), (1375 + textBoxWidth, 817 + textBoxHeight)]
    }

levelOneBoxes = copy.deepcopy(questionBoxDict)
levelTwoBoxes = {}
levelThreeBoxes = {}
levelFourBoxes = {}
levelFiveBoxes = {}

#0 is levelOne to levelTwo, 1 is levelTwo to levelThree, 2 is levelThree to levelFour, 3 is levelFour to levelFive
boxDistanceListY1 = [634, 644, 625, 646] 
levelFiveToLevelOneYDistance = 2555

def drawTextBox(questionsDictionary, DistanceListy1, draw):
    
    levelTwoBoxes   = {}
    levelThreeBoxes = {}
    levelFourBoxes  = {}
    levelFiveBoxes  = {}

    boxCount = 0

    questionDistancesY1 = DistanceListy1.copy()

    levelsBoxes = copy.deepcopy(questionsDictionary)

    while boxCount <= 15:
        boxCount += 1
        if boxCount <= 3: #FOR LEVELS 1 AND 5
            for i in range(1,3):
                levelFiveBoxes[i] = [
                    (levelsBoxes[i][0][0], levelsBoxes[i][0][1] + levelFiveToLevelOneYDistance),
                    (levelsBoxes[i][1][0], levelsBoxes[i][1][1] + levelFiveToLevelOneYDistance),
                ]
                draw.rectangle(levelFiveBoxes[i])
        elif boxCount >= 3 and boxCount <= 15: #FOR LEVELS 2 3 AND 4
            while boxCount >=4 and boxCount <= 7:
                boxCount += 1
                k = boxCount - 4
                dy = questionDistancesY1[0]
                levelsBoxes[k] = [
                    (levelsBoxes[k][0][0], levelsBoxes[k][0][1] + dy),
                    (levelsBoxes[k][1][0], levelsBoxes[k][1][1] + dy),
                ]
                levelTwoBoxes = copy.copy(levelsBoxes)
                draw.rectangle(levelsBoxes[k])
            while boxCount >= 8 and boxCount <= 11:
                boxCount += 1
                k = boxCount - 8
                dy = questionDistancesY1[1]
                levelsBoxes[k] = [
                    (levelsBoxes[k][0][0], levelsBoxes[k][0][1] + dy),
                    (levelsBoxes[k][1][0], levelsBoxes[k][1][1] + dy),
                ]
                levelThreeBoxes = copy.copy(levelsBoxes)
                draw.rectangle(levelsBoxes[k])
            while boxCount >= 12 and boxCount <= 15:
                boxCount += 1
                k = boxCount - 12
                dy = questionDistancesY1[2]
                levelsBoxes[k] = [
                    (levelsBoxes[k][0][0], levelsBoxes[k][0][1] + dy),
                    (levelsBoxes[k][1][0], levelsBoxes[k][1][1] + dy),
                ]
                levelFourBoxes = copy.copy(levelsBoxes)
                draw.rectangle(levelsBoxes[k])

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
    
def drawText(words, draw, levelBoxes):
    
    levelTwoBoxes, levelThreeBoxes, levelFourBoxes, levelFiveBoxes = levelBoxes

    levelsDict = {
        1: questionBoxDict,
        2: levelTwoBoxes,
        3: levelThreeBoxes,
        4: levelFourBoxes,
        5: levelFiveBoxes,
    }

    for dictCount in range(1, 6): #loops thru all boxes

        box = levelsDict[dictCount]
        levelKey = f"level{dictCount}"
        levelWords = words[levelKey]

        displayItems = [
            f"{kana} - {word}"
            for kana, word in zip(levelWords["kana"], levelWords["randomizedWords"])
        ]

        for i, text in enumerate(displayItems):
            key = i + 1
            if key not in box:
                continue
            boxList = box[key]
            font, _, _= fitSingleLine(draw, text, boxList, FONT_PATH, maxSize = 100)

            x = boxList[0][0]
            y = boxList[1][1]
            
            draw.text((x, y), text, font = font, anchor = "ls", fill = "black", encoding = "UTF-8")

    

def imageGeneration(input, words):

    soundoutDesign = userChoice(input)
    draw = ImageDraw.Draw(soundoutDesign)

    levelBoxes = drawTextBox(questionBoxDict, boxDistanceListY1, draw)

    drawText(words, draw, levelBoxes)
    bytesVar = BytesIO()
    soundoutDesign.save(bytesVar, format="PNG")
    bytesVar.seek(0)
    return bytesVar



