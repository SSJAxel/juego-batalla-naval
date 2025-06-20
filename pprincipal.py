import pygame
import sys
import random
from configuraciones import ANCHO_VENTANA, ALTO_VENTANA, BLANCO
from configuraciones import FILAS, COLUMNAS, TAM_CASILLA, GRIS, AZUL, ROJO, NEGRO

pygame.init()

# --- AGREGAR ESTO ---
pygame.mixer.init()
pygame.mixer.music.load("principal/god_of_war.ogg")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)  # Loop infinito
# --------------------

ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Batalla Naval")

# Carga y escala el fondo de los barcos en pantalla de inicio
fondo_barcos = pygame.image.load("principal/barcos.jpg")
fondo_barcos_scaled = pygame.transform.scale(fondo_barcos, (ANCHO_VENTANA, ALTO_VENTANA))
offset_x, offset_y = 0, 0

tablero_ancho = COLUMNAS * TAM_CASILLA
tablero_alto = FILAS * TAM_CASILLA
tablero_offset_x = (ANCHO_VENTANA - tablero_ancho) // 2
tablero_offset_y = (ALTO_VENTANA - tablero_alto) // 2

# texto al lado de el cuadrado / tablero de juego
info_x = tablero_offset_x + tablero_ancho + 40  
info_y = tablero_offset_y + tablero_alto // 2   

def crear_tablero():
    return [[0 for _ in range(COLUMNAS)] for _ in range(FILAS)]

def dibujar_tablero(superficie, mostrar_barcos=False):
    for fila in range(FILAS):
        for col in range(COLUMNAS):
            rect = pygame.Rect(
                tablero_offset_x + col * TAM_CASILLA,
                tablero_offset_y + fila * TAM_CASILLA,
                TAM_CASILLA, TAM_CASILLA
            )
            if tablero[fila][col] == 2:
                pygame.draw.rect(superficie, ROJO, rect)  # pega a barco
            elif tablero[fila][col] == 3:
                pygame.draw.rect(superficie, NEGRO, rect)  # errar al barco
            elif tablero[fila][col] == 1 and mostrar_barcos:
                pygame.draw.rect(superficie, AZUL, rect)  
            pygame.draw.rect(superficie, GRIS, rect, 2)

def puede_colocar(tablero, fila, columna, tamaño, horizontal=True):
    for i in range(tamaño):
        f = fila + (i if not horizontal else 0)
        c = columna + (i if horizontal else 0)
        for df in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                nf, nc = f + df, c + dc
                if 0 <= nf < FILAS and 0 <= nc < COLUMNAS:
                    if tablero[nf][nc] != 0:
                        return False
    if horizontal:
        if columna + tamaño > COLUMNAS:
            return False
    else:
        if fila + tamaño > FILAS:
            return False
    return True

def colocar_barcos_juego(tablero, barcos):
    for tamaño, cantidad in barcos:
        for _ in range(cantidad):
            colocado = False
            while not colocado:
                horizontal = random.choice([True, False])
                if horizontal:
                    fila = random.randint(0, FILAS - 1)
                    columna = random.randint(0, COLUMNAS - tamaño)
                else:
                    fila = random.randint(0, FILAS - tamaño)
                    columna = random.randint(0, COLUMNAS - 1)
                if puede_colocar(tablero, fila, columna, tamaño, horizontal):
                    for i in range(tamaño):
                        if horizontal:
                            tablero[fila][columna + i] = 1
                        else:
                            tablero[fila + i][columna] = 1
                    colocado = True

def todos_los_barcos_hundidos(tablero):
    for fila in tablero:
        if 1 in fila:
            return False
    return True

def contar_nave(tablero, fila, col):
    # Cuenta el tamaño de la nave (horizontal o vertical)
    tamaño = 1
    # Horizontal
    c = col - 1
    while c >= 0 and tablero[fila][c] in [1,2]:
        tamaño += 1
        c -= 1
    c = col + 1
    while c < COLUMNAS and tablero[fila][c] in [1,2]:
        tamaño += 1
        c += 1
    # Vertical
    f = fila - 1
    while f >= 0 and tablero[f][col] in [1,2]:
        tamaño += 1
        f -= 1
    f = fila + 1
    while f < FILAS and tablero[f][col] in [1,2]:
        tamaño += 1
        f += 1
    return tamaño

