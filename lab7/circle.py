import pygame

pygame.init()

screen=pygame.display.set_mode((800,600))

clock=pygame.time.Clock()

white=(255,255,255)
red=(255,0,0)

x=30
y=30


done=False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        

    keys=pygame.key.get_pressed()
    if keys[pygame.K_RIGHT] and x < 775:
        x += 20
    if keys[pygame.K_LEFT] and x > 25:
        x -= 20
    if keys[pygame.K_UP]:
        y -= 20
    if keys[pygame.K_DOWN]:
        y += 20

    
    if y > 600:     
        y = 0       
    elif y < 0:     
        y = 600     

    screen.fill(white)
    pygame.draw.circle(screen, red, (x, y), 25)
    pygame.display.flip()
    clock.tick(60)
 