from Inits.lib import ColourLibrary, PixelLibrary, PixelInteractionLibrary, ButtonLibrary
from random import randint
import pygame
import pickle
import os
import easygui



"""DEBUGGER"""

import time 


pygame.init()
 
#Main loop Value and global variables
CurrentlyRunning = True
Pause = False
ShaderState = True
ExecuteState = True
InteractionState = True
clock = pygame.time.Clock()
CurrentBrush = "ERASE"
GameFont = "Inits/font.ttf"

#Sets up PIXELMULTIPLIER as a value relative to the main screen pixel resolution
PIXELMULTIPLIER = 9


#Sets up the display screen according to strict values and the resolution dependent PIXELMULTIPLIER
WIDTH = 150
HEIGHT= 70
MENUBAR = HEIGHT * (3/10)
DisplaySurface = pygame.display.set_mode((WIDTH * PIXELMULTIPLIER , HEIGHT * PIXELMULTIPLIER + MENUBAR * PIXELMULTIPLIER))
RowOfButtons = 4
ColumnOfButtons = 13


pygame.display.set_caption("Pixel Garden")
DisplaySurface.fill(ColourLibrary["BACKGROUND"])
pygame.display.flip()

def PixelInteractions(ListOfNonVoids):  
    for NonVoid in ListOfNonVoids:
        PixelSenserIterator = 0
        #Keeps track of which neighbour is being evaluated in respect to the pixel
        LibraryTracker = -1
        #Kludgy way of keeping track of the item in the PixelInteractionLibrary
        
        Pixel = Grid[NonVoid[0]][NonVoid[1]]
        
        for PixelEntry in PixelInteractionLibrary:
            #Iterate over all the items in the library
            LibraryTracker += 1
            if Pixel[3] == PixelEntry[0] and randint(1,10000) >= PixelEntry[3]:
                #If there is a list that starts with the name of the pixel that is currently being evaluated
                Identities = []
                for Neighbour in PixelSenser(NonVoid):
                    PixelSenserIterator += 1
                    #For each neighbour in the pixelsenser, count the pixels
                    if Neighbour == "EDGE":
                        pass
                    else:
                        NeighbourType = Grid[Neighbour[0]][Neighbour[1]]
                        #Isolate the pixel type name
                        if NeighbourType[3] in PixelEntry[1]:
                            #If the pixel name appears in the list given in the pixel interactions library
                            if type(NeighbourType) == list and PixelSenserIterator in PixelEntry[4]:
                                #AND the currently evaluated pixel is allowed according to the same list
                                
                                for Identity in PixelLibrary[PixelInteractionLibrary[LibraryTracker][2]]:
                                    Identities.append(Identity)
                                    #Build the new pixels
                                
                                if PixelEntry[5] == True:
                                    #Remove the agent pixel 
                                    Grid[Neighbour[0]][Neighbour[1]] = PixelLibrary["ERASE"]
                                
                                if Pixel[3] != PixelEntry[2]:
                                    #This essentially stops pixels from being replaced with themselves
                                    Grid[NonVoid[0]][NonVoid[1]] = [Identities[0], Identities[1], Shader(Identities[2]), Identities[3], Identities[4]]
                                break
                    
def Shader(ColourTuple):
    #Takes the colour tuple from the COLOURS list and reconstructs it as a list
    #Then slightly alters the values uniformly so as to make a lighter or darker hue
    NewColour = []
    Adjustment = randint(-20,20)
    
    for IntValue in ColourTuple:
        if abs(IntValue + Adjustment) < 255:
            #Ensuring the new colour value is within the 8 bit range
            NewColour.append(abs(IntValue + Adjustment))
        else:
            #Otherwise leave the colour unchanged (Only noticable with white shades)
            NewColour.append(IntValue)               
    return NewColour

