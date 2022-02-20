import pygame, random

SCREEN_DIM = (432, 768)
MAX_HEIGHT = -300
FLOOR_Y = 100
BIRD_INIT_POS = (80, SCREEN_DIM[1]/2)
BIRD_DIM = (51, 36)
PIPE_DIM = (78, 480)
PIPE_GEN_TIME = 1500 # in ms
BOTTOM_PIPE_MAX_HEIGHT = 480
PIPE_X_START = 500
PIPE_GAP = 250
GRAVITY = 0.35
JUMP = 8
MOVING_SPEED = 3
SCORE_POS = (SCREEN_DIM[0]/2, 100)
ACTIVE_HIGH_SCORE_POS = (SCREEN_DIM[0]/2, 50)
DEAD_HIGH_SCORE_POS = (SCREEN_DIM[0]/2, SCREEN_DIM[1]-FLOOR_Y-50)
GAME_OVER_SURFACE_DIM = (276, 400)

game_active = False

score = 0
high_score = 0
can_score = True


    
def draw_floor():
    global floor_1, floor_2, floor_surface
    floor_1.left -= MOVING_SPEED
    floor_2.left -= MOVING_SPEED
    if floor_1.left < -SCREEN_DIM[0]:
        floor_1.left = 0
        floor_2.left = floor_1.left + SCREEN_DIM[0]
    screen.blit(source=floor_surface, dest=floor_1)
    screen.blit(source=floor_surface, dest=floor_2)
 
def create_pipe():
    global pipe_surface
    pipe_y_start = SCREEN_DIM[1]-FLOOR_Y-random.randint(0, BOTTOM_PIPE_MAX_HEIGHT)
    pipe_rect_1 = pipe_surface.get_rect(
        midtop=(PIPE_X_START, pipe_y_start))
    pipe_y_start_flipped = pipe_y_start-PIPE_GAP
    if pipe_y_start_flipped <= 0:
        pipe_y_start_flipped = -1000
    pipe_rect_2 = pipe_surface_flipped.get_rect(
        midbottom=(PIPE_X_START, pipe_y_start_flipped))
    return (pipe_rect_1, pipe_rect_2)

def move_pipes():
    global pipe_list
    for (pipe1,pipe2) in pipe_list:
        pipe1.centerx -= MOVING_SPEED
        pipe2.centerx -= MOVING_SPEED
        if pipe1.right < -10:
            pipe_list.remove((pipe1,pipe2))
    return pipe_list

def draw_pipes():
    global pipe_list, pipe_surface, pipe_surface_flipped
    for (pipe1,pipe2) in pipe_list:
        screen.blit(source=pipe_surface, dest=pipe1)
        screen.blit(source=pipe_surface_flipped, dest=pipe2)

def collide():
    global pipe_list, bird_rect
    for (pipe1,pipe2) in pipe_list:
        if bird_rect.colliderect(pipe1) or bird_rect.colliderect(pipe2):
            return True
    if bird_rect.top <= MAX_HEIGHT or bird_rect.bottom >= SCREEN_DIM[1]-FLOOR_Y:
        return True
    return False

def rotate_bird(): # rotate bird as it jumps and falls
    global bird_surface, bird_y_speed
    rotated_bird_surface = pygame.transform.rotate(
        surface=bird_surface, angle= -4*bird_y_speed) # rotated angle proportional to falling speed
    return rotated_bird_surface

def animate_bird():
    global bird_surface_list, bird_index, bird_rect
    new_bird = bird_surface_list[bird_index]
    new_bird_rect = new_bird.get_rect(center = (BIRD_INIT_POS[0],bird_rect.centery))
    return new_bird, new_bird_rect

def score_display():
    global score, game_active
    if game_active: 
        score_surface = game_font.render(str(score), True, (255,255,255))
        score_rect = score_surface.get_rect(center=SCORE_POS)
        high_score_surface = high_score_font.render(f"HiGH SCORE: {str(high_score)}", True, (255,255,255))
        high_score_rect = high_score_surface.get_rect(center = ACTIVE_HIGH_SCORE_POS)
        
    else:
        score_surface = game_font.render(f"SCORE: {str(score)}", True, (255,255,255))
        score_rect = score_surface.get_rect(center=SCORE_POS)
        high_score_surface = game_font.render(f"HiGH SCORE: {str(high_score)}", True, (255,255,255))
        high_score_rect = high_score_surface.get_rect(center=DEAD_HIGH_SCORE_POS)
    screen.blit(source=score_surface, dest=score_rect)
    screen.blit(source=high_score_surface, dest=high_score_rect)
        
 
def scoring():
    global score, can_score, high_score, score_sound
    if pipe_list:
        for (pipe,null) in pipe_list:
            if can_score and bird_rect.left-10 < pipe.right < bird_rect.left:
                score += 1
                can_score = False
                score_sound.play()
                if high_score < score:
                    high_score = score
            if pipe.centerx < 0:
                can_score = True

