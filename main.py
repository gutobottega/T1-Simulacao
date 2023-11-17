# algoritmo simulação de fila simples
# usa input:
# - o intervalo de tempo de chegada dos clientes na fila;
# - o intervalo de tempo de saida de um cliente na fila;
# - número de servidores;
# - capacidade da fila.

# print("Digite o intervalo de tempo de chegada dos clientes na fila: ")
# tempoChegadaA = int(input('De:'))
# tempoChegadaB = int(input('Até:'))
# print("Intervalo de tempo de chegada dos clientes na fila: ",
#       tempoChegadaA, "até", tempoChegadaB)
# print("Digite o intervalo de tempo de saida de um cliente na fila: ")
# tempoSaidaA = int(input('De:'))
# tempoSaidaB = int(input('Até:'))
# print("Intervalo de tempo de saida de um cliente na fila: ",
#       tempoSaidaA, "até", tempoSaidaB)
# numeroServidores = int(input("Digite o número de servidores: "))
# capacidadeFila = int(input("Digite a capacidade da fila: "))

tempoInicial = 2.5

# Fila 1
tempoChegadaA1 = 1
tempoChegadaB1 = 3
tempoSaidaA1 = 2
tempoSaidaB1 = 4
numeroServidores1 = 2
capacidadeFila1 = 3
# Fila 2
tempoSaidaA2 = 1
tempoSaidaB2 = 3
numeroServidores2 = 1
capacidadeFila2 = 5

# Números randomicos que serão usados na simulação - 100.000
numerosRandomicos = []

# Simulação
simulacao = {
    'evento': '-',
    'fila1': 0,
    'fila2': 0,
    'tempo': 0,
    'estadoFila1': [0] * (capacidadeFila1 + 1),
    'estadoFila2': [0] * (capacidadeFila2 + 1),
}

# Escalonador
escalonador = [
    {'evento': 'ch1', 'tempo': tempoInicial}
]

# Perda de clientes
perdaFila1 = 0
perdaFila2 = 0

def geraNumerosAle(x):
    a = 1826663
    c = 858765198
    M = 2**32
    for i in range(100000):
        x = (a*x + c) % M
        # with open("pseudoaleatorio1.txt", "a") as file:
        #     file.write(str(x/M) + "\n")
        numerosRandomicos.append(x/M)

def geraDistribuicaoProbabilidade(estado, tempo):
    return [(x/tempo) * 100 for x in estado]

# Sorteio


def sorteio(A, B):
    return A + (B-A) * numerosRandomicos.pop(0)


def addEscalonador(evento):
    if evento == 'ch1':
        tempoChegada = sorteio(
            tempoChegadaA1, tempoChegadaB1) + simulacao['tempo']
        escalonador.append({'evento': 'ch1', 'tempo': tempoChegada})
    # if de passagem da fila 1 para 2, utiliza os tempos de saida da fila 1
    elif evento == 'p12':
        tempoSaida = sorteio(tempoSaidaA1, tempoSaidaB1) + simulacao['tempo']
        escalonador.append({'evento': 'p12', 'tempo': tempoSaida})
    else:
        tempoSaida = sorteio(tempoSaidaA2, tempoSaidaB2) + simulacao['tempo']
        escalonador.append({'evento': 'sa2', 'tempo': tempoSaida})


def chegadaFila(evento, tempo):
    global tempoTotal
    global fila1
    global fila2
    global perdaFila1
    global perdaFila2
    global escalonador
    simulacao['evento'] = evento
    diferencaTempo = tempo - simulacao['tempo']
    simulacao['tempo'] = tempo
    # soma diferenca de tempo no estado atual da fila
    # simulacao['estado'][simulacao['fila']] += diferencaTempo
    
    simulacao['estadoFila1'][simulacao['fila1']] += diferencaTempo
    simulacao['estadoFila2'][simulacao['fila2']] += diferencaTempo
    
    # Checa se tem espaço fila 1
    if (simulacao['fila1'] < capacidadeFila1):
        simulacao['fila1'] += 1
        # checa se tem servidor disponivel na fila 1, se tiver agenda uma passagem pra fila 2 'P12'
        if (simulacao['fila1'] <= numeroServidores1):
            # addEscalonador('saida')
            addEscalonador('p12')
    else:
        perdaFila1 += 1
    if len(numerosRandomicos) == 0:
        return
    addEscalonador('ch1')