def GridMaker(PixelsX, PixelsY):
    #Sets up the grid for X pixels of length and Y pixels of height
    #It generates the grid by creating an entry of lists that runs in the Y direction
    #Then populating the grid with a running increment in the X direction
    #The result is a grid-like list of numbers, with each pixel having a listed item of their identities
    CurrentGrid = []
    for Lines in range(PixelsY):
        CurrentLine = []
        for Rows in range(PixelsX):
            CurrentLine.append(PixelLibrary["ERASE"])
        CurrentGrid.append(CurrentLine)
    return CurrentGrid

def FieldChecker(Field):
    #Checks all the pixel in the field by iterating over all the lists within the field list (Y) and then the individual pixels addresses in each nested list (X)
    #Anything that isn't a "ERASE" pixel type gets flagged and appended to the ListOfNonVoids list as an YX coordinate of the Field list
    ListOfNonVoids = []
    
    for Line in range(len(Field)):
        #This targets a list in the nested lists in Field by index number
        for Position in range(len(Field[Line])):
            #This targets a value in the currently evaluated line by index number
            #Essentially, for the Line in Field at the currently held index number, look at each pixel and give them YX coordinate
            if Field[Line][Position][3] != "ERASE":
                #This is a pixel worth keeping track off 
                ListOfNonVoids.append((Line, Position))
                "This value is represented as an YX coordinate"   
    return ListOfNonVoids

def PixelSenser(NonVoid):
  """This right here is the culprit, this is why everything comes down to a CRUNCH once you add enough pixels to the screen"""
    #Checks the surrounding pixels of an origin pixel PER pixel input
    NeighbouringPixels = []
    for PosY in range(-1, 2):
        for PosX in range(-1, 2):
            #Iterating over PosX and PosY essentially scans the surrounding locations
            if [PosY, PosX] != [0,0]:
                #The origin pixel itself is excluded from the list of surrounding pixels
                if NonVoid[0] + PosY >= 0 and NonVoid[1] + PosX >= 0 and NonVoid[0] + PosY <= HEIGHT-1 and NonVoid[1] + PosX <= WIDTH-1:
                    #As long as the surrounding pixel has positive values for both the Y and  X coordinate (Not outside of the grid top- or leftwise)
                    #AND as long as the surrounding pixel has a value that doesn't exceed the screen dimension maxima (Not outside of the grid bottom- or rightwise)
                    #Add the location tuple of that pixel to a list of all neighbours
                    NeighbouringPixels.append([NonVoid[0]+PosY, NonVoid[1]+PosX])                        
                else:
                    #Indicate that the pixel is at an edge at that location
                    NeighbouringPixels.append("EDGE")
    return NeighbouringPixels

def PixelMoverDown(NonVoid, SurroundingPixels): 
    YCoordinate = NonVoid[0]
    XCoordinate = NonVoid[1]
    ParticleValue = Grid[YCoordinate][XCoordinate]
    PriorityValue = randint(0,100)
    
    if ParticleValue[4] == 0:
        #If the momentum value for the pixel has not been set, randomly set the momentum (-1: left, 1: right)
        LeftOrRight = [-1,1][randint(0,1)]
    else:
        #If a momentum has been set, use that momentum
        LeftOrRight = ParticleValue[4]
    
    if type(SurroundingPixels[6]) != str and ParticleValue[1] >= 1:
        #If the location right below pixel is not a string ("EDGE") AND the pixel has the movement class 1 (Solid) or higher
        LocationValue = Grid[SurroundingPixels[6][0]][SurroundingPixels[6][1]]
        if LocationValue[3] == "ERASE":
            #If the location below the pixel is free, simply move it there
            Grid[SurroundingPixels[6][0]][SurroundingPixels[6][1]] = ParticleValue
            Grid[YCoordinate][XCoordinate] = LocationValue
        elif LocationValue[3] != "ERASE"  and ParticleValue[0] >= LocationValue[0] and ParticleValue[3] != LocationValue[3]:
            #If the location below the pixel is taken up by a pixel that is not itself
            #AND has a lower or equal priority AND the location pixel is a fluid, swap the pixels based on chance where a larger priority difference increases the swap chance
            if PriorityValue > 95 * ((LocationValue[0]) / (ParticleValue[0])) and LocationValue[1] >= 3:
                Grid[SurroundingPixels[6][0]][SurroundingPixels[6][1]] = ParticleValue
                Grid[YCoordinate][XCoordinate] = LocationValue
            else:
                PixelMoverDiagonal(YCoordinate, XCoordinate, ParticleValue, PriorityValue, LeftOrRight, SurroundingPixels)
        else:
            #All downward movement options have been exhausted, time to try diagonal motion
            PixelMoverDiagonal(YCoordinate, XCoordinate, ParticleValue, PriorityValue, LeftOrRight, SurroundingPixels)    
    elif type(SurroundingPixels[6]) == str and ParticleValue[1] >= 3:
        #It is possible that a pixel is on the bottom edge of the screen and allows for equilateral movement
        PixelMoverEquilateral(YCoordinate, XCoordinate, ParticleValue, PriorityValue, LeftOrRight, SurroundingPixels)

