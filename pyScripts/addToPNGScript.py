from PIL import Image, ImageDraw, ImageFont
import math
import copy

soundOutDesign = Image.open("../png/soundoutActivityBulbasaur.png")
draw = ImageDraw.Draw(soundOutDesign)

textBoxWidth, textBoxHeight = 1010, 70 #initializes global size of the txt box
questionBoxDict = {1: [(275, 497), (275 + textBoxWidth, 497 + textBoxHeight)], 
                2: [(1375, 497), (1375 + textBoxWidth, 497 + textBoxHeight)], 
                3: [(275, 817), (275 + textBoxWidth, 817 + textBoxHeight)], 
                4: [(1375, 817), (1375 + textBoxWidth, 817 + textBoxHeight)]}

#0 is levelOne to levelTwo, 1 is levelTwo to levelThree, 2 is levelThree to levelFour, 3 is levelFour to levelFive
boxDistanceListY1 = [634, 642, 627, 646] 
levelFiveToLevelOneYDistance = 2567

def drawTextBox(questionsDictionary, DistanceListy1):
        
    boxCount = 0

    questionDistancesY1 = DistanceListy1.copy()

    levelsBoxes = copy.deepcopy(questionsDictionary)

    while boxCount <= 15:
        boxN = (boxCount+1)%4
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
                boxNKey = boxCount - 4 #the value of the key the for the box that needs (lowkey jank but works so leave)
            while boxCount >= 8 and boxCount <= 11:
                boxCount += 1
                boxNKey = boxCount - 8
                i = (boxCount-1)%4


    soundOutDesign.save("../png/soundoutActivityBulbasaurWithText.png")

drawTextBox(questionBoxDict, boxDistanceListY1)

font = ImageFont.truetype("../comicSans.ttf", 100)
text = "this is a test"
fontSize = 100
#size = None

#print ("question 1 x coordinates: " + str(questionBoxDict["question 1"][0][0] + 2) + " to " + str(questionBoxDict["question 1"][1][0]))
#print ("question 1 y coordinates: " + str(questionBoxDict["question 1"][0][1]) + " to " + str(questionBoxDict["question 1"][1][1]))
#ImageDraw.Draw(soundOutDesign).rectangle(questionBoxDict["question 1"], outline="black")
#ImageDraw.Draw(soundOutDesign).rectangle(questionBoxDict["question 2"], outline="black")
#ImageDraw.Draw(soundOutDesign).rectangle(questionBoxDict["question 3"], outline="black")
#ImageDraw.Draw(soundOutDesign).rectangle(questionBoxDict["question 4"], outline="black")
#soundOutDesign.save("../png/soundoutActivityBulbasaurWithText.png")