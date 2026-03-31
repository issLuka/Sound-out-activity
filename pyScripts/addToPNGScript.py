from PIL import Image, ImageDraw, ImageFont
import math

soundOutDesign = Image.open("../png/soundoutActivityBulbasaur.png")
draw = ImageDraw.Draw(soundOutDesign)
textBoxWidth, textBoxHeight = 1010, 70
box = [(280, 497), (270 + textBoxWidth, 497 + textBoxHeight)]

font = ImageFont.truetype("../comicSans.ttf", 100)
text = "this is a test"
fontSize = 100
size = None


ImageDraw.Draw(soundOutDesign).rectangle(box, outline="black")
soundOutDesign.save("../png/soundoutActivityBulbasaurWithText.png")