def PixelMoverDiagonal(YCoordinate, XCoordinate, ParticleValue, PriorityValue, LeftOrRight, SurroundingPixels):
    if ParticleValue[1] >= 2 and XCoordinate + LeftOrRight >= 0 and (XCoordinate + LeftOrRight) < WIDTH:
        #If the proposed location is within Grid boundaries AND the pixel has the movement class 2 (Granulate) or higher
        LocationValue = Grid[SurroundingPixels[6 + LeftOrRight][0]][SurroundingPixels[6 + LeftOrRight][1]]
        if LocationValue[3] == "ERASE":
            #If the location at the chosen direction below the pixel is free, simply move it there
            Grid[SurroundingPixels[6 + LeftOrRight][0]][SurroundingPixels[6 + LeftOrRight][1]] = ParticleValue
            Grid[YCoordinate][XCoordinate] = LocationValue            
        elif XCoordinate + (LeftOrRight * -1) >= 0 and (XCoordinate) + (LeftOrRight * -1) < WIDTH:
            AlternateLocationValue = Grid[SurroundingPixels[6 + LeftOrRight][0]][SurroundingPixels[6 + (LeftOrRight * -1)][1]]
            #If the first chosen location is not viable, try the other side by multiplying LeftOrRight by -1, essentuially flipping the value
            if AlternateLocationValue[3] == "ERASE":
                Grid[SurroundingPixels[6 + LeftOrRight][0]][SurroundingPixels[6 + (LeftOrRight * -1)][1]] = ParticleValue
                Grid[YCoordinate][XCoordinate] = AlternateLocationValue
            else:
                #if diagonal motion is not possible, go straight to equilateral movement
                PixelMoverEquilateral(YCoordinate, XCoordinate, ParticleValue, PriorityValue, LeftOrRight, SurroundingPixels)
        else:
            #if diagonal motion is not possible, go straight to equilateral movement
            PixelMoverEquilateral(YCoordinate, XCoordinate, ParticleValue, PriorityValue, LeftOrRight, SurroundingPixels)
        

def PixelMoverEquilateral(YCoordinate, XCoordinate, ParticleValue, PriorityValue, LeftOrRight, SurroundingPixels):
    if ParticleValue[1] >= 3 and XCoordinate + LeftOrRight >= 0 and (XCoordinate) + LeftOrRight < WIDTH:
        #If the proposed location is within Grid boundaries AND the pixel has the movement class 3 (Liquid) or higher
        LocationValue = Grid[YCoordinate][XCoordinate + LeftOrRight]
        if LocationValue[3] == "ERASE":
            #If the location to the chosen side of the pixel is free, simply move it there
            ParticleValue[4] = LeftOrRight
            Grid[YCoordinate][XCoordinate + LeftOrRight] = ParticleValue
            Grid[YCoordinate][XCoordinate] = LocationValue
        elif LocationValue[3] != "ERASE" and ParticleValue[0] >= LocationValue[0]:
            if PriorityValue > 85 * ((LocationValue[0]) / (ParticleValue[0])):
                #If the location is taken up by a pixel, try to swap it based on priority and chances
                #Note how the Priority Value here only has to pass 85, as opposed to 95 for the vertical swap, as this swap should be easier
                ParticleValue[4] = 0
                #Reset the momentum value, this might not be necessary(?) 
                Grid[YCoordinate][XCoordinate] = LocationValue
                Grid[YCoordinate][XCoordinate + LeftOrRight] = ParticleValue                
        else:

            ParticleValue[4] = 0
            #Reset the momentum value, it is possible the Pixel simply cannot move that way, try rerolling to the other side
                

