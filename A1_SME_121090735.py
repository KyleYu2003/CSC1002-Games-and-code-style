import random

# Global variables
g_numberOfBalls = None   # The number of balls in the game.
g_oddBall = None         # The identifiers of the oddball.
g_leftPan = None         # The balls input from player to place at left.
g_rightPan = None        # The balls input from player to place at right.
g_boolean = True         # This is a boolean type to control the running fo the game.
g_count = 0              # To count the time player use scale.

# This function is used to give an introduction to player.
def showIntrodution():
    print('-'*50)                                                   # This is a boundary for the introduction.
    print("Welcome to Kangqi's odd-ball game!")                         
    print("You are given an even number of balls, labelled,")
    print("and among the balls one is heavier than the rest,")
    print("called the odd ball.")
    print("\nYour goal is to find out which one is the odd ball.")
    print("You are given a weighing scale!")
    print("\nGood luck and have fun!")
    print('-'*50)                                                   # This is a boundary for the introduction.

# This function is used to get the number of balls from player.
def getNumberOfBalls():
    global g_numberOfBalls
    while True:
        try:
            userInput = input("\nEnter the number of balls for the game:")
            g_numberOfBalls = int(userInput.strip())                # Strip two sides of space, making the game more friendly.
            if g_numberOfBalls >= 2 and g_numberOfBalls%2 == 0:     # To test whether it is an even integer, minimum 2.
                break                                               # We get a valid number from player, so stop loop.
            else:
                print("\nInvalid input!!!!")
                print("\nThe number of balls should be an even integer(such as 4, but not 4.0), minimum 2")
        except:
            print("Invalid input!!!!")
            print("\nThe number of balls should be an even integer(such as 4, but not 4.0), minimum 2")

#This function is used to generate an odd ball.
def generate(p_numberOfBalls):
    global g_oddBall
    g_oddBall = str(random.randint(1, p_numberOfBalls))             # I change it to string type, because str is more convenienced to check.

# This fuction is used to prompt palyer to place same number of ball on two sides and test whether they are valid.
def placeBalls():
    global g_leftPan
    global g_rightPan

    print("\nYou are prompted to enter the balls")
    print("to be placed on the pans of the scale,")
    print("separate each ball indentifier with one")
    print("minimum space, e.g. 1 2 3")

    while True:    
        g_leftPan = input("Enter the ball identifier(s) to be placed on the left pan:")
        g_rightPan = input("Enter the ball identifier(s) to be placed on the right pan:")
        if test(g_leftPan, g_rightPan):
            break
        print('\nYour input for left: "{}", right: "{}"'.format(g_leftPan, g_rightPan))
        print("\nInvalid input!!!!")
        print("\nPlease ensure correct ball identifiers(1-{})".format(g_numberOfBalls))
        print("are entered on each pan, no duplicate balls on either or both pans.")
        print("Both pans should have the same number of balls and must have at least one ball")

# This function is used to test whether the input from user is valid(return Ture else return False).
def test(p_left, p_right):
    leftList = p_left.split()
    rightList = p_right.split()
    removeDuplicatesSet = set()                                     # I use a set to remove duplicates.
    allTheBalls = leftList + rightList

    if len(leftList) == 0 or len(rightList) == 0:                   # Test whether the number of balls on each pan is 0.
        return False
    if len(leftList) != len(rightList):                             # Test whether the number of balls on two sides are the same.
        return False
    for i in allTheBalls:
        try:
            if not (1 <= int(i) <= g_numberOfBalls):                # Test whether the input of player is in a reasonable range.
                return False
        except:
            return False                                            # Test whether the input of player only includes integer
        removeDuplicatesSet.add(i)
    if len(removeDuplicatesSet) != len(allTheBalls):                # Test whether the input of player has some duplicates.
        return False
    
    return True

# This function is used to show the situation of scale.
def situationOfScale():
    global g_count
    g_count += 1

    if g_oddBall in g_leftPan:
        print("The scale shows: Left pan is down")
    elif g_oddBall in g_rightPan:
        print("The scale shows: Right pan is down")
    else:
        print("The scale shows: Balanced")

# This function is used to prompt player to guess and return a result.
def guess():
    global g_boolean

    while True:                                                    # This is a loop to prompt player to input a valid identifiers.
        userInput = input("Enter the odd ball number or press Enter to weigh:")
        if userInput == '':                                        # When player press Enter.
            return
        else:
            guessFromPlayer = userInput.strip()                    # Strip two sides of space, making the game more friendly.
            try:
                if not (1 <= int(guessFromPlayer) <= g_numberOfBalls):
                    print("\nInvalid input!!!!")
                    print("\nThe identifier of balls should be an integer(such as 1, but not 1.0)") 
                    print("between 1 and {}(contains two sides) or you can press Enter".format(g_numberOfBalls))
                else:
                    break
            except:
                print("\nInvalid input!!!!")
                print("\nThe identifier of balls should be an integer(such as 1, but not 1.0)")
                print("between 1 and {}(contains two sides) or you can press Enter".format(g_numberOfBalls))
        
    if guessFromPlayer == g_oddBall:
        g_boolean = False                                          # Make game stopped.
        print("\nCongratulations!!!! Scale usage count: {}".format(g_count))
    else:
        print("\nYour answer is not correct!!!!\n")

# This function is the structure of one game.
def game():
    showIntrodution()
    getNumberOfBalls()
    generate(g_numberOfBalls)
    while g_boolean:
        placeBalls()
        situationOfScale()
        guess()

# This function is used to control whether to strat a new game.
def main():
    global g_boolean
    global g_count

    startNew = True                                                # This is a boolean to control whether to start a new game.
    while startNew:
        g_boolean = True                                           # Reset it let the game to run nomarlly.
        g_count = 0                                                # Reset it let the game to run nomarlly.
        game()
        while True:
            print("Do you want to start a new game?")
            inputOfUser = input('Enter "Y/y" to start a new game or enter "Q/q" to end the game:').strip()
            if inputOfUser == 'Y' or inputOfUser == 'y':
                break
            elif inputOfUser == 'Q' or inputOfUser == 'q':
                startNew = False
                break
            else:
                print("Sorry, your input is invalid. Please enter again.")

if __name__ == '__main__':
    main()