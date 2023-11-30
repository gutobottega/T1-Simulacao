import json
import random

# Lista para armazenar números aleatórios
numerosRandomicos = []

# Definição da classe Fila, que representa uma fila no sistema

class Fila:
    def __init__(self, id, nome, tempoAtendimento, tempoChegada, numeroServidores, capacidadeFila, probabilidadeRoteamento):
        # Atributos da fila
        self.id = id
        self.nome = nome
        self.tempoAtendimento = tempoAtendimento
        self.tempoChegada = tempoChegada
        self.numeroServidores = numeroServidores
        self.probabilidadeRoteamento = probabilidadeRoteamento
        if capacidadeFila == -1:
            self.capacidadeFila = 10
            self.estadoFila = [0] * 11
        else:
            self.capacidadeFila = capacidadeFila
            self.estadoFila = [0] * (capacidadeFila + 1)
        self.tamanhoAtual = 0
        self.perda = 0

    # Método para simular a chegada de um elemento à fila
    def chegadaFila(self, tempo):
        global simulacao
        global filas

        diferencaTempo = tempo - simulacao['tempo']
        simulacao['tempo'] = tempo

        for fila in filas:
            fila.estadoFila[fila.tamanhoAtual] += diferencaTempo
            
        # Se ainda houver capacidade na fila, adiciona um novo elemento à fila
        if (self.capacidadeFila > self.tamanhoAtual or self.capacidadeFila == -1):
            self.tamanhoAtual += 1
            # Se ainda houver servidores disponíveis, adiciona o evento de passagemFila ao escalonador
            if (self.tamanhoAtual <= self.numeroServidores):
                 # Escolhe aleatoriamente a rota do elemento na fila
                rota = random.choices(list(self.probabilidadeRoteamento.keys()),
                                    weights=list(self.probabilidadeRoteamento.values()))[0]

                # Se a rota for "saida", adiciona o evento de saída ao escalonador
                if rota == "saida":
                    addEscalonador({
                        'evento': 'saida',
                        'fila': self.id,
                    })
                else:
                    # Caso contrário, encaminha o elemento para a fila de destino
                    fila_destino = next(fila for fila in filas if fila.nome == rota)
                addEscalonador({
                    'evento': 'passagemFila',
                    'fila': self.id,
                    'destino': fila_destino.id,
                })
        else:
            self.perda += 1
            
        if len(numerosRandomicos) == 0:
            return
        addEscalonador({
            'evento': 'chegada',
            'fila': self.id,
        })

    # Método para simular a saída de um elemento da fila
    def saidaFila(self, tempo):
        global simulacao
        global filas

        diferencaTempo = tempo - simulacao['tempo']
        simulacao['tempo'] = tempo

        for fila in filas:
            fila.estadoFila[fila.tamanhoAtual] += diferencaTempo

        self.tamanhoAtual -= 1
        # Se ainda houver elementos para serem atendidos na fila, adiciona o evento um evento ao escalonador
        if (self.tamanhoAtual >= self.numeroServidores):
            rota = random.choices(list(self.probabilidadeRoteamento.keys()),
                                  weights=list(self.probabilidadeRoteamento.values()))[0]
            # Se a rota for "saida", adiciona o evento de saída ao escalonador
            if rota == "saida":
                addEscalonador({
                    'evento': 'saida',
                    'fila': self.id,
                })
            else:
                # Caso contrário, encaminha o elemento para a fila de destino
                fila_destino = next(
                    fila for fila in filas if fila.nome == rota)
                addEscalonador({
                    'evento': 'passagemFila',
                    'fila': self.id,
                    'destino': fila_destino.id,
                })


    # Método para simular o passasgem de um elemento na fila
    def passagemFila(self, tempo, destino):
        global simulacao
        global filas

        diferencaTempo = tempo - simulacao['tempo']
        simulacao['tempo'] = tempo

        for fila in filas:
            fila.estadoFila[fila.tamanhoAtual] += diferencaTempo

        # Reduz o tamanho da fila após o processamento
        self.tamanhoAtual -= 1
        if (self.tamanhoAtual >= self.numeroServidores):
            rota = random.choices(list(self.probabilidadeRoteamento.keys()),
                                  weights=list(self.probabilidadeRoteamento.values()))[0]
            if rota == "saida":
                addEscalonador({
                    'evento': 'saida',
                    'fila': self.id,
                })
            else:
                # Caso contrário, encaminha o elemento para a fila de destino
                fila_destino = next(
                    fila for fila in filas if fila.nome == rota)
                addEscalonador({
                    'evento': 'passagemFila',
                    'fila': self.id,
                    'destino': fila_destino.id,
                })

        # Se ainda houver capacidade na fila, adiciona um novo elemento à fila
        if (filas[destino].tamanhoAtual < filas[destino].capacidadeFila or self.capacidadeFila == -1):
            filas[destino].tamanhoAtual += 1
            # Se ainda houver servidores disponíveis, adiciona o evento de passagemFila ao escalonador
            if filas[destino].tamanhoAtual <= filas[destino].numeroServidores:
                # Escolhe aleatoriamente a rota do novo elemento na fila
                rota = random.choices(list(filas[destino].probabilidadeRoteamento.keys()),
                                      weights=list(filas[destino].probabilidadeRoteamento.values()))[0]

                if rota == "saida":
                    addEscalonador({
                        'evento': 'saida',
                        'fila': filas[destino].id,
                    })
                else:
                    # Caso contrário, encaminha o elemento para a fila de destino
                    fila_destino = next(
                        fila for fila in filas if fila.nome == rota)
                    addEscalonador({
                        'evento': 'passagemFila',
                        'fila': filas[destino].id,
                        'destino': fila_destino.id,
                    })
        else:
            filas[destino].perda += 1