def DrawingToTheScreen(ShaderState):
    #Updates the pixel state on the screen in either pause or active modes    
    for LineToConsider in range(len(Grid)):
                for PixelToDraw in range(len(Grid[LineToConsider])):
                    if Grid[LineToConsider][PixelToDraw][3] != "ERASE":
                        #Iterates over each pixel in the grid and flags the ones that are not zero-values
                        ParticleValue = Grid[LineToConsider][PixelToDraw]                                
                        #Draws the pixel as specified by the Pixel Value Structure at the location of the Pixel in the Grid
                        #Considers the ShaderState value to see if pixels have to be drawn with variety or not.
                        if ShaderState == True:
                            pygame.draw.rect(DisplaySurface, ParticleValue[2], (PixelToDraw * PIXELMULTIPLIER , LineToConsider * PIXELMULTIPLIER , PIXELMULTIPLIER , PIXELMULTIPLIER ))
                        elif ShaderState == False:
                            pygame.draw.rect(DisplaySurface, ColourLibrary[ParticleValue[3]], (PixelToDraw * PIXELMULTIPLIER , LineToConsider * PIXELMULTIPLIER , PIXELMULTIPLIER , PIXELMULTIPLIER ))

def MousePositioner():
    #Floor dividing the mouse position by PIXELMULTUPLIER basically scales down the screen's resolution
    MouseX = (pygame.mouse.get_pos()[0])//PIXELMULTIPLIER
    MouseY = (pygame.mouse.get_pos()[1])//PIXELMULTIPLIER
    
    if MouseY < HEIGHT:
        #If the mouse is within the playing field
        Brush(MouseY, MouseX)
    elif MouseY >= HEIGHT:
        #If the mouse is in the menu bar
        ButtonListings(MouseY, MouseX)
        

def Brush(MouseY, MouseX):
    #Allows Pixels to be populated into the grid based on the position of the mouse on the screen    
    Identities = []
       
    if Grid[MouseY][MouseX][3] == "ERASE" and CurrentBrush != "ERASE":
        #If the mouse hovers over a pixel that is empty and the current brush isn't set to "ERASE"  (erase)
        #Create a pixel at this location
        #The Pixel Identity needs to be reconstructed so that any change doesn't get lead back to the dictionary
        PixelIdentity = PixelLibrary[CurrentBrush]
        for Identity in PixelIdentity:
            Identities.append(Identity)
        
        #Note how the 3rd identity (Colour) is being processed using the Shader() function to ensure colour variety
        Grid[MouseY][MouseX] = [Identities[0], Identities[1], Shader(Identities[2]), Identities[3], Identities[4]]
    
    elif Grid[MouseY][MouseX][3] != "ERASE" and CurrentBrush == "ERASE":
        #Note how there is no need to mess with building the pixel up as we are not altering the values using "Shader"; "ERASE" is invisble anyway
        Grid[MouseY][MouseX] = PixelLibrary["ERASE"]

        
def CurrentBrushSettings(CurrentBrush):
    font = pygame.font.Font(GameFont, int(PIXELMULTIPLIER * 3))
    text = font.render(str(CurrentBrush), True, ColourLibrary[CurrentBrush])
    DisplaySurface.blit(text, (4 * PIXELMULTIPLIER, 2 * PIXELMULTIPLIER))
    