def nave_hundida(tablero, fila, col):
    # Busca en las 4 direcciones si queda alguna parte de la nave sin derribar
    for df, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
        f, c = fila, col
        while 0 <= f < FILAS and 0 <= c < COLUMNAS and tablero[f][c] != 0 and tablero[f][c] != 3:
            if tablero[f][c] == 1:
                return False
            f += df
            c += dc
    return True

def pantalla_inicio():
    fondo = fondo_barcos_scaled
    fuente = pygame.font.SysFont(None, 60)
    botones = [
        {"texto": "Jugar", "rect": pygame.Rect(250, 230, 300, 60)},
        {"texto": "Ver Puntajes", "rect": pygame.Rect(250, 310, 300, 60)},
        {"texto": "Salir", "rect": pygame.Rect(250, 390, 300, 60)},
    ]

    while True:
        ventana.blit(fondo, (0, 0))
        for boton in botones:
            mouse_pos = pygame.mouse.get_pos()
            color = (180, 180, 180) if boton["rect"].collidepoint(mouse_pos) else GRIS
            pygame.draw.rect(ventana, (100, 100, 100), boton["rect"].move(3, 3), border_radius=15)
            pygame.draw.rect(ventana, NEGRO, boton["rect"], 2, border_radius=15)
            pygame.draw.rect(ventana, color, boton["rect"], border_radius=15)
            texto = fuente.render(boton["texto"], True, NEGRO)
            # Centrar el texto en el botón
            texto_rect = texto.get_rect(center=boton["rect"].center)
            ventana.blit(texto, texto_rect)
        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                x, y = evento.pos
                for boton in botones:
                    if boton["rect"].collidepoint(x, y):
                        if boton["texto"] == "Salir":
                            pygame.quit()
                            sys.exit()
                        elif boton["texto"] == "Jugar":
                            barcos_configurados = elegir_nivel()
                            return barcos_configurados
                        elif boton["texto"] == "Ver Puntajes":
                            mostrar_puntajes()

def pedir_nombre():
    # --- DETENER LA MUSICA AL PEDIR NOMBRE ---
    pygame.mixer.music.stop()
    # -----------------------------------------
    nombre = ""
    fuente = pygame.font.SysFont(None, 48)
    input_box = pygame.Rect(250, 250, 300, 50)
    activo = True
    while activo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN and nombre != "":
                    activo = False
                elif evento.key == pygame.K_BACKSPACE:
                    nombre = nombre[:-1]
                else:
                    if len(nombre) < 12 and evento.unicode.isprintable():
                        nombre += evento.unicode

        ventana.fill(BLANCO)
        texto = fuente.render("Ingresá tu nombre:", True, NEGRO)
        ventana.blit(texto, (250, 180))
        pygame.draw.rect(ventana, GRIS, input_box)
        texto_nombre = fuente.render(nombre, True, NEGRO)
        ventana.blit(texto_nombre, (input_box.x + 10, input_box.y + 5))
        pygame.display.flip()
    return nombre

def mostrar_puntajes():
    try:
        with open("puntajes.txt", "r", encoding="utf-8") as f:
            puntajes = []
            for linea in f:
                partes = linea.strip().split(",")
                if len(partes) == 2:
                    nombre, puntos = partes
                    puntajes.append((nombre, int(puntos)))
            puntajes.sort(key=lambda x: x[1], reverse=True)
            top3 = puntajes[:3]
    except FileNotFoundError:
        top3 = []

    fuente = pygame.font.SysFont(None, 48)
    volver_btn = pygame.Rect(300, 500, 200, 50)
    activo = True
    while activo:
        ventana.fill(BLANCO)
        texto = fuente.render("Mejores Puntajes", True, NEGRO)
        ventana.blit(texto, (250, 100))
        for i, (nombre, puntos) in enumerate(top3):
            texto_p = fuente.render(f"{i+1}. {nombre}: {puntos}", True, AZUL)
            ventana.blit(texto_p, (250, 180 + i*60))
        pygame.draw.rect(ventana, GRIS, volver_btn)
        texto_volver = fuente.render("Volver", True, NEGRO)
        ventana.blit(texto_volver, (volver_btn.x + 30, volver_btn.y + 5))
        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                x, y = evento.pos
                if volver_btn.collidepoint(x, y):
                    activo = False

