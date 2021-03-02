import pygame,sys
import random


pygame.init()

screen = pygame.display.set_mode((400,600))
pygame.display.set_caption("Flappy Multiplayer")
clock = pygame.time.Clock()
game_font = pygame.font.Font('freesansbold.ttf', 33)
game_font2 = pygame.font.Font('freesansbold.ttf', 20)
game_over = pygame.font.Font('freesansbold.ttf', 60)


#game variables
gravity = 0.25
bird_movement = 0
game_active = False
score =0
high_score=0
first_try = True
playerone= False
playertwo = False

background = pygame.image.load("background.png").convert()
floor = pygame.image.load("floor.png").convert()
floor = pygame.transform.scale2x(floor)
floorsX = 0

def getFloor():
    screen.blit(floor, (floorsX, 500))
    screen.blit(floor, (floorsX + 387, 500))


def create_pipe():
    rand_pipeh = random.choice(pipe_height)
    rand_gap = random.choice(gap_dist)
    new_pipe = pipe.get_rect(midtop=(420,rand_pipeh))
    opp_pipe = pipe.get_rect(midbottom=(420,rand_pipeh-rand_gap))
    return new_pipe, opp_pipe


def move_pipe(pipes):
    for pipex in pipes:
        pipex.centerx -=5
    return pipes

def show_pipe(pipes):
    for pipex in pipes:
        if pipex.bottom>600:
          screen.blit(pipe, pipex)
        else:
            screen.blit(pygame.transform.flip(pipe,False, True), pipex)

def check_collision(pipes):
    for pipex in pipes:
        if bird_rect.colliderect(pipex):
            return True
    return False


def rcheck_collision(pipes):
    for pipex in pipes:
        if rbird_rect.colliderect(pipex):
            return True
    return False

def rotated_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement*3, 1)
    return new_bird

def score_display():
    score_surf = game_font.render("Score " + str(score),True, (0,0,0))
    screen.blit(score_surf, (20,35))

def high_score_display():
    high_score_surf = game_font2.render("High Score "+str(high_score),True,(0,0,0))
    screen.blit(high_score_surf, (20,85))


def gameover(x):
    over = game_over.render("GAME OVER", True, (255,2,2))
    sp = game_font2.render("press space to retry", True, (255,5,2))
    screen.blit(over, (15,255))
    screen.blit(sp, (28,320 ))
    playerwins(x)

def welcome():
    over = game_over.render("Welcome!! ", True, (0,0,230))
    ll = game_font2.render("press space to play", True,(0,0,230))
    screen.blit(over, (15,255))
    screen.blit(ll, (25,320))

def playerwins(who):
    over = game_over.render(who+" wins!!", True, (0,230,23))
    screen.blit(over, (15,200))

bird2 = pygame.image.load("bird2.png").convert_alpha()
bird1 = pygame.image.load("bird1.png").convert_alpha()
bird3 = pygame.image.load("bird3.png").convert_alpha()
birdlist = [bird1, bird2, bird3]
bird_index = 0
bird = birdlist[bird_index]
bird_rect = bird.get_rect(center=(50,300))
BIRDFLAP =  pygame.USEREVENT +1
pygame.time.set_timer(BIRDFLAP, 200)


#second brid info
rbird1 = pygame.image.load("rbird1.png")
rbird2 = pygame.image.load("rbird2.png")
rbird3 = pygame.image.load("rbird3.png")
rbirdlist = [rbird1, rbird2, rbird3]
rbirdindex = 1
rbird = rbirdlist[rbirdindex]
rbird_rect = rbird.get_rect(center=(50,300))
rbird_movement = 0

pipe = pygame.image.load("pipe-green.png")
pipe = pygame.transform.scale(pipe,(70,400))
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_height = [450,350,400,375,285,225,300,425,275]
#gap_dist = [150,125,137,175]
gap_dist = [250]


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key==pygame.K_UP:
                bird_movement=0
                bird_movement -=7
            if event.key ==pygame.K_w:
                rbird_movement = 0
                rbird_movement -=7
            if event.key == pygame.K_SPACE and game_active==False:
                game_active = True
        if event.type == SPAWNPIPE and game_active:
            pipe_list.extend(create_pipe())
        if event.type == BIRDFLAP:
            if bird_index <2:
                bird_index +=1
            else:
                bird_index=0
            bird = birdlist[bird_index]
            if rbirdindex <2:
                rbirdindex +=1
            else:
                rbirdindex=0
            rbird = rbirdlist[rbirdindex]


    screen.blit(background,(0,0))
    if not game_active and first_try:
       welcome()
    if game_active:
            # bird movement
            first_try = False
            if bird_rect.centery < 5:
                bird_movement = 0
                bird_rect.centery = 5
            if rbird_rect.centery < 5:
                rbird_movement = 0
                rbird_rect.centery = 5

            bird_movement += gravity
            rbird_movement += gravity
            rot_bird = rotated_bird(bird)
            rot_rbird = rotated_bird(rbird)
            rbird_rect.centery += rbird_movement
            bird_rect.centery += bird_movement
            screen.blit(rot_bird, bird_rect)
            screen.blit(rot_rbird, rbird_rect)

            # collision code
            if  check_collision(pipe_list) or bird_rect.centery > 494:
                game_active = False
                pipe_list.clear()
                bird_movement = 0
                bird_rect.centery = 300
                rbird_movement = 0
                rbird_rect.centery = 300
                score = 0
                high_score_display()
                playertwo = True
            if rcheck_collision(pipe_list) or rbird_rect.centery>494:
                game_active = False
                pipe_list.clear()
                bird_movement = 0
                bird_rect.centery = 300
                rbird_movement = 0
                rbird_rect.centery = 300
                score = 0
                high_score_display()
                playerone = True
    #pipe movement
            pipe_list = move_pipe(pipe_list)
            show_pipe(pipe_list)

            # floor movement
            floorsX -= 1

            if floorsX < -400:
                floorsX = 0

            if len(pipe_list)>0 and  pipe_list[-1].centerx==bird_rect.centerx:
                score +=1
            if score>high_score:
                high_score = score

    elif not first_try:

        if playerone:
           win = "player 1"
        if playertwo:
            win ="player 2"
        playertwo =False
        playerone =False
        gameover(win)


    score_display()
    high_score_display()
    getFloor()
    pygame.display.update()
    clock.tick(64)