def ShaderStatusScreen(ShaderState):
    #Indicates the Shader Status on-screen
    font = pygame.font.Font(GameFont, int(PIXELMULTIPLIER * 3))
    if ShaderState == True:
        text = font.render("Shader: On", True, ColourLibrary["WHITE"])
    else:
        text = font.render("Shader: Off", True, ColourLibrary["WHITE"])
    DisplaySurface.blit(text, (40 * PIXELMULTIPLIER, 2 * PIXELMULTIPLIER))
    
def PauseStatusScreen(Pause):
    #Indicates the Pause status on-Screen
    font = pygame.font.Font(GameFont, int(PIXELMULTIPLIER * 3))
    if Pause == True:
        text = font.render("PAUSED", True, ColourLibrary["WHITE"])
    else:
        text = font.render("RUNNING", True, ColourLibrary["WHITE"])
    DisplaySurface.blit(text, (130 * PIXELMULTIPLIER, 2 * PIXELMULTIPLIER))
    
def InteractionStatusScreen(InteractionState):
    #Indicates the Interactions status on-Screen
    font = pygame.font.Font(GameFont, int(PIXELMULTIPLIER * 3))
    if InteractionState == True:
        text = font.render("PIXEL INTERACTIONS: ON", True, ColourLibrary["WHITE"])
    else:
        text = font.render("PIXEL INTERACTIONS: OFF", True, ColourLibrary["WHITE"])
    DisplaySurface.blit(text, (70 * PIXELMULTIPLIER, 2 * PIXELMULTIPLIER))

def MenuBarSettings():
    #Sets up the Menu below the playing field with all relevant dimensions        
    #Adjusts the various dimensions so that the coordinate system is separate from the total screen and later allows buttons to scale proportionally in MaterialButtonPopulator
    #Calls MaterialButtonPopulator() to populate the menu with pixel buttons
    AdjustedOrigin = HEIGHT * PIXELMULTIPLIER
    AdjustedHeight= (HEIGHT + MENUBAR) * PIXELMULTIPLIER
    AdjustedWidth = WIDTH * PIXELMULTIPLIER
   
    pygame.draw.rect(DisplaySurface, ColourLibrary["MENUCOLOUR"], (0, AdjustedOrigin, AdjustedWidth, AdjustedHeight))
    #A separate solid backdrop colour for the menu
    pygame.draw.rect(DisplaySurface, ColourLibrary["MENUACCENT"], (-PIXELMULTIPLIER, AdjustedOrigin, AdjustedWidth + 2 * PIXELMULTIPLIER, AdjustedHeight), int(0.5 * PIXELMULTIPLIER))
    #A frame for the backdrop

    
    MaterialButtonPopulator(AdjustedOrigin, AdjustedHeight, AdjustedWidth)

def MaterialButtonPopulator(AdjustedOrigin, AdjustedHeight, AdjustedWidth):
    #Populates the menu field with buttons linking to the various pixel materials
    ButtonWidth = WIDTH/ColumnOfButtons
    ButtonHeight = MENUBAR/RowOfButtons
    SideIncrement = 5/PIXELMULTIPLIER
    ButtonIncrement = SideIncrement*2
    font = pygame.font.Font(GameFont, int(PIXELMULTIPLIER * 1.9))

    for ButtonCoordinate in list(ButtonLibrary.keys()):
        ButtonPositionX = (((ButtonCoordinate[1]) * ButtonWidth)+SideIncrement) * PIXELMULTIPLIER
        ButtonPositionY = (((ButtonCoordinate[0]) * (ButtonHeight) + SideIncrement) * PIXELMULTIPLIER) + PIXELMULTIPLIER/2
        #For as long as I live, I will never create another lengthy monstrosity like this
        #Essentially, it calls upon the coordinates given in ButtonLibrary and constructs a button proportionally to the screen dimension values
        #If there is no coordinate in the library, there is no button generated
        #May God have mercy on your soul for you cannot explain this statement on judgement day
        pygame.draw.rect(DisplaySurface, ColourLibrary["BUTTONUP"],
        pygame.Rect(ButtonPositionX, ButtonPositionY + AdjustedOrigin, (ButtonWidth - ButtonIncrement) * PIXELMULTIPLIER, (ButtonHeight - ButtonIncrement)* PIXELMULTIPLIER))
        pygame.draw.rect(DisplaySurface, ColourLibrary["BUTTONFONT"],
        pygame.Rect(ButtonPositionX, ButtonPositionY + AdjustedOrigin, (ButtonWidth - ButtonIncrement) * PIXELMULTIPLIER, (ButtonHeight - ButtonIncrement)* PIXELMULTIPLIER), int(PIXELMULTIPLIER/2))
    
        
        text = font.render(ButtonLibrary[ButtonCoordinate], True, ColourLibrary["BUTTONFONT"])
        DisplaySurface.blit(text, (ButtonPositionX + PIXELMULTIPLIER, ButtonPositionY + PIXELMULTIPLIER + AdjustedOrigin))
        #Writes the button identity as text over the button
        
    FunctionButtonPopulator(AdjustedOrigin, AdjustedHeight, AdjustedWidth, ButtonWidth, ButtonHeight, SideIncrement, ButtonIncrement, font)
    #Initialise the function buttons
    