def elegir_nivel():
    niveles = [
        {"texto": "Fácil", "barcos": [(5,1),(4,1),(3,1),(2,2)]},
        {"texto": "Normal", "barcos": [(5,1),(4,1),(3,2),(2,3)]},
        {"texto": "Difícil", "barcos": [(5,1),(4,2),(3,3),(2,4)]},
    ]
    fuente = pygame.font.SysFont(None, 48)
    botones = [pygame.Rect(300, 200 + i*80, 200, 50) for i in range(3)]
    activo = True
    nivel_elegido = 1  # Por defecto "Normal"
    while activo:
        ventana.fill(BLANCO)
        texto = fuente.render("Elegí el nivel:", True, NEGRO)
        ventana.blit(texto, (250, 100))
        for i, rect in enumerate(botones):
            pygame.draw.rect(ventana, GRIS, rect)
            texto_btn = fuente.render(niveles[i]["texto"], True, NEGRO)
            ventana.blit(texto_btn, (rect.x + 30, rect.y + 5))
        pygame.display.flip()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                x, y = evento.pos
                for i, rect in enumerate(botones):
                    if rect.collidepoint(x, y):
                        nivel_elegido = i
                        activo = False
    return niveles[nivel_elegido]["barcos"]

def preguntar_jugar_de_nuevo():
    fuente = pygame.font.SysFont(None, 48)
    ancho, alto = 400, 180
    x = (ANCHO_VENTANA - ancho) // 2
    y = (ALTO_VENTANA - alto) // 2
    rect = pygame.Rect(x, y, ancho, alto)
    boton_si = pygame.Rect(x + 50, y + 100, 120, 50)
    boton_no = pygame.Rect(x + 230, y + 100, 120, 50)
    while True:
        pygame.draw.rect(ventana, (30, 30, 30), rect, border_radius=20)
        pygame.draw.rect(ventana, BLANCO, rect, 3, border_radius=20)
        texto = fuente.render("¿Jugar de nuevo?", True, BLANCO)
        ventana.blit(texto, (x + 60, y + 30))
        pygame.draw.rect(ventana, (0, 180, 0), boton_si, border_radius=10)
        pygame.draw.rect(ventana, (180, 0, 0), boton_no, border_radius=10)
        texto_si = fuente.render("Sí", True, BLANCO)
        texto_no = fuente.render("No", True, BLANCO)
        ventana.blit(texto_si, (boton_si.x + 35, boton_si.y + 5))
        ventana.blit(texto_no, (boton_no.x + 30, boton_no.y + 5))
        pygame.display.flip()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                x_click, y_click = evento.pos
                if boton_si.collidepoint(x_click, y_click):
                    return True
                if boton_no.collidepoint(x_click, y_click):
                    return False

#aca empieza mi programa principal

barcos_configurados = pantalla_inicio()

tablero = crear_tablero()
colocar_barcos_juego(tablero, barcos_configurados)
corriendo = True
disparos = 0
puntaje = 0
nick = pedir_nombre()

