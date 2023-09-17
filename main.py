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

tempoInicial= 2
tempoChegadaA = 1
tempoChegadaB = 2
tempoSaidaA = 3
tempoSaidaB = 6
numeroServidores = 1
capacidadeFila = 3

# Números randomicos que serão usados na simulação - 100.000
numerosRandomicos = []

# Simulação
simulacao = {
    'evento': '-',
    'fila': 0,
    'tempo': 0,
    'estado': [0] * (capacidadeFila + 1),
}

# Escalonador
escalonador = [
    {'evento': 'chegada', 'tempo': tempoInicial}
]

# Perda de clientes
perda = 0


def geraDistribuicaoProbabilidade(estado, tempo):
    return [(x/tempo) * 100 for x in estado]

# Sorteio


def sorteio(A, B):
    return A + (B-A) * numerosRandomicos.pop(0)


def addEscalonador(evento):
    if evento == 'chegada':
        tempoChegada = sorteio(
            tempoChegadaA, tempoChegadaB) + simulacao['tempo']
        escalonador.append({'evento': 'chegada', 'tempo': tempoChegada})
    else:
        tempoSaida = sorteio(tempoSaidaA, tempoSaidaB) + simulacao['tempo']
        escalonador.append({'evento': 'saida', 'tempo': tempoSaida})


def chegadaFila(evento, tempo):
    global tempoTotal
    global fila
    global perda
    global escalonador
    simulacao['evento'] = evento
    diferencaTempo = tempo - simulacao['tempo']
    simulacao['tempo'] = tempo
    # soma diferenca de tempo no estado atual da fila
    simulacao['estado'][simulacao['fila']] += diferencaTempo
    if (simulacao['fila'] < capacidadeFila):
        simulacao['fila'] += 1
        if (simulacao['fila'] <= numeroServidores):
            addEscalonador('saida')
    else:
        perda += 1
    if len(numerosRandomicos) == 0:
        return
    addEscalonador('chegada')


def saidaFila(evento, tempo):
    global tempoTotal
    global fila
    global perda
    global escalonador
    simulacao['evento'] = evento
    diferencaTempo = tempo - simulacao['tempo']
    simulacao['tempo'] = tempo
    # soma diferenca de tempo no estado atual da fila
    simulacao['estado'][simulacao['fila']] += diferencaTempo
    simulacao['fila'] -= 1
    if (simulacao['fila'] >= numeroServidores):
        addEscalonador('saida')


arquivo = open('ale.txt', 'r')
for linha in arquivo:
    numerosRandomicos.append(float(linha))
arquivo.close()

while (len(escalonador) > 0 and len(numerosRandomicos) > 0):
    escalonador.sort(key=lambda x: x['tempo'])
    print(escalonador)
    evento = escalonador.pop(0)
    if (evento['evento'] == 'chegada'):
        chegadaFila(evento['evento'], evento['tempo'])
    else:
        saidaFila(evento['evento'], evento['tempo'])

print("Tempo de simulação: ", simulacao['tempo'])
print("Perda de clientes: ", perda)
print("Distribuição de probabilidade dos estados da fila: ",
      geraDistribuicaoProbabilidade(simulacao['estado'], simulacao['tempo']))
