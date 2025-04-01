import pygame

from stock import Stock

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0
player_speed = 0
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
candle_width = 43
background = (30, 30, 40)
wick_up = None
wick_down = None
stock = Stock("AAPL", "2024-09-03", "2025-02-08")
index = 33
candle_size = abs(stock.opens[index] - stock.closes[index]) + 1



while running:
    player_click = pygame.mouse.get_pos()

    # player_acc = max()
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    index = 33

    # fill the screen with a color to wipe away anything from last frame
    screen.fill(background)

    rect = pygame.Rect(player_pos[0], player_pos[1], candle_width, candle_size)


    # # pygame.draw.rect(screen, color="green", rect=rect, width=10)
    # pygame.draw.rect(screen, (200, 200, 200), rect)
    #TODO - make this work with stock.highs and lows
    # pygame.draw.line(screen,
    #                  start_pos=(player_pos[0]+rect.width/2, player_pos[1]),
    #                  end_pos=(player_pos[0]+rect.width/2, player_pos[1] + 200),
    #                  color="white")
    pygame.draw.rect(screen, "red", rect)
    # pygame.draw.rect(screen, color="green", rect=rect, width=10)
    pygame.draw.rect(screen, "white", rect, 1)

    # x_acc = abs(player_pos[0] - player_click[0])
    # y_acc = abs(player_pos[1] - player_click[1])
    #
    # if player_pos[0] < player_click[0]:
    #     player_pos.x += (player_speed + x_acc) * dt
    # if player_pos[0] > player_click[0]:
    #     player_pos.x -= (player_speed + x_acc) * dt
    # if player_pos[1] < player_click[1]:
    #     player_pos.y += (player_speed + y_acc) * dt
    # if player_pos[1] > player_click[1]:
    #     player_pos.y -= (player_speed + y_acc) * dt



    # keys = pygame.key.get_pressed()
    # if keys[pygame.K_w]:
    #     player_pos.y -= player_speed * dt
    # if keys[pygame.K_s]:
    #     player_pos.y += player_speed * dt
    # if keys[pygame.K_a]:
    #     player_pos.x -= player_speed * dt
    # if keys[pygame.K_d]:
    #     player_pos.x += player_speed * dt


    # flip() the display to put your work on screen
    pygame.display.flip() #INFO .flip() like flipping a page, i'd call it frame.update or something memba dis

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()

