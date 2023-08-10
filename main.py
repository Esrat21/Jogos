import random

# Define o tamanho do tabuleiro e os tamanhos dos navios
tamanho_tabuleiro = 10
tamanhos_navios = [5, 4, 3, 3, 2]

# Inicializa os tabuleiros do jogador e da IA, o tabuleiro auxiliar e a grade de probabilidades
tabuleiro_jogador = [["~" for _ in range(tamanho_tabuleiro)] for _ in range(tamanho_tabuleiro)]
tabuleiro_ia = [["~" for _ in range(tamanho_tabuleiro)] for _ in range(tamanho_tabuleiro)]
tabuleiro_auxiliar = [["~" for _ in range(tamanho_tabuleiro)] for _ in range(tamanho_tabuleiro)]
grade_probabilidades = [[1.0 for _ in range(tamanho_tabuleiro)] for _ in range(tamanho_tabuleiro)]


# Coloca os navios aleatoriamente no tabuleiro
def colocar_navios(tabuleiro):
    for tamanho in tamanhos_navios:
        while True:
            direcao = random.choice(['horizontal', 'vertical'])
            if direcao == 'horizontal':
                x = random.randint(0, tamanho_tabuleiro - tamanho)
                y = random.randint(0, tamanho_tabuleiro - 1)
            else:
                x = random.randint(0, tamanho_tabuleiro - 1)
                y = random.randint(0, tamanho_tabuleiro - tamanho)

            valido = True
            for i in range(tamanho):
                if direcao == 'horizontal':
                    if tabuleiro[y][x + i] != "~":
                        valido = False
                        break
                else:
                    if tabuleiro[y + i][x] != "~":
                        valido = False
                        break

            if valido:
                for i in range(tamanho):
                    if direcao == 'horizontal':
                        tabuleiro[y][x + i] = str(tamanho)
                    else:
                        tabuleiro[y + i][x] = str(tamanho)
                break


# Atualiza a grade de probabilidades após cada acerto
def atualizar_grade_probabilidades(tabuleiro, grade, x, y):
    grade[y][x] = 0

    for i in range(-1, 2):
        for j in range(-1, 2):
            novo_x = x + i
            novo_y = y + j
            if 0 <= novo_x < tamanho_tabuleiro and 0 <= novo_y < tamanho_tabuleiro and grade[novo_y][novo_x] != 0:
                grade[novo_y][novo_x] += 0.1


# Estratégia combinada da IA para atirar
def estrategia_combinada_ia(tabuleiro, grade):
    max_probabilidade = 0
    coordenadas_max = []

    for y in range(tamanho_tabuleiro):
        for x in range(tamanho_tabuleiro):
            if tabuleiro[y][x] == "~":
                if grade[y][x] > max_probabilidade:
                    max_probabilidade = grade[y][x]
                    coordenadas_max = [(x, y)]
                elif grade[y][x] == max_probabilidade:
                    coordenadas_max.append((x, y))

    return random.choice(coordenadas_max)


# Mostra os tabuleiros do jogador e o tabuleiro auxiliar lado a lado
def mostrar_tabuleiros(tabuleiro_jogador, tabuleiro_auxiliar):
    for linha_jogador, linha_auxiliar in zip(tabuleiro_jogador, tabuleiro_auxiliar):
        print(" ".join(linha_jogador) + "   " + " ".join(linha_auxiliar))


# Loop principal do jogo
def jogo():
    print("Bem-vindo ao Batalha Naval!")
    colocar_navios(tabuleiro_jogador)
    colocar_navios(tabuleiro_ia)
    while True:
        print("\nSeu tabuleiro:")
        print("" + " ".join(str(i) for i in range(tamanho_tabuleiro)))
        mostrar_tabuleiros(tabuleiro_jogador, tabuleiro_auxiliar)

        while True:
            try:
                x = int(input("Informe a coordenada x do disparo: "))
                y = int(input("Informe a coordenada y do disparo: "))
                if 0 <= x < tamanho_tabuleiro and 0 <= y < tamanho_tabuleiro and tabuleiro_auxiliar[y][x] == "~":
                    break
                elif tabuleiro_auxiliar[y][x] != "~":
                    print("Você já atacou esse ponto. Tente novamente.")
                else:
                    print("As coordenadas estão fora dos limites. Tente novamente.")
            except ValueError:
                print("Entrada inválida. Por favor, informe coordenadas válidas.")

        if tabuleiro_ia[y][x] != "~":
            #print("Acertou nas coordenadas da IA:", y, x)
            tabuleiro_auxiliar[y][x] = "X"
            tabuleiro_ia[y][x] = "X"
            atualizar_grade_probabilidades(tabuleiro_ia, grade_probabilidades, x, y)
        else:
            print("Errou!")
            tabuleiro_auxiliar[y][x] = "O"

        x_ia, y_ia = estrategia_combinada_ia(tabuleiro_jogador, grade_probabilidades)
        print("A IA Atingiu as coordenadas:", y_ia, x_ia)  # Imprime a suposição da IA em cada jogada
        if tabuleiro_jogador[y_ia][x_ia] != "~":
            print("A IA acertou no seu navio!")
            tabuleiro_jogador[y_ia][x_ia] = "X"
            atualizar_grade_probabilidades(tabuleiro_jogador, grade_probabilidades, x_ia, y_ia)
        else:
            print("A IA errou!")
            tabuleiro_jogador[y_ia][x_ia] = "O"

        navios_jogador_restantes = any(
            str(tamanho_navio) in linha for linha in tabuleiro_jogador for tamanho_navio in tamanhos_navios)
        navios_ia_restantes = any(
            str(tamanho_navio) in linha for linha in tabuleiro_ia for tamanho_navio in tamanhos_navios)

        if not navios_jogador_restantes:
            print("Você perdeu! A IA venceu.")
            break
        elif not navios_ia_restantes:
            print("Parabéns! Você afundou todos os navios da IA.")
            break


# Inicia o jogo
jogo()