# Função para carregar parâmetros de configuração do arquivo JSON
def carregaParametros():
    with open('config.json', 'r') as file:
        parametros = json.load(file)
    return parametros


def sorteio(A, B):
    A, B = float(A), float(B)
    if numerosRandomicos:
        return A + (B - A) * numerosRandomicos.pop(0)

# Função para adicionar eventos ao escalonador


def addEscalonador(evento):
    global escalonador
    if evento['evento'] == 'chegada':
        # Gera um tempo de chegada aleatório e adiciona ao escalonador
        tempoChegada = sorteio(
            filas[evento['fila']].tempoChegada.split('/')[0],
            filas[evento['fila']].tempoChegada.split('/')[1]) + simulacao['tempo']
        escalonador.append(
            {'evento': 'chegada', 'tempo': tempoChegada, 'fila': evento['fila']})
    elif evento['evento'] == 'passagemFila':
        # Gera um tempo de processamento aleatório e adiciona ao escalonador
        tempoSaida = sorteio(
            filas[evento['fila']].tempoAtendimento.split('/')[0],
            filas[evento['fila']].tempoAtendimento.split('/')[1]) + simulacao['tempo']
        escalonador.append({'evento': 'passagemFila', 'tempo': tempoSaida,
                           'fila': evento['fila'], 'destino': evento['destino']})
    elif evento['evento'] == 'saida':
        # Gera um tempo de saída aleatório e adiciona ao escalonador
        tempoSaida = sorteio(
            filas[evento['fila']].tempoAtendimento.split('/')[0],
            filas[evento['fila']].tempoAtendimento.split('/')[1]) + simulacao['tempo']
        escalonador.append(
            {'evento': 'saida', 'tempo': tempoSaida, 'fila': evento['fila']})


# Função para gerar números aleatórios usando um gerador linear congruente


def geraNumerosAle(x):
    a = 1826663
    c = 858765198
    M = 2**32
    for i in range(100000):
        x = (a*x + c) % M
        numerosRandomicos.append(x/M)

# Função para gerar a distribuição de probabilidade com base no estado da fila


def geraDistribuicaoProbabilidade(estado, tempo):
    return [(x / tempo) * 100 for x in estado]


# Função principal para executar a simulação
def run(x):
    # Inicializa as variáveis da simulação
    global simulacao
    global filas
    global escalonador

    simulacao = {
        'evento': '-',
        'tempo': 0,
    }

    escalonador = [{'evento': 'chegada',
                    'tempo': float(parametros['Tempo Inicial']), 'fila': 0}]
    geraNumerosAle(x)

    # Loop principal da simulação
    while escalonador and numerosRandomicos:
        escalonador.sort(key=lambda x: x['tempo'])
        evento = escalonador.pop(0)
        # Executa o evento com base no tipo
        # print(escalonador)
        if evento['evento'] == 'chegada':
            filas[evento['fila']].chegadaFila(evento['tempo'])
        elif evento['evento'] == 'passagemFila':
            filas[evento['fila']].passagemFila(
                evento['tempo'], evento['destino'])
        elif evento['evento'] == 'saida':
            filas[evento['fila']].saidaFila(evento['tempo'])


# Carrega os parâmetros do arquivo JSON
parametros = carregaParametros()
filas_parametros = parametros["Filas"]

# Inicializa as filas com base nos parâmetros
filas = [Fila(fila["Id"],
              fila["Nome"],
              fila["Tempo de Atendimento"],
              fila["Tempo de Chegada"],
              fila["Numero de Servidores"],
              fila["Capacidade da Fila"],
              fila["Probabilidade Roteamento"])
         for fila in filas_parametros]

run(parametros['Semente'])

print("Tempo de simulação: ", simulacao['tempo'])
# Exibe os resultados da simulação
for i, fila in enumerate(filas):
    print(f"Perda de clientes da fila {i+1}: ", fila.perda)
    print(f"Distribuição de probabilidade dos estados da fila {i+1}: ",
          geraDistribuicaoProbabilidade(fila.estadoFila, simulacao['tempo']))
