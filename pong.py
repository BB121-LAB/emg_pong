#!/usr/bin/python
import pygame, sys, random

# color tuples 
WHITE = (255, 255, 255)
ORANGE = (255, 140, 0)
GREEN = (0, 255, 0)
BG = (20, 20, 20)

# global vars
RES_X = 800
RES_Y = 600
PADDLE_WIDTH = 30
PADDLE_HEIGHT = 100
BALL_WIDTH = 20
BALL_HEIGHT = 20

class Ball:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.x_vel = 0
        self.y_vel = 0
        self.reset()
    def update_position(self):
        # check for top or bottom collision
        if(self.y == 0 and self.y_vel < 0):
            self.y_vel = -self.y_vel
        if(self.y == (RES_Y - BALL_HEIGHT) and self.y_vel > 0):
            self.y_vel = -self.y_vel
        self.x += self.x_vel
        self.y += self.y_vel
    def draw(self, window):
        pygame.draw.rect(window, GREEN, (self.x, self.y, BALL_WIDTH, BALL_HEIGHT))
    def reset(self):
        self.x = (RES_X // 2) - (BALL_WIDTH // 2)
        self.y = (RES_Y // 2) - (BALL_HEIGHT // 2)
        self.y_vel = 0
        self.x_vel = 5

class Paddle:
    def __init__(self, x_pos):
        self.x = x_pos
        self.y = 0
        self.y_vel = 0
        self.not_edge = 1
        self.reset()
    def update_position(self):
        if(self.y == 0 and self.y_vel < 0):
            self.not_edge = 0
        elif(self.y == (RES_Y - PADDLE_HEIGHT) and self.y_vel > 0):
            self.not_edge = 0
        else:
            self.not_edge = 1
        self.y += self.y_vel * self.not_edge
    def draw(self, window):
        pygame.draw.rect(window, WHITE, (self.x, self.y, PADDLE_WIDTH, PADDLE_HEIGHT))
    def reset(self):
        self.y = (RES_Y // 2) - (PADDLE_HEIGHT // 2)
        self.y_vel = 5       
        
def window_clear(window):
    window.fill(BG)
    pygame.draw.line(window, ORANGE, [RES_X // 2, 0], [RES_X // 2, RES_Y])

def game_reset():
    player_paddle.reset()
    ai_paddle.reset()
    ball.reset()

def main():
    pygame.init()
    clock = pygame.time.Clock()
    window = pygame.display.set_mode((RES_X, RES_Y), 0, 32)
    pygame.display.set_caption('One-button Pong')
    
    # create the things
    global player_paddle, ai_paddle, ball
    player_paddle = Paddle(10)
    ai_paddle     = Paddle(RES_X - PADDLE_WIDTH - 10)
    ball = Ball()

    # game loop
    while True:
        
        # clear window 
        window_clear(window)
        
        # update and draw pieces
        player_paddle.update_position()
        ai_paddle.update_position()
        ball.update_position()
        ball.draw(window)
        player_paddle.draw(window)
        ai_paddle.draw(window)
        
        # check if ball passes one of the walls
        if(ball.x <= 0 or ball.x >= RES_X):
            game_reset()
        
        # check if ball collides with paddle
        if(ball.x == player_paddle.x + PADDLE_WIDTH):
            if(ball.y in range(player_paddle.y, player_paddle.y + PADDLE_HEIGHT) or
                (ball.y + BALL_HEIGHT) in range(player_paddle.y, player_paddle.y + PADDLE_HEIGHT)):
                ball.x_vel = -ball.x_vel
                ball.y_vel = random.choice([1, 2, 5]) * random.choice([-1, 1])
        if(ball.x + BALL_WIDTH == ai_paddle.x):
            if(ball.y in range(ai_paddle.y, ai_paddle.y + PADDLE_HEIGHT) or
                (ball.y + BALL_HEIGHT) in range(ai_paddle.y, ai_paddle.y + PADDLE_HEIGHT)):
                ball.x_vel = -ball.x_vel
                ball.y_vel = random.choice([1, 2, 5]) * random.choice([-1, 1])

        # make AI paddle chase ball when it's in the AI's court
        if(ball.x > RES_X // 2 and ball.x_vel > 0):
            ai_center = ai_paddle.y + (PADDLE_HEIGHT // 2)
            if(ball.y > ai_center + 20):
                ai_paddle.y_vel = 5
            elif(ball.y < ai_center - 20):
                ai_paddle.y_vel = -5
        else:
            ai_paddle.y_vel = 0
        
        # draw buffer to screen
        pygame.display.update()
 
        # handle user events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            """
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                player_paddle.y_vel = -5
            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                player_paddle.y_vel = 5
            """
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                player_paddle.y_vel *= -1
        
        # for FPS regulation
        clock.tick(60)

if __name__ == '__main__':
    main()
