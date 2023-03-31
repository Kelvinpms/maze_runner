# Importa as bibliotecas necessárias
import numpy as np
from queue import Queue
import re
from colorama import Fore, Back, Style
# função para encontrar todos os caminhos mais curtos em um labirinto
def shortest_paths(labyrinth, start, end):
    # Obtém o número de linhas e colunas da matriz
    nrows, ncols = labyrinth.shape
    # Define uma matriz com as direções possíveis: norte, leste, sul e oeste
    directions = [[-1, 0], [0, 1], [1, 0], [0, -1]] # norte Leste Sul Oeste
    # Define uma matriz para armazenar quais células foram visitadas
    visited = np.zeros_like(labyrinth)
    # Define uma matriz para armazenar as distâncias de cada célula até o ponto de partida
    distance = np.zeros_like(labyrinth)
    distance.fill(np.inf)
    # Define a distância da célula de partida como 0
    distance[start[0], start[1]] = 0
    # Cria uma fila para armazenar as células a serem visitadas
    queue = Queue()
    # Adiciona a célula de partida à fila
    queue.put(start)
    # Enquanto a fila não estiver vazia
    while not queue.empty():
        # Remove a célula atual da fila
        current_row, current_col = queue.get()
        # Marca a célula atual como visitada
        visited[current_row, current_col] = True
        # Percorre todas as direções possíveis
        for direction in directions:
            row, col = current_row + direction[0], current_col + direction[1]
            # Se a célula estiver fora dos limites do labirinto ou for uma parede, continue
            if row < 0 or col < 0 or row >= nrows or col >= ncols or labyrinth[row, col] == -1:
                continue
            # Se a célula ainda não foi visitada
            if not visited[row, col]:
                # Atualiza a distância da célula em relação à célula de partida
                distance[row, col] = distance[current_row, current_col] + 1
                # Marca a célula como visitada
                visited[row, col] = True
                # Adiciona a célula à fila para visitar mais tarde
                queue.put([row, col])
    # Se a célula de destino não foi visitada, não há caminho
    if visited[end[0], end[1]] == False:
        print(Fore.RED +"Não existe caminho entre Thomas e a saída"+ Style.RESET_ALL)
    else:
        # Caso contrário, encontre todos os caminhos mais curtos
        paths = []
        path = []
        find_paths(labyrinth, start, end, distance, paths, path)
        print(Fore.GREEN +"Todos os caminhos mais curtos de Thomas até a saída são:"+ Style.RESET_ALL)
        for path in paths:
            # Substitui o número de cada célula pelo número da etapa da solução
            path_str = '-'.join(map(str, path))
            path_substituido = re.sub(r'\d', lambda m: str(int(m.group(0))+1), path_str)
            print(Fore.YELLOW +path_substituido+ Style.RESET_ALL)

  


# Define a função recursiva para encontrar todos os caminhos mais curtos
#Essa função find_paths é responsável por encontrar todos os caminhos mais curtos de current até end, dada a matriz labyrinth e a matriz de distâncias distance. Ela usa uma estratégia recursiva para explorar todas as possíveis rotas a partir de current, e armazena todos os caminhos encontrados em uma lista paths.
def find_paths(labyrinth, current, end, distance, paths, path):
    path.append(current)#Adiciona current ao final da lista path.

    if current == end: #Verifica se current é igual a end. Se for, adiciona uma cópia de path na lista paths.
        paths.append(path.copy()) 
    else: #Se current não é igual a end, continua explorando as rotas possíveis.
        for direction in [[-1, 0], [0, 1], [1, 0], [0, -1]]: #Itera sobre as quatro direções possíveis a partir de current: norte, leste, sul e oeste.
            row, col = current[0] + direction[0], current[1] + direction[1] # Calcula a posição na matriz correspondente à direção atual.
            if row < 0 or col < 0 or row >= labyrinth.shape[0] or col >= labyrinth.shape[1] or labyrinth[row, col] == -1: #Verifica se a posição calculada está fora dos limites da matriz, ou se a posição corresponde a uma parede (-1). Se estiver, passa para a próxima direção.
                continue
            if distance[row, col] == distance[current[0], current[1]] + 1: #Verifica se a posição atual está a uma distância de um passo de current. Se estiver, chama recursivamente a função find_paths com current atualizado para a nova posição.
                find_paths(labyrinth, [row, col], end, distance, paths, path)
    path.pop() #Remove o último elemento de path, para desfazer as alterações feitas durante a exploração dessa rota.

# lê a entrada do arquivo
with open('input.txt') as f:
    # leia as coordenadas de Thomas
    ti, tj = map(int, f.readline().replace('1', '0').replace('2', '1').replace('3', '2').replace('4', '3').replace('5', '4').replace('6', '5').replace('7', '6').replace('8', '7').replace('9', '8').replace('10', '9').split())
    # lê as coordenadas de saída
    ei, ej = map(int, f.readline().replace('1', '0').replace('2', '1').replace('3', '2').replace('4', '3').replace('5', '4').replace('6', '5').replace('7', '6').replace('8', '7').replace('9', '8').replace('10', '9').split())
    # leia as dimensões da matriz
    n, m = map(int, f.readline().split())
    # leia a matriz
    matrix = np.zeros((n, m), dtype=int)
    for i in range(n):
        row = list(map(int, f.readline().split()))
        matrix[i, :] = row

# encontre todos os caminhos mais curtos de Thomas até a saída
shortest_paths(matrix, [ti, tj], [ei, ej])