while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            # Botón de Reiniciar
            if 650 <= x <= 770 and 20 <= y <= 60:
                tablero = crear_tablero()
                colocar_barcos_juego(tablero, barcos_configurados)
                disparos = 0
                puntaje = 0
                continue  
            if (tablero_offset_x <= x < tablero_offset_x + tablero_ancho and
                tablero_offset_y <= y < tablero_offset_y + tablero_alto):
                fila = (y - tablero_offset_y) // TAM_CASILLA
                col = (x - tablero_offset_x) // TAM_CASILLA
                if 0 <= fila < FILAS and 0 <= col < COLUMNAS:
                    if tablero[fila][col] == 1:
                        tablero[fila][col] = 2
                        disparos += 1
                        puntaje += 5  # acierto y verifica si hundiste la nave
                        tamaño_nave = contar_nave(tablero, fila, col)
                        if nave_hundida(tablero, fila, col):
                            puntaje += tamaño_nave * 10
                    elif tablero[fila][col] == 0:
                        tablero[fila][col] = 3
                        disparos += 1
                        puntaje -= 1  # error al disparar

    ventana.blit(fondo_barcos_scaled, (offset_x, offset_y))
    dibujar_tablero(ventana)
    fuente = pygame.font.SysFont(None, 36)
    # Centro los textos al costado derecho del tablero
    texto_disparos = fuente.render(f"Disparos: {disparos}", True, NEGRO)
    texto_puntaje = fuente.render(f"Puntaje: {puntaje:04d}", True, NEGRO)

    # Centro los textos
    total_text_height = texto_disparos.get_height() + 20 + texto_puntaje.get_height()
    start_y = tablero_offset_y + (tablero_alto - total_text_height) // 2

    ventana.blit(texto_disparos, (info_x, start_y))
    ventana.blit(texto_puntaje, (info_x, start_y + texto_disparos.get_height() + 20))
    if todos_los_barcos_hundidos(tablero):
        fuente = pygame.font.SysFont(None, 60)
        texto = fuente.render("¡Ganaste!", True, BLANCO)
        texto_rect = texto.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2))
        for _ in range(6):
            ventana.blit(fondo_barcos_scaled, (offset_x, offset_y))
            dibujar_tablero(ventana, mostrar_barcos=True)
            if _ % 2 == 0:
                # Fondo negro detrás del texto
                rect_fondo = pygame.Rect(
                    texto_rect.x - 40, texto_rect.y - 20,
                    texto_rect.width + 80, texto_rect.height + 40
                )
                pygame.draw.rect(ventana, (0, 0, 0), rect_fondo, border_radius=20)
                ventana.blit(texto, texto_rect)
            pygame.display.flip()
            pygame.time.wait(300)

        # Botón "Comenzar de nuevo"
        boton_nuevo = pygame.Rect(ANCHO_VENTANA // 2 - 180, ALTO_VENTANA // 2 + 80, 360, 70)
        fuente_btn = pygame.font.SysFont(None, 48)
        activo = True
        while activo:
            ventana.blit(fondo_barcos_scaled, (offset_x, offset_y))
            dibujar_tablero(ventana, mostrar_barcos=True)
            # Fondo negro detrás del texto de victoria
            pygame.draw.rect(ventana, (0, 0, 0), rect_fondo, border_radius=20)
            ventana.blit(texto, texto_rect)
            # botón más grande, fondo negro, letras blancas
            pygame.draw.rect(ventana, (0, 0, 0), boton_nuevo, border_radius=15)
            pygame.draw.rect(ventana, BLANCO, boton_nuevo, 2, border_radius=15)
            texto_btn = fuente_btn.render("Comenzar de nuevo", True, BLANCO)
            texto_btn_rect = texto_btn.get_rect(center=boton_nuevo.center)
            ventana.blit(texto_btn, texto_btn_rect)
            pygame.display.flip()
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    x, y = evento.pos
                    if boton_nuevo.collidepoint(x, y):
                        # Reiniciar juego: pedir nombre, reiniciar tablero, puntaje, disparos, etc.
                        nick = pedir_nombre()
                        tablero = crear_tablero()
                        colocar_barcos_juego(tablero, barcos_configurados)
                        disparos = 0
                        puntaje = 0
                        corriendo = True
                        activo = False
    # Dibujo del botón Reiniciar
    boton_reiniciar = pygame.Rect(650, 20, 120, 40)
    pygame.draw.rect(ventana, GRIS, boton_reiniciar)
    fuente = pygame.font.SysFont(None, 36)
    texto_reiniciar = fuente.render("Reiniciar", True, NEGRO)
    ventana.blit(texto_reiniciar, (boton_reiniciar.x + 10, boton_reiniciar.y + 5))
    pygame.display.flip()

with open("puntajes.txt", "a", encoding="utf-8") as f:
    f.write(f"{nick},{puntaje}\n")
pygame.quit()
sys.exit()