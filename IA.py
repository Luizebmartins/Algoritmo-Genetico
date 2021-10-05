import math
import random
import time

# classe para manipular as cidades
class city:

    def __init__(self, nome, x, y):
        self.nome = nome
        self.x = x
        self.y = y

    def getNome(self):
        return self.nome

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def distancia(self, destino):
        return math.sqrt((self.x - destino.getX()) ** 2 + (self.y - destino.getY()) ** 2)


def criaIndividuo(cidades):
    individuo = random.sample(cidades, len(cidades))
    return individuo


def criaPopulacao(cidades, tam):
    populacao = []
    for i in range(0, tam):
        populacao.append(criaIndividuo(cidades))

    return populacao


def Aptidao(individuo):
    distancia = 0

    # calculo da da distancia entre as cidades atuais [i] até
    # a próxima [i+1]
    for i in range(0, len(individuo) - 1):
        cidAtual = individuo[i]
        cidAte = individuo[i+1]
        distancia += cidAtual.distancia(cidAte)

    # distancia para retornar até a primeira cidade
    cidAtual = individuo[len(individuo) - 1]
    cidAte = individuo[0]
    distancia += cidAtual.distancia(cidAte)

    return distancia


def cruzamento(mae, pai):
    aux_1 = []
    aux_2 = []

    size = len(mae)

    if size % 2 == 0:
        end = int(size / 2)
    
    else:
        end = int((size - 1) / 2)
    # primeira parte do filho será a primeira metade da mãe
    for i in range(0, end):
        aux_1.append(mae[i])

    # segunda parte do filho será o restante do pai
    # A ordem é seguida, e pega as cidades que ainda não
    # existem no aux 1
    aux_2 = [item for item in pai if item not in aux_1]

    # retorna a junção das duas partes
    return aux_1 + aux_2


def mutacao(individuo, prob):
    # caso rate(entre 0.0 e 1.0) seja menor que prob
    # troca duas posições aleatórias
    rate = random.random()
    if rate < prob:
        size = len(individuo)
        troca1 = random.randint(0, size - 1)
        troca2 = random.randint(0, size - 1)
        individuo[troca1], individuo[troca2] = individuo[troca2], individuo[troca1]

    return individuo


def SelecaoTorneio(populacao):
    selecionados = []
    auxPreench = 0

    IndiceMaior = len(populacao) - 1

    # Sorteia dois individuos aleatórios da população para fazer uma
    # disputa. O que tiver a menor aptidão, já que trata-se da distancia
    # total, é selecionado
    while auxPreench < 6:
        lutador1 = random.randint(0, IndiceMaior)
        lutador2 = random.randint(0, IndiceMaior)

        Al1 = Aptidao(populacao[lutador1])
        Al2 = Aptidao(populacao[lutador2])

        if Al1 < Al2 and populacao[lutador1] not in selecionados:
            selecionados.append(populacao[lutador1])
            auxPreench += 1

        elif Al2 < Al1 and populacao[lutador2] not in selecionados:
            selecionados.append(populacao[lutador2])
            auxPreench += 1

        else:
            selecionados.append(populacao[lutador1])
            auxPreench += 1

    return selecionados


def melhorIndividuo(pop):
    # percorre a populaçao procurando o individuo
    # com a menor aptidao
    aux = pop[0]

    for i in range(0, len(pop)):
        if Aptidao(aux) > Aptidao(pop[i]):
            aux = pop[i]

    return aux


def criaGeracao(pop, probMutacao):
    # Seleciona os pais pretendentes através do torneio
    # Adicionao o melhor da população à nova geração
    # faz o cruzamento e aplica a mutacao já adicionado na geração

    NovaGeracao = []
    selecionados = SelecaoTorneio(pop)
    NovaGeracao.append(melhorIndividuo(pop))

    size = len(selecionados) - 1

    for i in range(1, len(pop)):
        mae = random.randint(0, size)
        pai = random.randint(0, size)

        filho = cruzamento(selecionados[mae], selecionados[pai])
        NovaGeracao.append(mutacao(filho, probMutacao))

    return NovaGeracao

t0 = time.time()

# cidades predefinidas
cidades = [city('A', 1560, 1980),
           city('B', 660, 920),
           city('C', 1100, 832),
           city('D', 300, 380),
           city('E', 700, 420),
           city('F', 2002, 1430),
           city('G', 200, 250),
           city('H', 520, 870),
           city('I', 878, 956 ),
           city('J', 2134, 3450),
           city('K', 2109, 2998),
           city('L', 3987, 2781),
           city('M', 221, 599),
           city('N', 459, 854),
           city('O', 1547, 1874),
           city('P', 1999, 2020)]
            
# população inicial
populacao = criaPopulacao(cidades, 100000)

# Passagem de 10 gerações
for i in range(0, 10):
    populacao = criaGeracao(populacao, 0.1)

# escolha do melhor indivíduo da ultima geração
melhor = melhorIndividuo(populacao)
print('\n\n')
print('Indivíduo com o melhor resultado:', end=" ")
for i in melhor:
    print(f'{i.getNome()}', end="")

print()
print(f'Distância percorrida: {Aptidao(melhor)}')

tempoExec = time.time() - t0

print(f'Tempo de execução: {tempoExec}')
print('\n\n')

