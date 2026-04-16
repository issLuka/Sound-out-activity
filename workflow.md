

### 3/30/2026 
- got mostly working really roughly only locally, can go from home page, to enter info, to display simple text results. Results buttons are mostly not functional
    - want to (for now) set up the edit button to work to edit the output text, add button to generate PNG (need to figure out png pasting)
    add back to entering text, move the picture selection to the text results page - add another result page to display generated PNG. 
    ## ASAP ADDS
    - Result page: buttons for going back to enter text and edit results
    - Input page: make it a limit so the user can ONLY enter 4 words (levels1-4) and 2 words(level5)

    use seperate fonts for ENglish and Japanese

    make so user can paste in a list of words already made and it will enter in sections of 4 per text box
    
    want to use https://www.kfstudio.net/font/kfhimaji/ font, but awaiting permission

### 4/14/2026
- it's working on a railway test site, but there's stil stuff to do.

 ## to do
-  add spaces between letters (ask higuchi sensei if she prefs with or without)
- make so it gives the error red or some type of signal when entering noncharacters (,.-/ etc)
- make it print the mixed text according to the box entered, like if user enters 3 words in level 1, 2 in level 2 , 1 in level 3, make it print out the 3 in level 1, 2 in level 2 etc
    - (work flow for this will likely be initially changing the way the input is taken into the pyApp and sent to the soundOutTranslation, then the output from that and adjusting the input in the actual writing script so they can reflect the original input)
        - **PERHAPS MAKE IT EVENTUALLY HAVE ABILITY TO MAKE MINI WORKSHEET? LIKE 2 WORDS A LEVEL OR 1-4 INSTEAD OF 1-5 OR SOMETHIG***
- figure out the error it throws when a level is skipped or don't allow the generate button to work if all levels not filled with message that says "fill all levels" and a list of what's not filled in or something along those lines
- add copy paste commands (allow users to paste and have it fill in level 1 with 4, 2 with 4 etc automatically)
- add borders to seperate levels
- set up half work sheets
    - 4 levels, 2 words each, selector at top for full or half sheet which will determine the text boxes displayed
        - seperate scripts to all be in inputHandler.js maybe or create completely seperate scripts sheet?