def replay():
    global game_active, pipe_list, bird_rect, bird_y_speed, can_score, score, high_score
    game_active = True
    pipe_list.clear()
    bird_rect.center = BIRD_INIT_POS
    bird_y_speed = -JUMP
    can_score = True
    if score > high_score:
        high_score = score
    score = 0
    swoosh_sound.play()
    


pygame.init()
screen = pygame.display.set_mode(size=SCREEN_DIM)  # creates a Surface object
pygame.display.set_caption("Flappy Bird")
pygame.display.set_icon(pygame.image.load('assets/images/favicon.ico').convert())
clock = pygame.time.Clock()

game_font = pygame.font.Font('assets/04B_19.ttf', 40)
high_score_font = pygame.font.Font('assets/04B_19.ttf', 20)

# background
# convert() converts image to a more efficient file for pygame
bg_surface = pygame.image.load('assets/images/background-day.png').convert()
bg_surface = pygame.transform.scale(bg_surface, SCREEN_DIM)

# floor
floor_surface = pygame.image.load('assets/images/base.png').convert()
# floor_surface = pygame.transform.scale2x(floor_surface)
floor_surface = pygame.transform.scale(floor_surface, (SCREEN_DIM[0], FLOOR_Y))
floor_x_pos = 0
floor_1 = floor_surface.get_rect(topleft=(0, SCREEN_DIM[1]-FLOOR_Y))
floor_2 = floor_surface.get_rect(topleft=(0 + SCREEN_DIM[0], SCREEN_DIM[1]-FLOOR_Y))
    


# bird
up_flap = pygame.transform.scale(pygame.image.load('assets/images/yellowbird-upflap.png').convert_alpha(), BIRD_DIM)
mid_flap = pygame.transform.scale(pygame.image.load('assets/images/yellowbird-midflap.png').convert_alpha(), BIRD_DIM)
down_flap = pygame.transform.scale(pygame.image.load('assets/images/yellowbird-downflap.png').convert_alpha(), BIRD_DIM)
BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 50)

bird_surface_list = [up_flap, mid_flap, down_flap]
bird_index = 0
bird_surface = bird_surface_list[bird_index]
bird_rect = bird_surface.get_rect(center=BIRD_INIT_POS)
bird_y_speed = 0

# pipes
pipe_surface = pygame.image.load('assets/images/pipe-green.png').convert()
pipe_surface = pygame.transform.scale(pipe_surface, PIPE_DIM)
pipe_surface_flipped = pygame.transform.flip(surface=pipe_surface, flip_x=True, flip_y=True)
pipe_list = [] #list of rects of
SPAWNPIPE = pygame.USEREVENT  # creates custom event
pygame.time.set_timer(SPAWNPIPE, PIPE_GEN_TIME)
# creates timer to repeat SPAWNPIPE event every 1000 milisecond

# game over
game_over_surface = pygame.image.load('assets/images/message.png').convert_alpha()
game_over_surface = pygame.transform.scale(game_over_surface, GAME_OVER_SURFACE_DIM)
game_over_rect = game_over_surface.get_rect(center= (SCREEN_DIM[0]/2, SCREEN_DIM[1]/2))

# sounds
death_sound = pygame.mixer.Sound('assets/sounds/die.wav')
hit_sound = pygame.mixer.Sound('assets/sounds/hit.wav')
hit_sound.set_volume(death_sound.get_volume()/5)
score_sound = pygame.mixer.Sound('assets/sounds/point.wav')
wing_sound = pygame.mixer.Sound('assets/sounds/wing.wav')
swoosh_sound = pygame.mixer.Sound('assets/sounds/swoosh.wav')

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_active:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird_y_speed = -JUMP
                wing_sound.play()
            if event.type == SPAWNPIPE:
                pipe_list.append(create_pipe())
            if event.type == BIRDFLAP:
                if bird_index >= 0:
                    bird_index += 1
                else:
                    bird_index -= 1
                if bird_index > 2:
                    bird_index = -1
                elif bird_index < -3:
                    bird_index = 0
                bird_surface, bird_rect = animate_bird()
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                # replay game
                replay()

    # background
    screen.blit(source=bg_surface, dest=(0, 0))

    if game_active:
        # bird
        screen.blit(source=rotate_bird(), dest=bird_rect)
        bird_y_speed += GRAVITY
        bird_rect.centery += bird_y_speed

        # pipes
        pipe_list = move_pipes()
        draw_pipes()

        # collision
        if collide():
            game_active = False
            hit_sound.play()
            death_sound.play()
        # score and high score
        
        scoring()
    else:
        screen.blit(source=game_over_surface, dest=game_over_rect)
    score_display()


    # floor
    draw_floor()
    
    pygame.display.update()
    clock.tick(120)  # limit framerate upto 120 fps
pygame.quit()
pygame.QUIT