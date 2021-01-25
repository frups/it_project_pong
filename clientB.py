import pygame, sys, random, socketio

io = socketio.Client()

@io.event
def connect():
    print('connection established')
    
@io.event
def connect_error():
    print("The connection failed!")

@io.event
def disconnect():
    print('disconnected from server')


### Update from server ###
@io.on('r')
def on_message(arg):
    global player_1_score, player_2_score
    print('response: ', arg)
    ball.x = int(arg['b_x'])
    ball.y = int(arg['b_y'])
    opponent.y = int(arg['p'])
    opponent_speed = int(arg['p'])
    player_1_score = int(arg['sa'])
    player_2_score = int(arg['sb'])


### Setup ###
pygame.init()
clock = pygame.time.Clock()


def score_update(x):
    global v_sound
    #if x:
        #player_2_score += 1
    #else:
        #player_1_score +=1

    if player_1_score > 9:
        victorySound.play()
        v_sound = True

    if player_2_score > 9:
        victorySound.play()
        v_sound = True




def ball_animation():
    global ball_speed_x, ball_speed_y

    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top <= 0 or ball.bottom >= screen_height:
        ball_speed_y *= -1
    if ball.left <= 0:
        score_update(1)
        ball_restart()

    if ball.right >= screen_width:
        score_update(0)
        ball_restart()

    if ball.colliderect(player) or ball.colliderect(opponent):
        ball_speed_x *= -1
        hitSound.play()



def player_animation():
    player.y += player_speed
    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height


def opponent_animation():
    opponent.y += opponent_speed
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= screen_height:
        opponent.bottom = screen_height


def ball_restart():
        global ball_speed_x, ball_speed_y
        ball.center = (screen_width/2, screen_height/2)
        ball_speed_y *= random.choice((1,-1))
        ball_speed_x *= random.choice((1,-1))


### Main window setup ###
screen_width = 1280
screen_height = 960
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('pong_clientB')

### Rectangles ###
ball = pygame.Rect(screen_width/2-15,screen_height/2-15,30,30)
player = pygame.Rect(screen_width-30,screen_height/2-70 ,20,140)
opponent = pygame.Rect(10,screen_height/2-70 ,20,140)

### Colors ###
bg_color = (62,77,34)
light_grey = (173,165,144)

### Connect to serv ###
#Here write your public ip from you're running server, ofcourse you need to enable port 3000 in your firewall#
io.connect('Your_Adress:3000', namespaces=['/'])
io.sleep(1)
print('my sid is', io.sid)


### Speed ###
ball_speed_x = 6
ball_speed_y = 6
player_speed = 0
opponent_speed = 0

### Sounds are disabled just put that files in folder witch you're running code###
#hitSound = pygame.mixer.Sound("tennisserve.wav")
#victorySound = pygame.mixer.Sound("Cheering.wav")

#music = pygame.mixer.music.load("music.wav")
#pygame.mixer.music.play(-1)


### Score ###
player_1_score = 0
player_2_score = 0
v_sound = False


### Input ###
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player_speed +=6
            if event.key == pygame.K_UP:
                player_speed -=6
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player_speed -=6
            if event.key == pygame.K_UP:
                player_speed +=6




    ball_animation()
    player_animation()
    opponent_animation()

    ### Visuals ###
    screen.fill(bg_color)
    pygame.draw.rect(screen,light_grey,player)
    pygame.draw.rect(screen,light_grey,opponent)
    pygame.draw.ellipse(screen,light_grey,ball)
    pygame.draw.aaline(screen, light_grey, (screen_width/2,0),(screen_width/2,screen_height))
    font = pygame.font.SysFont('courier new', 50)
    text_score_1 = font.render("Player 2: " + str(player_1_score) , 1, (132, 165, 202))
    screen.blit(text_score_1, (screen_width // 4 - (text_score_1.get_width() / 2), screen_height // 6 ))
    text_score_2 = font.render("Player 1: " + str(player_2_score), 1, (219, 202, 105))
    screen.blit(text_score_2, ((screen_width // 4) * 3 - (text_score_2.get_width() / 2), screen_height // 6))
    font_2 = pygame.font.SysFont('comicsans', 100, False)

    if v_sound:
        if player_1_score > 9:
            text = font_2.render("Player 2 won!", 1, (132, 165, 202))
            screen.blit(text, (screen_width // 2 - (text.get_width() / 2), screen_height // 3))
            pygame.display.update()
            i = 0
            while i < 300:
                pygame.time.delay(10)
                i += 1
            run = False
            player_1_score = 0
            player_2_score = 0
        if player_2_score > 9:
            text_2 = font_2.render("Player 1 won!", 1, (219, 202, 105))
            screen.blit(text_2, (screen_width // 2 - (text_2.get_width() / 2), screen_height // 3))
            pygame.display.update()
            i = 0
            while i < 300:
                pygame.time.delay(10)
                i += 1
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        i = 301
                        pygame.quit()
            run = False
            player_1_score = 0
            player_2_score = 0
        v_sound = False

    ### Updating the window ###
    pygame.display.flip()
    clock.tick(60)
    ### Send response to server ###
    if io.connected==True:
        print("emit")
        io.emit('b', {'p_B': player.y})
    io.on('r', on_message)