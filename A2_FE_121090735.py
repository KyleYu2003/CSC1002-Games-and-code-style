"""
Description:
This file can give a GUI to palyer to play Color Flipping.
The main idea of this file is to generate a random situation and transfrom it to GUI frist, 
then capture the clicking on the screen and flip colors.

The following are some tips to help you to understand my code and play happy:
1. If you want to change the size of the broad, just change the value of DIM.(DIM >= 1, and it should be an integer)
2. You also can change the color of this game by changing COROL.
3. BORDER + SIZE appear many times in this file, this is the total width of the tile(include the width of border).
4. You should choose a tile first, then click the color from color bar. If you do not do so, nothing will be changed.
5. All the positions of tiles is based on the top-left one.

Have fun!
"""

import turtle
import random

# Global constants
DIM = 5                                                # Imply the size of the board is 5x5.
BORDER = 5                                             # The width of border is 5.
SIZE = 80                                              # The size of each tile is 80x80.
COLOR = ["red", "yellow", "purple", "orange", "blue"]  # The colors can be use in this game.
NUM_COLOR = len(COLOR)                                 # The number of color.
BOARD_X_MAX = (SIZE + BORDER) * DIM / 2                # The follow four constants is the border of the board.
BOARD_X_MIN = -BOARD_X_MAX
BOARD_Y_MAX = (SIZE + BORDER) * ((DIM + 1) / 2) + 5
BOARD_Y_MIN = BOARD_Y_MAX - (SIZE + BORDER) * DIM
BAR_X_MAX = BOARD_X_MIN + (SIZE + BORDER) * NUM_COLOR  # The follow four constants is the border of the bar.
BAR_X_MIN = BOARD_X_MIN
BAR_Y_MAX = BOARD_Y_MAX - (SIZE + BORDER) * DIM - 10
BAR_Y_MIN = BAR_Y_MAX - (SIZE + BORDER)

# Global variables
g_number_board = []                                    # A list contains all the situations of tiles. Use number to corresponding color in list.
g_object_board =[]                                     # A list contains all the tile objects.
g_color_bar = []                                       # A list contains all the bar objects.
g_previous_object = None                               # The object that is clicked last time.
g_flip = []                                            # This is a list to contian all the tile can be filed.
g_choose_flag = None                                   # This is a flag show the choosing state of the game(whether the player choose a tile).

def generate_random():
    """
    This function can genrate random situation for the board.
    Parameters: None
    Return: None
    """
    global g_number_board

    for _ in range(DIM**2):                                            # The _ is an element to occupy a position. Because I don't want to create too much local variables.
        g_number_board.append(random.randint(0, NUM_COLOR - 1))

