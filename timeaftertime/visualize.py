import pygame

from timeaftertime.game import GameBoard

def display(screen, image_name, left, top, width=20, height=20):
    image = pygame.image.load(f'timeaftertime/data/images/{image_name}.png')
    image = pygame.transform.smoothscale(image, (width, height))
    screen.blit(image, (left,top))

color_dict = {1: 'red', 2: 'blue', 3: 'green', 4: 'orange', 5: 'yellow'}
special_dict = {1: 'dice', 2: 'bomb', 3: 'heart'}

# define some colors
BLACK = (0,0,0)
GREY = (185, 191, 196)
WHITE = (255,255,255)
RED = (255,0,0)

# this sets the WIDTH and HEIGHT of each cell
WIDTH_BLOCKS = 20
HEIGHT_BLOCKS = 20

# this sets the margin between each cell
MARGIN_BLOCKS = 1
MARGIN_SIDE = 4
MARGIN_LEFT = 7
MARGIN_TOP = 20

# generate keeropkeer playing board
game_board = GameBoard()
game_board.initialize()
game_board.generate()

# Set the HEIGHT and WIDTH of the screen
nrows = game_board.height
ncols = game_board.width
height = nrows * (WIDTH_BLOCKS + MARGIN_BLOCKS) + MARGIN_BLOCKS + MARGIN_SIDE*2 + MARGIN_LEFT + MARGIN_TOP + WIDTH_BLOCKS*4
width = ncols * (WIDTH_BLOCKS + MARGIN_BLOCKS) + MARGIN_BLOCKS + MARGIN_SIDE*2 + MARGIN_LEFT*2 + WIDTH_BLOCKS*3

# open window
screen = pygame.display.set_mode([width, height])
 
# Set title of screen
pygame.display.set_caption("Keer op keer 2")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 
# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop

        # fill background
        screen.fill(GREY) 

        # Draw starting column highlight
        screen.fill(WHITE, ((MARGIN_BLOCKS + WIDTH_BLOCKS) * game_board.layout['start_column'] + MARGIN_SIDE + MARGIN_LEFT + WIDTH_BLOCKS*2,
                        MARGIN_SIDE + MARGIN_TOP + HEIGHT_BLOCKS - MARGIN_BLOCKS, 
                        WIDTH_BLOCKS+MARGIN_BLOCKS*2, 
                        HEIGHT_BLOCKS*nrows+MARGIN_BLOCKS*(nrows+1)))

        # Draw the main board
        for block in game_board.board.blocks:
            color = block.color
            for coord in block.coords:
                image_name = f'{color_dict[color]}'
                if coord in game_board.layout['dice']:
                    image_name += f'_dice'
                elif coord in game_board.layout['star']:
                    image_name += f'_star'
                display(screen, 
                        image_name, 
                        (MARGIN_BLOCKS + WIDTH_BLOCKS) * coord.y + MARGIN_SIDE + MARGIN_LEFT + MARGIN_BLOCKS + WIDTH_BLOCKS*2, 
                        (MARGIN_BLOCKS + HEIGHT_BLOCKS) * coord.x + MARGIN_SIDE + MARGIN_TOP + HEIGHT_BLOCKS,
                        width=WIDTH_BLOCKS,
                        height=HEIGHT_BLOCKS)
        
        # Draw the row scores/specials
        for row in range(nrows):
            # row scores
            display(screen,
                    f'scores/{game_board.layout["row_scores"][row]}',
                    MARGIN_LEFT,
                    (MARGIN_BLOCKS + HEIGHT_BLOCKS) * row + MARGIN_SIDE + MARGIN_TOP + HEIGHT_BLOCKS,
                    width=WIDTH_BLOCKS,
                    height=HEIGHT_BLOCKS)
            
            # row specials
            display(screen,
                f'{special_dict[game_board.layout["row_attributes"][row]]}',
                MARGIN_LEFT+WIDTH_BLOCKS+MARGIN_BLOCKS,
                (MARGIN_BLOCKS + HEIGHT_BLOCKS) * row + MARGIN_SIDE + MARGIN_TOP + HEIGHT_BLOCKS,
                width=WIDTH_BLOCKS,
                height=HEIGHT_BLOCKS)

        # Draw the col scores/specials
        for column in range(ncols):
            # col scores top
            if game_board.layout['col_scores_top'][column] == 0:
                col_score_top = f'dice_2'
            else:
                col_score_top = f'scores/{game_board.layout["col_scores_top"][column]}'
            display(screen,
                    col_score_top,
                    (MARGIN_BLOCKS + WIDTH_BLOCKS) * column + MARGIN_SIDE + MARGIN_LEFT + MARGIN_BLOCKS + WIDTH_BLOCKS*2,
                    (MARGIN_BLOCKS + HEIGHT_BLOCKS) * nrows + MARGIN_SIDE + MARGIN_TOP + HEIGHT_BLOCKS + MARGIN_SIDE,
                    width=WIDTH_BLOCKS,
                    height=HEIGHT_BLOCKS)   

            # col scores bottom
            if game_board.layout['col_scores_bottom'][column] == 0:
                col_score_bottom = f'dice_0'
            else:
                col_score_bottom = f'scores/{game_board.layout["col_scores_bottom"][column]}'
            display(screen,
                    col_score_bottom,
                    (MARGIN_BLOCKS + WIDTH_BLOCKS) * column + MARGIN_SIDE + MARGIN_LEFT + MARGIN_BLOCKS + WIDTH_BLOCKS*2,
                    (MARGIN_BLOCKS + HEIGHT_BLOCKS) * nrows + MARGIN_SIDE + MARGIN_TOP + HEIGHT_BLOCKS*2 + MARGIN_SIDE + MARGIN_BLOCKS,
                    width=WIDTH_BLOCKS,
                    height=HEIGHT_BLOCKS)  

            # col hearts
            display(screen,
                'heart_alpha',
                (MARGIN_BLOCKS + WIDTH_BLOCKS) * column + MARGIN_SIDE + MARGIN_LEFT + MARGIN_BLOCKS + WIDTH_BLOCKS*2,
                (MARGIN_BLOCKS + HEIGHT_BLOCKS) * nrows + MARGIN_SIDE*2 + MARGIN_TOP + HEIGHT_BLOCKS*3 + MARGIN_BLOCKS*2,
                width=WIDTH_BLOCKS,
                height=HEIGHT_BLOCKS)

        # Draw row names
        for row in range(nrows):
            display(screen,
                    f'rowcol/{game_board.layout["row_names"][row]}',
                    (MARGIN_BLOCKS + WIDTH_BLOCKS) * ncols + MARGIN_SIDE*2 + MARGIN_LEFT + WIDTH_BLOCKS*2,
                    (MARGIN_BLOCKS + HEIGHT_BLOCKS) * row + MARGIN_SIDE + MARGIN_TOP + HEIGHT_BLOCKS,
                    width=WIDTH_BLOCKS,
                    height=HEIGHT_BLOCKS)

        # Draw col names
        for column in range(ncols):
            column_name = f'rowcol/{game_board.layout["col_names"][column]}'
            if game_board.layout['col_names'][column] == game_board.layout['start_column']:
                column_name = f'{column_name}_red'
            display(screen,
                    column_name,
                    (MARGIN_BLOCKS + WIDTH_BLOCKS) * column + MARGIN_SIDE + MARGIN_LEFT + MARGIN_BLOCKS + WIDTH_BLOCKS*2,
                    MARGIN_TOP,
                    width=WIDTH_BLOCKS,
                    height=HEIGHT_BLOCKS)

    # Limit to 60 frames per second
    clock.tick(60)
 
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()