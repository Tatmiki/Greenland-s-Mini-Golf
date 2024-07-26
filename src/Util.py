import pygame

TILE_SIZE = 50

# Função para desenhar uma seta
def draw_arrow(screen: pygame.Surface, 
               color: pygame.Color, 
               start: pygame.Vector2, 
               end: pygame.Vector2, 
               arrow_width: int = 5, 
               head_length: int = 15) -> None:
    # Calcula as diferenças entre os pontos
    dx = end[0] - start[0]
    dy = end[1] - start[1]

    # Calcula o comprimento da linha
    length = (dx ** 2 + dy ** 2) ** 0.5

    # Normaliza as diferenças para obter o vetor unitário
    unit_dx = dx / length
    unit_dy = dy / length

    # Calcula os pontos para a linha principal da seta
    main_line_start = (start[0] + unit_dy * arrow_width / 2, start[1] - unit_dx * arrow_width / 2)
    main_line_end = (end[0] + unit_dy * arrow_width / 2, end[1] - unit_dx * arrow_width / 2)

    # Calcula os pontos para a cabeça da seta
    arrow_head_base = (end[0] - unit_dx * head_length, end[1] - unit_dy * head_length)
    left_head = (arrow_head_base[0] + unit_dy * arrow_width, arrow_head_base[1] - unit_dx * arrow_width)
    right_head = (arrow_head_base[0] - unit_dy * arrow_width, arrow_head_base[1] + unit_dx * arrow_width)

    # Desenha a linha principal da seta
    pygame.draw.aaline(screen, color, start, arrow_head_base, arrow_width)

    # Desenha a cabeça da seta
    pygame.draw.polygon(screen, color, [end, left_head, right_head])

# Função para ler uma matriz de inteiros de um arquivo .csv
def read_matrix_from_file(filename: str) -> list[list[int]]:
    matrix = []
    with open(filename, 'r') as file:
        for line in file:
            row = [int(value) for value in line.strip().split(',')]
            matrix.append(row)
    return matrix

# Lê um sprite presente em uma spritesheet
def read_one_from_spritesheet(filename: str,
                              position_x: int,
                              position_y: int,
                              region_size: tuple[int, int] = (32, 32)) -> pygame.Surface:
    sprite = pygame.image.load(filename).convert_alpha()
    sprite = sprite.subsurface((position_x * region_size[0], position_y * region_size[1]), region_size)
    
    return sprite

def read_all_from_spritesheet(filename: str,
                              columns: int,
                              lines: int,
                              region_size: tuple[int, int] = (32, 32)) -> list[pygame.Surface]:
    list_sprites = []
    spritesheet = pygame.image.load(filename)
    for x in range(columns):
        for y in range(lines):
            sprite = spritesheet.subsurface((x * region_size[0], y * region_size[1]), region_size)
            list_sprites.append(sprite)
    
    return list_sprites