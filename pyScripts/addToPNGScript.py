from PIL import Image, ImageDraw, ImageFont
import math

soundOutDesign = Image.open("../png/soundoutActivityBulbasaur.png")
draw = ImageDraw.Draw(soundOutDesign)

textBoxWidth, textBoxHeight = 1010, 70 #initializes global size of the txt box
box = [(280, 497), (280 + textBoxWidth, 497 + textBoxHeight)] #initializes the coordinates of the first box (leve1 question 1s TL)
box2 = [(1380, 497), (1380 + textBoxWidth, 497 + textBoxHeight)] #initializes the coordinates of the second box (level 1 question 2s TL)

levelOneToTwoDistance = 244
levelTwoToThreeDistance = 257
LevelThreeToFourDistance = 240
levelFourToFiveDistance = 256

boxCount = 0


font = ImageFont.truetype("../comicSans.ttf", 100)
text = "this is a test"
fontSize = 100
#size = None


ImageDraw.Draw(soundOutDesign).rectangle(box, outline="black")
ImageDraw.Draw(soundOutDesign).rectangle(box2, outline="black")
soundOutDesign.save("../png/soundoutActivityBulbasaurWithText.png")