def FunctionButtonPopulator(AdjustedOrigin, AdjustedHeight, AdjustedWidth, ButtonWidth, ButtonHeight, SideIncrement, ButtonIncrement, font):
    #This function is largely the same as MaterialButtonPopulator
    
    for ButtonCoordinate in list(FunctionButtonLibrary.keys()):
        ButtonPositionX = (((ButtonCoordinate[1]) * ButtonWidth)+SideIncrement) * PIXELMULTIPLIER
        ButtonPositionY = (((ButtonCoordinate[0]) * (ButtonHeight) + SideIncrement) * PIXELMULTIPLIER) + PIXELMULTIPLIER/2
        pygame.draw.rect(DisplaySurface, ColourLibrary["FUNCTIONUP"],
        pygame.Rect(ButtonPositionX, ButtonPositionY + AdjustedOrigin, (ButtonWidth - ButtonIncrement) * PIXELMULTIPLIER, (ButtonHeight - ButtonIncrement)* PIXELMULTIPLIER))
        pygame.draw.rect(DisplaySurface, ColourLibrary["FUNCTIONFONT"],
        pygame.Rect(ButtonPositionX, ButtonPositionY + AdjustedOrigin, (ButtonWidth - ButtonIncrement) * PIXELMULTIPLIER, (ButtonHeight - ButtonIncrement)* PIXELMULTIPLIER), int(PIXELMULTIPLIER/2))
        text = font.render(FunctionButtonLibrary[ButtonCoordinate][0], True, ColourLibrary["FUNCTIONFONT"])
        DisplaySurface.blit(text, (ButtonPositionX + PIXELMULTIPLIER, ButtonPositionY + PIXELMULTIPLIER + AdjustedOrigin))

def PauseTheGame():
    #Function to flip the state of the Pause variable when the Pause button is pressed
    global Pause
    Pause = False if Pause else True
        
def SetTheShader():
    #Function to flip the state of the ShaderState variable when the Shader button is pressed
    global ShaderState
    ShaderState = False if ShaderState else True

def SetTheInteract():
    #Function to flip the state of the InteractState variable when the Shader button is pressed
    global InteractionState
    InteractionState = False if InteractionState else True        
        
def SaveTheGame():
    #Creates a pickle file with the current GameState and open the File Explorer
    path = easygui.filesavebox(default = str(os.listdir()) + '\Saves')
    if path != None:
        with open(path, 'wb') as SaveGameState:
            pickle.dump(Grid, SaveGameState)
    else:
        pass
        
def LoadTheGame():
    #Opens the File Explorer and allows you to select a pickle file to load
    global Grid
    global Pause
    path = easygui.fileopenbox(default = str(os.listdir()) + '\Saves')
    if path != None:
        with open(path, 'rb') as LoadGameState:
            Grid = pickle.load(LoadGameState)
            Pause = True

def WipeGameStateRequest():
    #Creates a button to confirm resetting the grid
    #If this button is already up, it will hide it instead
    if (1,10) in FunctionButtonLibrary:
        del FunctionButtonLibrary[(1,10)]
    else:
        FunctionButtonLibrary.update({(1, 10) : ["YES", WipeGameState]})
       