def saidaFila(evento, tempo):
    global tempoTotal
    global fila
    global perda
    global escalonador
    simulacao['evento'] = evento
    diferencaTempo = tempo - simulacao['tempo']
    simulacao['tempo'] = tempo
    # soma diferenca de tempo no estado atual da fila
    # simulacao['estado'][simulacao['fila']] += diferencaTempo
    simulacao['estadoFila1'][simulacao['fila1']] += diferencaTempo
    simulacao['estadoFila2'][simulacao['fila2']] += diferencaTempo
    
    simulacao['fila2'] -= 1
    if (simulacao['fila2'] >= numeroServidores2):
        addEscalonador('sa2')
        
        
def p12(evento, tempo):
    global tempoTotal
    global fila1
    global fila2
    global perdaFila1
    global perdaFila2
    global escalonador
    simulacao['evento'] = evento
    diferencaTempo = tempo - simulacao['tempo']
    simulacao['tempo'] = tempo
    # soma diferenca de tempo no estado atual da fila
    # simulacao['estado'][simulacao['fila']] += diferencaTempo
    simulacao['estadoFila1'][simulacao['fila1']] += diferencaTempo
    simulacao['estadoFila2'][simulacao['fila2']] += diferencaTempo
    
    simulacao['fila1'] -= 1
    if (simulacao['fila1'] >= numeroServidores1):
        addEscalonador('p12')
    if(simulacao['fila2'] < capacidadeFila2):
        simulacao['fila2'] += 1
        if(simulacao['fila2'] <= numeroServidores2):
            addEscalonador('sa2')
    else:
        perdaFila2 +=1


def run(x):
    global perdaFila1
    global perdaFila2
    perdaFila1 = 0
    perdaFila2 = 0
    # Simulação
    global simulacao
    simulacao = {
        'evento': '-',
        'fila1': 0,
        'fila2': 0,
        'tempo': 0,
        'estadoFila1': [0] * (capacidadeFila1 + 1),
        'estadoFila2': [0] * (capacidadeFila2 + 1),
    }
    global escalonador
    # Escalonador
    escalonador = [
        {'evento': 'ch1', 'tempo': tempoInicial}
    ]
    # arquivo = open(arq, 'r')
    # for linha in arquivo:
    #     numerosRandomicos.append(float(linha))
    # arquivo.close()
    geraNumerosAle(x)

    while (len(escalonador) > 0 and len(numerosRandomicos) > 0):
        escalonador.sort(key=lambda x: x['tempo'])
        # print(escalonador)
        evento = escalonador.pop(0)
        if (evento['evento'] == 'ch1'):
            chegadaFila(evento['evento'], evento['tempo'])
        elif evento['evento'] == 'sa2':
            saidaFila(evento['evento'], evento['tempo'])
        else:
            p12(evento['evento'], evento['tempo'])

    print("Tempo de simulação: ", evento['tempo'])
    print("Perda de clientes fila1: ", perdaFila1)
    print("Perda de clientes fila2: ", perdaFila2)
    print("Distribuição de probabilidade dos estados da fila: ",
          geraDistribuicaoProbabilidade(simulacao['estadoFila1'], simulacao['tempo']))
    print("Distribuição de probabilidade dos estados da fila 2: ",
          geraDistribuicaoProbabilidade(simulacao['estadoFila2'], simulacao['tempo']))
    return simulacao, perdaFila1, perdaFila2

tempoTotal = 0
estadoFinal1 = [0] * (capacidadeFila1 + 1)
estadoFinal2 = [0] * (capacidadeFila2 + 1)
perdaFinalFila1 = 0
perdaFinalFila2 = 0

for i in range(5):
    print("Simulação ", i+1)
    sim, perd1, perd2 = run(i+1)
    tempoTotal += sim['tempo']
    estadoFinal1 = [x + y for x, y in zip(estadoFinal1, sim['estadoFila1'])]
    estadoFinal2 = [x + y for x, y in zip(estadoFinal2, sim['estadoFila2'])]
    perdaFinalFila1 += perd1
    perdaFinalFila2 += perd2

print("Tempo médio de simulação: ", tempoTotal/5)
print("Perda média de clientes na fila 1: ", perdaFinalFila1/5)
print("Perda média de clientes na fila 2: ", perdaFinalFila2/5)
print("Distribuição de probabilidade dos estados da fila 1: ",
      geraDistribuicaoProbabilidade(estadoFinal1, tempoTotal))
print("Distribuição de probabilidade dos estados da fila 2: ",
      geraDistribuicaoProbabilidade(estadoFinal2, tempoTotal))
    
