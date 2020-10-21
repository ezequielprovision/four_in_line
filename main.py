import numpy as np
import pygame
import math

############# CONST ###############
ROW_COUNT = 6      # AXIS Y
COLUMN_COUNT = 7   # AXIS X
PLAYER_1_PIECE = (255, 255, 0)
PLAYER_2_PIECE = (255, 0, 0)
############# FUNCTIONS ############
def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT)) # lista con 6 listas, y cada una con 7 ceros dentro
    return board

def print_board(board):
    print(np.flip(board, 0)) # sino el tablero se ve invertido de arriba a abajo

def winning_move(board, piece):
    """Para ganar tienen q ser 4 fichas en linea, por eso se optimiza con el nº3"""
    """ comprueba de manera horizonal"""
    for c in range(COLUMN_COUNT - 3): # -3 optimiza, ya q si no dio posistivo antes, no va a dar despues de eso
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True 

    """ comprueba de manera vertical"""
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    """ diagonal a la derecha"""
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    """diagonal a la izquierda"""
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[5][col] == 0 # IF THIS PLACE IS EMPTY

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, (0, 128, 255), (c*SQUARESIZE, r*SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, (0,0,0), (int(c*SQUARESIZE + SQUARESIZE/2), int(r*SQUARESIZE + SQUARESIZE + SQUARESIZE/2)), RADIUS)

    circle_color = (0,0,0)
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):

            if board[r][c] == 1: # SI PERTENECE AL JUGADOR 1
                circle_color = (255, 255, 0)
            elif board[r][c] == 2: # si pertenece al 2
                circle_color = (255, 0, 0)
            pygame.draw.circle(screen, circle_color, (int(c*SQUARESIZE + SQUARESIZE/2), height - int(r*SQUARESIZE + SQUARESIZE/2)), RADIUS)
            circle_color = (0, 0, 0)

    """
        if board[r][c] == 1: # SI PERTENECE AL JUGADOR 1
            pygame.draw.circle(screen, (255,255,0), (int(c*SQUARESIZE + SQUARESIZE/2), height - int(r*SQUARESIZE + SQUARESIZE/2)), RADIUS)
        elif board[r][c] == 2: # si pertenece al 2
            pygame.draw.circle(screen, (255,0,0), (int(c*SQUARESIZE + SQUARESIZE/2), height - int(r*SQUARESIZE + SQUARESIZE/2)), RADIUS)
    """  
      
    pygame.display.update()

############## VARS ################
game_over = False
board = create_board()
turn = 0
pygame.init()

"""
safely initializes all imported pygame modules regardless 
if the modules actually need to be initialized; 
but since it does for the ones that do, 
it saves the trouble of manually initializing each module individually.
"""
SQUARESIZE = 100
RADIUS = int(SQUARESIZE/2 - 5)
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE # para tener un espacio para mover la ficha
size = (width, height)
screen = pygame.display.set_mode(size) 



draw_board(board)

game_font = pygame.font.SysFont('lucida console', int(SQUARESIZE/1.5))

pygame.display.update()
#print_board(board)

############# MAIN LOOP #############
while not game_over:

    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, (0, 0, 0), (0, 0, width, SQUARESIZE))
                  
            posx = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, (255, 255, 0), (posx, int(SQUARESIZE/2)), RADIUS)
            else:
                pygame.draw.circle(screen, (255, 0, 0), (posx, int(SQUARESIZE/2)), RADIUS)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, (0, 0, 0), (0, 0, width, SQUARESIZE))
            if turn == 0:
                posx = event.pos[0] 
                #col = int(math.floor(posx/SQUARESIZE)) 
                col = int(posx//SQUARESIZE)

            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, 1)

            if winning_move(board, 1):
                label = game_font.render('Player 1 wins!', True, (255, 255, 0))
                screen.blit(label, (40, 10))
                print('Player 1 wins! lineality')
                game_over = True
                break # breaks the for loop
            
        else:
            posx = event.pos[0] 
            col = int(math.floor(posx/SQUARESIZE)) 
            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, 2)
                if winning_move(board, 2):
                    label = game_font.render('Player 2 wins!', True, (255, 0, 0))
                    screen.blit(label, (40, 10))
                    print('Player 2 wins! lineality')
                    game_over = True
                    break

        print_board(board)            
        draw_board(board)
        turn += 1
        turn %= 2 # if 0 player_1, if 1 player_2

draw_board(board)
pygame.display.update()
pygame.time.wait(3000)