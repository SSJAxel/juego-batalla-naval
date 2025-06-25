import pygame
import sys
import random
from configuraciones import BLANCO
from configuraciones import TAM_CASILLA, GRIS, AZUL, ROJO, NEGRO

# Inicialización
pygame.init()
# Música de fondo estilo tribal
try:
    pygame.mixer.music.load("tribe-drum-loop-103173.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)  # Loop infinito
except Exception as e:
    print("No se pudo cargar la música de fondo:", e)

# Cargar sonido de disparo
try:
    sonido_disparo = pygame.mixer.Sound("single-pistol-gunshot-33-37187.mp3")
    sonido_disparo.set_volume(0.10)
except Exception as e:
    print("No se pudo cargar el sonido de disparo:", e)

ANCHO_VENTANA = 1280
ALTO_VENTANA = 720
ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))

# Carga y escalado de la imagen de fondo para el menú
fondo_mar = pygame.image.load("barcos.jpg")
img_w, img_h = fondo_mar.get_size()
scale = min(ANCHO_VENTANA / img_w, ALTO_VENTANA / img_h)
new_w, new_h = int(img_w * scale), int(img_h * scale)
fondo_mar_scaled = pygame.transform.scale(fondo_mar, (new_w, new_h))
offset_x = (ANCHO_VENTANA - new_w) // 2
offset_y = (ALTO_VENTANA - new_h) // 2

# Carga y escalado de la imagen de fondo para el juego
mar = pygame.image.load("mar.jpg")
img_w, img_h = mar.get_size()
scale = min(ANCHO_VENTANA / img_w, ALTO_VENTANA / img_h)
new_w, new_h = int(img_w * scale), int(img_h * scale)
mar_scaled = pygame.transform.scale(mar, (new_w, new_h))
offset_x_mar = (ANCHO_VENTANA - new_w) // 2
offset_y_mar = (ALTO_VENTANA - new_h) // 2

# Cambia la fuente global a una de estilo griego o similar
# Usaremos 'Papyrus' si está disponible, o una fuente alternativa decorativa
FUENTE_GRIEGA = None
for fuente_nombre in ["Papyrus", "Segoe Script", "Garamond", "Times New Roman"]:
    try:
        test_font = pygame.font.SysFont(fuente_nombre, 24)
        if test_font:
            FUENTE_GRIEGA = fuente_nombre
            break
    except:
        continue
if FUENTE_GRIEGA is None:
    FUENTE_GRIEGA = "arial"  # Fallback

def dibujar_boton_menu(superficie, texto, rect, activo=False):
    color_base = (30, 60, 90, 180)
    color_hover = (60, 100, 140, 220)
    color = color_hover if activo else color_base
    boton_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    pygame.draw.rect(boton_surface, color, boton_surface.get_rect(), border_radius=18)
    pygame.draw.rect(boton_surface, (255, 255, 255, 120), boton_surface.get_rect(), 3, border_radius=18)
    superficie.blit(boton_surface, rect.topleft)
    fuente_btn = pygame.font.SysFont(FUENTE_GRIEGA, 38, bold=True)
    texto_render = fuente_btn.render(texto, True, (230, 230, 230))
    texto_rect = texto_render.get_rect(center=rect.center)
    superficie.blit(texto_render, texto_rect)

