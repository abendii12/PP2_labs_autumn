import pygame

def main():#в неё упакованы все действия чтобы можно было вызывать main() в конце файла
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()#создаём объект clock чтобы ограничивать кадры в секунду и контролировать скорость цикла
    
    radius = 15
    x = 0
    y = 0
    mode = 'blue'
    points = [] #список точек для отрисовки непрерывной линии
    drawing_tool = 'pen'  # 'pen', 'rectangle', 'circle', 'eraser'
    start_pos = None #хранит позицию где пользователь нажал чтобы начать рисовать фигуру
    shapes = [] #список уже завершённых фигур каждая фигура хранится как кортеж
    
    while True:
        
        pressed = pygame.key.get_pressed()
        
        for event in pygame.event.get(): 
            
            
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_ESCAPE:
                    return
            
                 #переключение цвета
                if event.key == pygame.K_r:
                    mode = 'red'
                elif event.key == pygame.K_g:
                    mode = 'green'
                elif event.key == pygame.K_b:
                    mode = 'blue'
                
                #выбор инструментов
                if event.key == pygame.K_p:
                    drawing_tool = 'pen'
                elif event.key == pygame.K_e:
                    drawing_tool = 'eraser'
                elif event.key == pygame.K_1:
                    drawing_tool = 'rectangle'
                elif event.key == pygame.K_2:
                    drawing_tool = 'circle'
            
            if event.type == pygame.MOUSEBUTTONDOWN:#событие нажатия любой кнопки мыши
                if event.button == 1: #левая кнопка
                    if drawing_tool in ['rectangle', 'circle']:
                        start_pos = event.pos #если выбран режим рисования фигуры rectangle или circle то сохраняем start_pos = event.pos это точка начала фигуры
                    else:
                        radius = min(200, radius + 1)
                elif event.button == 3: #правая кнопка уменьшает толщину кисти но не ниже 1 через max
                    radius = max(1, radius - 1)
            
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and start_pos is not None:
                    end_pos = event.pos #точка где отпустили мышь
                    if drawing_tool == 'rectangle':
                        shapes = shapes + [('rectangle', start_pos, end_pos, mode)]
                    elif drawing_tool == 'circle':
                        '''в список shapes добавляем кортеж с типом фигуры start_pos end_pos и текущим 
                        цветом mode затем сбрасываем start_pos = None чтобы система знала что фигура завершена'''
                        shapes = shapes + [('circle', start_pos, end_pos, mode)]
                    start_pos = None
            
            if event.type == pygame.MOUSEMOTION:
                #если активен инструмент pen или eraser добавляем текущую позицию курсора в список points
                if drawing_tool == 'pen' or drawing_tool == 'eraser':
                    position = event.pos
                    points = points + [position]
                    
                
        screen.fill((0, 0, 0))
        
        #рисуем все фигуры 
        for shape in shapes:
            if shape[0] == 'rectangle':
                rect = pygame.Rect(shape[1], (shape[2][0] - shape[1][0], shape[2][1] - shape[1][1]))
                color = get_color(shape[3])
                pygame.draw.rect(screen, color, rect, 3)
            elif shape[0] == 'circle':
                center = shape[1]
                radius_shape = int(((shape[2][0] - shape[1][0])**2 + (shape[2][1] - shape[1][1])**2)**0.5)
                color = get_color(shape[3])
                pygame.draw.circle(screen, color, center, radius_shape, 3)
        
        #рисуем все точки
        i = 0
        while i < len(points) - 1:
            if drawing_tool == 'pen':
                drawLineBetween(screen, i, points[i], points[i + 1], radius, mode)
            elif drawing_tool == 'eraser':
                eraseLineBetween(screen, i, points[i], points[i + 1], radius)
            i += 1
        
        #показываем текущую фигуру во время рисования
        if start_pos is not None:
            current_pos = pygame.mouse.get_pos()
            if drawing_tool == 'rectangle':
                rect = pygame.Rect(start_pos, (current_pos[0] - start_pos[0], current_pos[1] - start_pos[1]))
                color = get_color(mode)
                pygame.draw.rect(screen, color, rect, 3)
            elif drawing_tool == 'circle':
                radius_shape = int(((current_pos[0] - start_pos[0])**2 + (current_pos[1] - start_pos[1])**2)**0.5)
                color = get_color(mode)
                pygame.draw.circle(screen, color, start_pos, radius_shape, 3)
        
        pygame.display.flip()
        
        clock.tick(60)

def get_color(color_mode):
    if color_mode == 'blue':
        return (0, 0, 255)
    elif color_mode == 'red':
        return (255, 0, 0)
    elif color_mode == 'green':
        return (0, 255, 0)

def drawLineBetween(screen, index, start, end, width, color_mode):
    #насыщенные цвета без прозрачности
    if color_mode == 'blue':
        color = (0, 0, 255)  #чистый синий
    elif color_mode == 'red':
        color = (255, 0, 0)  #чистый красный
    elif color_mode == 'green':
        color = (0, 255, 0)  #чистый зеленый
    
    dx = start[0] - end[0]
    dy = start[1] - end[1]
    iterations = max(abs(dx), abs(dy))
    #функция рисования линии между двумя точками
    for i in range(iterations):
        progress = 1.0 * i / iterations
        aprogress = 1 - progress
        x = int(aprogress * start[0] + progress * end[0])
        y = int(aprogress * start[1] + progress * end[1])
        pygame.draw.circle(screen, color, (x, y), width)

def eraseLineBetween(screen, index, start, end, width):
    color = (0, 0, 0)  # черный цвет для стирания
    
    dx = start[0] - end[0]
    dy = start[1] - end[1]
    iterations = max(abs(dx), abs(dy))
    
    #по точкам плавно переходим от start к end
    for i in range(iterations):
        progress = 1.0 * i / iterations
        aprogress = 1 - progress
        x = int(aprogress * start[0] + progress * end[0])
        y = int(aprogress * start[1] + progress * end[1])
        pygame.draw.circle(screen, color, (x, y), width)

main()