def WipeGameState():
    #Fully resets the Grid
    global Grid
    Grid = GridMaker(WIDTH, HEIGHT)
    del FunctionButtonLibrary[(1,10)]
    
def SetAllToLiquid():
    for PixelLine in range(len(Grid)):
        for Pixel in range(len(Grid[PixelLine])):
            Grid[PixelLine][Pixel][0] = 1
            Grid[PixelLine][Pixel][1] = 3
        

        


#Internal dictionary to create the function buttons
#Sadly cannot be exported as it calls functions within the main program
FunctionButtonLibrary = {
    (0, 11) : ["PAUSE", PauseTheGame],
    (1, 11) : ["SHADER", SetTheShader],
    (2, 11) : ["ACTIONS", SetTheInteract],
    (2, 10) : ["SAVE", SaveTheGame],
    (3, 10) : ["LOAD", LoadTheGame],
    (0, 10) : ["CLEAR", WipeGameStateRequest],
    (1, 12) : ["SOUP IT", SetAllToLiquid]

    }
    
def ExecuteFunctionButton(CoordinatePair):
    #Executes the function given in FunctionButtonLibrary 
    
    global ExecuteState
    #ExecuteState is a variable that enforces a local pause
    #If this is not present, the program will keep executing the Function button, resulting in "flickering" while the mouse button is pressed
    #By setting ExecuteState to False at the end of the function, you ensure that this function is only run once
    #The main gameplay loop sets ExecuteState back to True if there is no mouse button pressed, making the function available again
        
    if ExecuteState == True:
        FunctionButtonLibrary[CoordinatePair][1]()
        ExecuteState = False


             
def ButtonListings(MouseY, AdjustedX):
    #Relates the mouse's position in the menu to a button in ButtonLibrary
    AdjustedY = MouseY-HEIGHT
    ButtonWidth = WIDTH/ColumnOfButtons
    ButtonHeight = MENUBAR/RowOfButtons
    
    global CurrentBrush           
    if ((AdjustedY//ButtonHeight, AdjustedX//ButtonWidth)) in ButtonLibrary:
        CurrentBrush = ButtonLibrary[((AdjustedY//ButtonHeight, AdjustedX//ButtonWidth))]
    elif ((AdjustedY//ButtonHeight, AdjustedX//ButtonWidth)) in FunctionButtonLibrary:
        ExecuteFunctionButton(((AdjustedY//ButtonHeight, AdjustedX//ButtonWidth)))

    
Grid = GridMaker(WIDTH, HEIGHT)
MenuBarSettings()



while CurrentlyRunning == True:
    clock.tick(25)
    
    if pygame.mouse.get_pressed()[0] == False:
        ExecuteState = True
        MenuBarSettings()
        #This variable controls local pausing for function button pressing
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            CurrentlyRunning = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                #Placeholder action to test program functionalities
                for line in Grid:
                    for pixel in line:
                        if pixel[3] != "ERASE":
                            print(pixel)
          
    if pygame.mouse.get_pressed()[0] == True:
        MousePositioner()
                       
    if Pause == False:
        start = time.time()
        if InteractionState == True:
            
            PixelInteractions(FieldChecker(Grid))
            
        #print(len(FieldChecker(Grid)))
        
        for i in reversed(FieldChecker(Grid)):
                    PixelMoverDown(i, PixelSenser(i))
                    
        #print(time.time()-start)
        

        
        


    DrawingToTheScreen(ShaderState)
    CurrentBrushSettings(CurrentBrush)
    ShaderStatusScreen(ShaderState)
    PauseStatusScreen(Pause)
    InteractionStatusScreen(InteractionState)
    pygame.display.flip()
    pygame.draw.rect(DisplaySurface, ColourLibrary["BACKGROUND"], (0,0, WIDTH * PIXELMULTIPLIER, HEIGHT * PIXELMULTIPLIER))


pygame.quit()