def pantalla_inicio():
    titulo_font = pygame.font.SysFont(FUENTE_GRIEGA, 70, bold=True)
    titulo = titulo_font.render("BATALLA NAVAL", True, (255, 255, 255))
    sombra = titulo_font.render("BATALLA NAVAL", True, (0, 0, 0))
    titulo_rect = titulo.get_rect(center=(ANCHO_VENTANA // 2, 110))
    sombra_rect = titulo_rect.copy()
    sombra_rect.move_ip(4, 4)
    botones = [
        {"texto": "Facil", "rect": pygame.Rect(ANCHO_VENTANA//2 - 150, 240, 300, 65)},
        {"texto": "Normal", "rect": pygame.Rect(ANCHO_VENTANA//2 - 150, 330, 300, 65)},
        {"texto": "Dificil", "rect": pygame.Rect(ANCHO_VENTANA//2 - 150, 420, 300, 65)},
    ]
    while True:
        ventana.blit(fondo_mar_scaled, (offset_x, offset_y))
        ventana.blit(sombra, sombra_rect)
        ventana.blit(titulo, titulo_rect)
        mouse_pos = pygame.mouse.get_pos()
        for boton in botones:
            activo = boton["rect"].collidepoint(mouse_pos)
            dibujar_boton_menu(ventana, boton["texto"], boton["rect"], activo)
        pygame.display.flip()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                for boton in botones:
                    if boton["rect"].collidepoint(evento.pos):
                        esperar_soltado()
                        return boton["texto"].lower()

def esperar_soltado():
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.MOUSEBUTTONUP:
                esperando = False

def menu_principal():
    fuente = pygame.font.SysFont(FUENTE_GRIEGA, 60, bold=True)
    fuente_btn = pygame.font.SysFont(FUENTE_GRIEGA, 40, bold=True)
    botones = [
        {"texto": "Jugar", "rect": pygame.Rect(ANCHO_VENTANA//2 - 150, 250, 300, 70)},
        {"texto": "Ver Puntajes", "rect": pygame.Rect(ANCHO_VENTANA//2 - 150, 350, 300, 70)},
        {"texto": "Salir", "rect": pygame.Rect(ANCHO_VENTANA//2 - 150, 450, 300, 70)},
    ]
    while True:
        ventana.blit(fondo_mar_scaled, (offset_x, offset_y))
        titulo = fuente.render("BATALLA NAVAL", True, (255,255,255))
        sombra = fuente.render("BATALLA NAVAL", True, (0,0,0))
        ventana.blit(sombra, (ANCHO_VENTANA//2 - titulo.get_width()//2 + 4, 114))
        ventana.blit(titulo, (ANCHO_VENTANA//2 - titulo.get_width()//2, 110))
        mouse_pos = pygame.mouse.get_pos()
        for boton in botones:
            activo = boton["rect"].collidepoint(mouse_pos)
            dibujar_boton_menu(ventana, boton["texto"], boton["rect"], activo)
        pygame.display.flip()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                for boton in botones:
                    if boton["rect"].collidepoint(evento.pos):
                        esperar_soltado()
                        return boton["texto"].lower()

def mostrar_puntajes():
    fuente = pygame.font.SysFont(FUENTE_GRIEGA, 40, bold=True)
    ventana.blit(fondo_mar_scaled, (offset_x, offset_y))
    try:
        with open("puntajes.txt", "r", encoding="utf-8") as f:
            puntajes = [line.strip().split(',') for line in f if ',' in line]
            puntajes = sorted(puntajes, key=lambda x: int(x[1]), reverse=True)[:3]
    except Exception:
        puntajes = []
    titulo = fuente.render("Mejores Puntajes", True, (255,255,255))
    ventana.blit(titulo, (ANCHO_VENTANA//2 - titulo.get_width()//2, 100))
    fuente2 = pygame.font.SysFont(FUENTE_GRIEGA, 32)
    for i, (nombre, puntaje) in enumerate(puntajes):
        texto = fuente2.render(f"{i+1}. {nombre} - {int(puntaje):04d}", True, (255,255,255))
        ventana.blit(texto, (ANCHO_VENTANA//2 - 200, 180 + i*40))
    texto_volver = fuente2.render("[Click para volver]", True, (200,200,200))
    ventana.blit(texto_volver, (ANCHO_VENTANA//2 - 120, ALTO_VENTANA - 80))
    pygame.display.flip()
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                esperar_soltado()
                esperando = False

# --- FUNCIONES AUXILIARES ---
def crear_tablero():
    return [[0 for _ in range(COLUMNAS)] for _ in range(FILAS)]

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

def dibujar_tablero(superficie, mostrar_barcos=False):
    for fila in range(FILAS):
        for col in range(COLUMNAS):
            rect = pygame.Rect(
                tablero_offset_x + col * TAM_CASILLA,
                tablero_offset_y + fila * TAM_CASILLA,
                TAM_CASILLA, TAM_CASILLA
            )
            if tablero[fila][col] == 2:
                pygame.draw.rect(superficie, ROJO, rect)  # Impacto
            elif tablero[fila][col] == 3:
                pygame.draw.rect(superficie, NEGRO, rect)  # Agua fallida
            elif tablero[fila][col] == 1 and mostrar_barcos:
                pygame.draw.rect(superficie, AZUL, rect)  # Barco solo si mostrar_barcos es True
            pygame.draw.rect(superficie, GRIS, rect, 2)

def todos_los_barcos_hundidos(tablero):
    for fila in tablero:
        if 1 in fila:
            return False
    return True

def contar_nave(tablero, fila, col):
    tamaño = 1
    c = col - 1
    while c >= 0 and tablero[fila][c] in [1,2]:
        tamaño += 1
        c -= 1
    c = col + 1
    while c < COLUMNAS and tablero[fila][c] in [1,2]:
        tamaño += 1
        c += 1
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
    for df, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
        f, c = fila, col
        while 0 <= f < FILAS and 0 <= c < COLUMNAS and tablero[f][c] != 0 and tablero[f][c] != 3:
            if tablero[f][c] == 1:
                return False
            f += df
            c += dc
    return True

def pedir_nombre_pygame():
    nombre = ""
    fuente = pygame.font.SysFont(FUENTE_GRIEGA, 48)
    input_box = pygame.Rect(ANCHO_VENTANA//2 - 200, ALTO_VENTANA//2, 400, 60)
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    if nombre.strip() == "":
                        nombre = "Jugador"
                    return nombre  # Sale inmediatamente al presionar Enter
                elif evento.key == pygame.K_BACKSPACE:
                    nombre = nombre[:-1]
                else:
                    if len(nombre) < 16 and evento.unicode.isprintable():
                        nombre += evento.unicode
        ventana.blit(mar_scaled, (offset_x_mar, offset_y_mar))
        overlay = pygame.Surface((ANCHO_VENTANA, ALTO_VENTANA), pygame.SRCALPHA)
        overlay.fill((0,0,0,180))
        ventana.blit(overlay, (0,0))
        texto = fuente.render("Ingresa tu nombre:", True, (255,255,255))
        ventana.blit(texto, (ANCHO_VENTANA//2 - texto.get_width()//2, ALTO_VENTANA//2 - 80))
        pygame.draw.rect(ventana, (255,255,255), input_box, 2)
        texto_nombre = fuente.render(nombre, True, (255,255,255))
        ventana.blit(texto_nombre, (input_box.x+10, input_box.y+10))
        pygame.display.flip()
    return nombre

# --- NUEVO FLUJO PRINCIPAL ---
while True:
    opcion = menu_principal()
    if opcion == "jugar":
        # Elegir dificultad
        dificultad = pantalla_inicio()  # Reutiliza la función de elegir dificultad
        if dificultad == "facil":
            FILAS = 5
            COLUMNAS = 5
            barcos_configurados = [
                (3, 1),  # Submarino
                (2, 1),  # Destructor
            ]
        elif dificultad == "normal":
            FILAS = 10
            COLUMNAS = 10
            barcos_configurados = [
                (5, 1),  # Portaaviones
                (4, 1),  # Acorazado
                (3, 1),  # Crucero
                (3, 1),  # Submarino
                (2, 1),  # Destructor
            ]
        else:
            FILAS = 12
            COLUMNAS = 12
            barcos_configurados = [
                (5, 1),  # Portaaviones
                (4, 2),  # Acorazado x2
                (3, 2),  # Crucero/Submarino x2
                (2, 2),  # Destructor x2
            ]
        # Inicializar variables globales del juego
        tablero_ancho = COLUMNAS * TAM_CASILLA
        tablero_alto = FILAS * TAM_CASILLA
        tablero_offset_x = (ANCHO_VENTANA - tablero_ancho) // 2
        tablero_offset_y = (ALTO_VENTANA - tablero_alto) // 2
        tablero = crear_tablero()
        colocar_barcos_juego(tablero, barcos_configurados)
        nick = pedir_nombre_pygame()
        disparos = 0
        puntaje = 0
        # Centrar el botón Reiniciar debajo del tablero
        boton_reiniciar_ancho = 180
        boton_reiniciar_alto = 50
        boton_reiniciar_x = tablero_offset_x + (tablero_ancho - boton_reiniciar_ancho) // 2
        boton_reiniciar_y = tablero_offset_y + tablero_alto + 40  # 40px debajo del tablero
        boton_reiniciar = pygame.Rect(boton_reiniciar_x, boton_reiniciar_y, boton_reiniciar_ancho, boton_reiniciar_alto)
        # Botón Salir debajo del de Reiniciar
        boton_salir_ancho = 180
        boton_salir_alto = 50
        boton_salir_x = boton_reiniciar_x
        boton_salir_y = boton_reiniciar_y + boton_reiniciar_alto + 20  # 20px de separación
        boton_salir = pygame.Rect(boton_salir_x, boton_salir_y, boton_salir_ancho, boton_salir_alto)
        corriendo = True
        while corriendo:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if boton_reiniciar.collidepoint(x, y):
                        tablero = crear_tablero()
                        colocar_barcos_juego(tablero, barcos_configurados)
                        disparos = 0
                        puntaje = 0
                        continue
                    if boton_salir.collidepoint(x, y):
                        pygame.quit()
                        sys.exit()
                    if (tablero_offset_x <= x < tablero_offset_x + tablero_ancho and
                        tablero_offset_y <= y < tablero_offset_y + tablero_alto):
                        fila = (y - tablero_offset_y) // TAM_CASILLA
                        col = (x - tablero_offset_x) // TAM_CASILLA
                        if 0 <= fila < FILAS and 0 <= col < COLUMNAS:
                            if tablero[fila][col] == 1:
                                tablero[fila][col] = 2
                                disparos += 1
                                puntaje += 5
                                tamaño_nave = contar_nave(tablero, fila, col)
                                if 'sonido_disparo' in globals():
                                    sonido_disparo.play()
                                if nave_hundida(tablero, fila, col):
                                    puntaje += tamaño_nave * 10
                            elif tablero[fila][col] == 0:
                                tablero[fila][col] = 3
                                disparos += 1
                                puntaje -= 1
            ventana.fill((0, 0, 0))
            ventana.blit(mar_scaled, (offset_x_mar, offset_y_mar))
            dibujar_tablero(ventana)
            # Dibuja el botón Reiniciar centrado abajo del tablero
            pygame.draw.rect(ventana, GRIS, boton_reiniciar, border_radius=15)
            fuente = pygame.font.SysFont(FUENTE_GRIEGA, 36)
            texto_reiniciar = fuente.render("Reiniciar", True, NEGRO)
            texto_reiniciar_rect = texto_reiniciar.get_rect(center=boton_reiniciar.center)
            ventana.blit(texto_reiniciar, texto_reiniciar_rect)
            # Dibuja el botón Salir debajo del de Reiniciar
            pygame.draw.rect(ventana, (200, 60, 60), boton_salir, border_radius=15)
            texto_salir = fuente.render("Salir", True, BLANCO)
            texto_salir_rect = texto_salir.get_rect(center=boton_salir.center)
            ventana.blit(texto_salir, texto_salir_rect)
            info_x = tablero_offset_x + tablero_ancho + 30
            # Mostrar el mejor puntaje y nombre arriba del panel de puntaje
            try:
                with open("puntajes.txt", "r", encoding="utf-8") as f:
                    puntajes_archivo = [line.strip().split(',') for line in f if ',' in line]
                    if puntajes_archivo:
                        mejor = max(puntajes_archivo, key=lambda x: int(x[1]))
                        mejor_nombre, mejor_puntaje = mejor[0], int(mejor[1])
                    else:
                        mejor_nombre, mejor_puntaje = "-", 0
            except Exception:
                mejor_nombre, mejor_puntaje = "-", 0
            fuente = pygame.font.SysFont(FUENTE_GRIEGA, 36)
            texto_mejor = fuente.render(f"Mejor: {mejor_nombre} ({mejor_puntaje:04d})", True, (255,255,255))
            ventana.blit(texto_mejor, (info_x, tablero_offset_y))
            # Dibuja el puntaje y disparos al costado derecho del tablero
            fuente = pygame.font.SysFont(FUENTE_GRIEGA, 36)
            texto_disparos = fuente.render(f"Disparos: {disparos}", True, NEGRO)
            texto_puntaje = fuente.render(f"Puntaje: {puntaje:04d}", True, NEGRO)
            ventana.blit(texto_disparos, (info_x, tablero_offset_y + 40))
            ventana.blit(texto_puntaje, (info_x, tablero_offset_y + 100))
            if todos_los_barcos_hundidos(tablero):
                fuente = pygame.font.SysFont(None, 60)
                texto = fuente.render("¡Ganaste!", True, BLANCO)
                texto_rect = texto.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2))
                for _ in range(6):
                    ventana.blit(mar_scaled, (offset_x_mar, offset_y_mar))
                    dibujar_tablero(ventana, mostrar_barcos=True)
                    if _ % 2 == 0:
                        rect_fondo = pygame.Rect(
                            texto_rect.x - 40, texto_rect.y - 20,
                            texto_rect.width + 80, texto_rect.height + 40
                        )
                        pygame.draw.rect(ventana, (0, 0, 0), rect_fondo, border_radius=20)
                        ventana.blit(texto, texto_rect)
                    pygame.display.flip()
                    pygame.time.wait(300)
                boton_nuevo = pygame.Rect(ANCHO_VENTANA // 2 - 180, ALTO_VENTANA // 2 + 80, 360, 70)
                fuente_btn = pygame.font.SysFont(None, 48)
                activo = True
                while activo:
                    ventana.blit(mar_scaled, (offset_x_mar, offset_y_mar))
                    dibujar_tablero(ventana, mostrar_barcos=True)
                    pygame.draw.rect(ventana, (0, 0, 0), rect_fondo, border_radius=20)
                    ventana.blit(texto, texto_rect)
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
                                nick = pedir_nombre_pygame()
                                tablero = crear_tablero()
                                colocar_barcos_juego(tablero, barcos_configurados)
                                disparos = 0
                                puntaje = 0
                                corriendo = True
                                activo = False
            pygame.display.flip()
    elif opcion == "ver puntajes":
        mostrar_puntajes()
    elif opcion == "salir":
        pygame.quit()
        sys.exit()

    # Guardar puntaje solo si se jugó una partida
    if opcion == "jugar":
        with open("puntajes.txt", "a", encoding="utf-8") as f:
            f.write(f"{nick},{puntaje}\n")

pygame.quit()
sys.exit()