def create_board_bar():
    """
    This function can create an initial board(DIMxDIM) and a color bar(1xNUM_COLOR).
    Parameters: None
    Return: None
    """
    global g_object_board

    # The following is to create a broad.
    tile = turtle.Turtle("square")
    tile.penup()                                                       # Without moving trace.
    tile.goto(BOARD_X_MIN + (SIZE + BORDER) / 2, BOARD_Y_MAX - (SIZE + BORDER) / 2)
    tile.turtlesize(SIZE / 20, SIZE / 20, BORDER)                      # The unit of tile size is 20 pixel, so we need to divide 20.
    tile.color("white", COLOR[g_number_board[0]])                      # Transform number board to GUI.
    g_object_board.append(tile)
    for i in range(1, DIM**2):                                         # Clone other tiles as the first one and let them go to where they should be.
        clone = tile.clone()
        clone.color("white", COLOR[g_number_board[i]])
        clone.penup()
        clone.goto(BOARD_X_MIN + (SIZE + BORDER) / 2, BOARD_Y_MAX - (SIZE + BORDER) / 2)
        if i//DIM != 0:
            clone.right(90)
            clone.fd((i//DIM) * (SIZE + BORDER))                       # i//DIM get the (row - 1) of the tile.
            clone.left(90)
        clone.fd((i % DIM) * (SIZE + BORDER))                          # i%DIM get the (column - 1) of the tile.
        g_object_board.append(clone)
    
    # The following is to create a color bar.
    for i in range(NUM_COLOR):
        color = tile.clone()
        g_color_bar.append(color)
        # First, move to the (5, 1) in the broad. Second, let it move to the first position of bar.
        color.goto(BOARD_X_MIN + (SIZE + BORDER) / 2, BOARD_Y_MAX - (SIZE + BORDER)*(DIM - 1/2))
        color.right(90)
        color.fd(SIZE + BORDER + 10)                                   # Get to the head of the color bar.
        color.left(90)
        color.fd(i*(SIZE + BORDER))
        color.color("black", COLOR[i])

    turtle.update()                                                    # Refresh the game area.

def search(p_index):
    """
    This function search for the same color tiles around it. Put them all to g_flip.
    Parameters: p_index(the index of the tile you want to search): int
    Return: None
    """
    global g_flip
    
    if p_index < 0:                                                    # p_index should bigger or equal to 0, or it will give an out of range error.
        pass
    else:
        if (p_index + 1) % DIM != 1:                                   # Left boundary constraint.
            if p_index - 1 not in g_flip:                              # Eaxmine whether we have searched it. 
                if g_object_board[p_index - 1].color()[1] == g_previous_object.color()[1]:
                    g_flip.append(p_index - 1)
                    search(p_index - 1)
        if (p_index + 1) % DIM != 0:                                   # Right boundary constraint.
            if p_index + 1 not in g_flip:                              # Eaxmine whether we have searched it. 
                if g_object_board[p_index + 1].color()[1] == g_previous_object.color()[1]:
                    g_flip.append(p_index + 1)
                    search(p_index + 1)
        if p_index // DIM != 0:                                        # Upper boundary constraint.
            if p_index - DIM not in g_flip:                            # Eaxmine whether we have searched it. 
                if g_object_board[p_index - DIM].color()[1] == g_previous_object.color()[1]:
                    g_flip.append(p_index - DIM)
                    search(p_index - DIM)
        if p_index // DIM != DIM - 1:                                  # Bottom boundary constraint.
            if p_index + DIM not in g_flip:                            # Eaxmine whether we have searched it. 
                if g_object_board[p_index + DIM].color()[1] == g_previous_object.color()[1]:
                    g_flip.append(p_index + DIM)
                    search(p_index + DIM)

def click_tile(p_coordinate_x, p_coordinate_y):
    """
    This fuction use the coordination of click point to determine which tile is clicked. Then show the border of it or change color.
    Parameters: p_coordinate_x, p_coordinate_y(from onclick()): float, float
    Return: None
    """
    global g_previous_object
    global g_flip
    global g_choose_flag

    # Determine whether it is in the broad.
    if BOARD_X_MIN < p_coordinate_x < BOARD_X_MAX and BOARD_Y_MIN < p_coordinate_y < BOARD_Y_MAX:
        # The following codes are taking the top left corner of (1, 1) as the pivot. 
        # Caculate the the distance from the click point to determine the index of the tile.                            
        x_distance = p_coordinate_x - BOARD_X_MIN
        y_distance = BOARD_Y_MAX - p_coordinate_y
        x_index = x_distance//(SIZE + BORDER)
        y_index = y_distance//(SIZE + BORDER)
        if g_previous_object != None:
            g_previous_object.color("white", g_previous_object.color()[1])
        g_choose_flag = True                                            # Player choose one tile, so the flag is changed. 
        g_previous_object = g_object_board[int(x_index + DIM * y_index)]# The result of index is float, so I use int() to change type.
        g_object_board[int(x_index + DIM * y_index)].color("black", g_previous_object.color()[1])
        turtle.update()                                                 # Refresh the game area.

    # Determine whether it is in the bar    
    elif BAR_X_MIN < p_coordinate_x < BAR_X_MAX and BAR_Y_MIN < p_coordinate_y < BAR_Y_MAX:
        # The following codes are taking the top left corner of color bar as the pivot. 
        # Caculate the the distance from the click point to determine the index of the tile.
        if g_choose_flag:
            x_distance = p_coordinate_x - BAR_X_MIN
            x_index = x_distance//(BORDER + SIZE)
            if COLOR[int(x_index)] != g_previous_object.color()[1]:     # If the color of the choosen tile is the same to the color you want, do not search.
                g_flip.append(g_object_board.index(g_previous_object))
                search(g_flip[0])
                for i in g_flip:
                    g_object_board[i].color("white",COLOR[int(x_index)])# The result of index is float, so I use int() to change type.
                g_flip = []                                             # Reset the list.
            else:
                g_previous_object.color("white", g_previous_object.color()[1])
            g_choose_flag = False                                       # I change the color, so the choosing is removed. 
            turtle.update()                                             # Refresh the game area.

def main():
    """
    Main fuction of this game.
    Parameters: None
    Return: None
    """
    turtle.tracer(0)                                                    # Disable auto screen refresh.
    if DIM >= 5:
        turtle.setup(2 * (BOARD_X_MAX + 10), 2 * (BOARD_Y_MAX + 10))
    else:                                                               # If you make DIM less, this will make sure show all the color in the screen.
        turtle.setup(2 * (BAR_X_MAX + 25), 2 * (BOARD_Y_MAX + 20))
    turtle.title("Color Flipping")
    generate_random()
    create_board_bar()
    turtle.Screen().onclick(click_tile)                                 # Capture the mouse-click event.
    turtle.mainloop()

if __name__ == "__main__":
    main()