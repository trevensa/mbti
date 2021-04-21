import os, getpass, time, json, requests, base64
from datetime import date, datetime

#Constante de tempo
k = 0.03

#---------------------------------------------------------------------------------------------
#Escreve a mensagem (parâmetro) letra por letra estilo pokemon

def escrita_letra(mensagem, timer=0.03, final='\n'):

    for letra in (mensagem+final):

        print(letra, end='', flush=True)
        time.sleep(timer)

#---------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------
#Cria uma função que retorna o nome da pessoa com as letras iniciais maiúsculas

def frescura(nome_minusculo):

    nomes = nome_minusculo.split()

    for qtd in range(len(nomes)):

        nomes[qtd] = nomes[qtd].capitalize()

    return ' '.join(nomes)

#---------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------
#Função que passa as informações iniciais do teste e explica seu funcionamento

def comecou():

    escrita_letra("Bem vindo ao teste de MBTI!")
    time.sleep(k)
    escrita_letra("Para cada uma das perguntas abaixo responda um número de -2 a 2 com base na frequência em que você realiza o que está descrito.")
    time.sleep(k)
    escrita_letra("Legenda:")
    time.sleep(k)
    escrita_letra("Muito raramente = -2")
    escrita_letra("Ocasionalmente = -1")
    escrita_letra("Neutro = 0")
    escrita_letra("Comum = 1")
    escrita_letra("Bastante Frequentemente = 2")
    time.sleep(k)
    escrita_letra("Tente ser honesto nas respostas mesmo que elas te desagradem ou te envergonhem de alguma forma.")
    time.sleep(k)
    emoji = chr(2)
    escrita_letra(f"Bom teste! {emoji}")
    time.sleep(k)
    print()

#---------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------
#Cria uma função que se despede do usuário e informa onde os resultados estarão disponíveis

def acabou():

    fim = 5

    print()
    escrita_letra('Obrigado por realizar o teste!')
    time.sleep(k)
    escrita_letra('Uma pasta chamada "Resultados Teste MBTI" foi criada na sua área de trabalho.')
    time.sleep(k)
    escrita_letra('Dentro dela, haverá um arquivo com os seus resultados nesse teste.')
    time.sleep(k)
    print()
    escrita_letra(f'Essa janela se fechará em: {fim}...',0.05,'\r')
    time.sleep(1)

    while fim > 1:

        fim -= 1
        print(f'Essa janela se fechará em: {fim}...', end='\r')
        time.sleep(1)

#---------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------
#Cria uma função responsável por escrever um arquivo com informações básicas acerca das personalidades

def introducao(way,nome_pasta,tipos):

    readme = open(f'{way}\{nome_pasta}\INTRODUCAO.txt','w')

    readme.write('Olá! Este arquivo contém uma base acerca do conteúdo de MBTI\n\n')
    readme.write('Esta teoria conta com 16 tipos de personalidade, onde cada uma delas possui 4 funções cognitivas:\n\n')
    readme.write('  - Função Dominante: esta função é a mais presente em sua personalidade e portanto a mais utilizada por você \n')
    readme.write('  - Função Auxiliar: esta função, como o próprio nome diz, tem como objetivo "auxiliar" a dominante, equilibrando as decisões tomadas por ela \n')
    readme.write('  - Função Terciaria: esta função possui um grau de desenvolvimento mais baixo e portanto pode apresentar um comportamento mais imaturo\n')
    readme.write('  - Função Inferior: por fim, esta função é a menos desenvolvida dentre as 4 e é uma função que você encontra dificuldade de colocar em ação\n\n')
    readme.write('Existem 8 possibilidades de função cognitiva, sendo elas: \n\n')
    readme.write('Si: Sensação Introvertida\n')
    readme.write('Se: Sensação Extrovertida\n')
    readme.write('Ni: Intuição Introvertida\n')
    readme.write('Ne: Intuição Extrovertida\n')
    readme.write('Fi: Sentimento Introvertido\n')
    readme.write('Fe: Sentimento Extrovertido\n')
    readme.write('Ti: Pensamento Introvertido\n')
    readme.write('Te: Pensamento Extrovertido\n\n')
    readme.write('Cada personalidade possui uma combinação diferente de 4 dessas funções. Veja:\n\n')

    for t in tipos:

        dom = tipos[t]['Dominante']
        aux = tipos[t]['Auxiliar']
        ter = tipos[t]['Terciaria']
        inf = tipos[t]['Inferior']

        readme.write(f' - {t}: {dom} {aux} {ter} {inf}\n')

    readme.write('\nOBS.: A ordem das funções da esquerda pra direita é: \n')
    readme.write('  Dominante | Auxiliar | Terciária | Inferior')

    readme.close()

#---------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------
#Cria uma funcao responsavel por traduzir o que significa em palavras cada uma das possibilidades de resposta
#Muito Raramente = -2
#Ocasionalmente = -1
#Neutro = 0
#Comum = 1
#Bastante Frequente = 2

def resposta(ponto):

    if ponto == -2:
        return 'Muito Raramente'
    
    elif ponto == -1:
        return 'Ocasionalmente'

    elif ponto == 0:
        return 'Neutro'

    elif ponto == 1:
        return 'Comum'

    elif ponto == 2:
        return 'Bastante Frequente'

#---------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------
#Cria uma função responsável por determinar a(s) dominante(s) com base nas pontuações e retorna uma lista

def escolher_dom(funcoes):

    dominantes = []

    pos = max(funcoes, key = lambda k: funcoes[k])
    maior_valor = funcoes[pos]

    for item in funcoes:

        if funcoes[item] == maior_valor:

            dominantes.append(item)
        
    return dominantes

#---------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------
#Cria uma função responsável por determinar a auxiliar com base na dominante e retorna uma lista

def escolher_aux(dominante,funcoes):

    if dominante == 'Ne' or dominante == 'Se':

        if funcoes['Ti'] > funcoes['Fi']:

            return ['Ti']
        
        elif funcoes['Fi'] > funcoes['Ti']:

            return ['Fi']

        else:

            return ['Ti','Fi']

    elif dominante == 'Te' or dominante == 'Fe':

        if funcoes['Si'] > funcoes['Ni']:

            return ['Si']
        
        elif funcoes['Ni'] > funcoes['Si']:

            return ['Ni']
        
        else:

            return ['Si','Ni']

    elif dominante == 'Ni' or dominante == 'Si':

        if funcoes['Te'] > funcoes['Fe']:

            return ['Te']
        
        elif funcoes['Fe'] > funcoes['Te']:

            return ['Fe']
        
        else:

            return ['Te','Fe']

    elif dominante == 'Ti' or dominante == 'Fi':

        if funcoes['Ne'] > funcoes['Se']:

            return ['Ne']
        
        elif funcoes['Se'] > funcoes['Ne']:

            return ['Se']

        else:

            return ['Ne','Se']

#---------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------

def pegaPerguntas():

    resposta_git = requests.get('https://api.github.com/repos/trevensa/mbti/contents/INFOS.txt')
    traducao_py = json.loads(resposta_git.text)
    perguntas = base64.b64decode(traducao_py['content']).decode('UTF-8')

    perguntas = perguntas.split('\n')

    return perguntas

#---------------------------------------------------------------------------------------------

def mbti():

#---------------------------------------------------------------------------------------------
#Declara as variaveis

    primeira_poss = True
    ja_escreveu = True
    dominantes = []
    auxiliares = []
    dominante = ''
    auxiliar = ''
    terciaria = ''
    inferior = ''
    tipo = ''
    pos_tipos = []

#---------------------------------------------------------------------------------------------
#Cria um banco de dados acerca de cada personalidade, indicando as funções de cada uma
#Cria também um dic com as funções onde será armazenado os pontos de cada uma

    tipos = {

        'ISFJ':{'Dominante':'Si', 'Auxiliar':'Fe', 'Terciaria':'Ti', 'Inferior':'Ne'},
        'ISTJ':{'Dominante':'Si', 'Auxiliar':'Te', 'Terciaria':'Fi', 'Inferior':'Ne'},
        'INFJ':{'Dominante':'Ni', 'Auxiliar':'Fe', 'Terciaria':'Ti', 'Inferior':'Se'},
        'INTJ':{'Dominante':'Ni', 'Auxiliar':'Te', 'Terciaria':'Fi', 'Inferior':'Se'},
        'ESFJ':{'Dominante':'Fe', 'Auxiliar':'Si', 'Terciaria':'Ne', 'Inferior':'Ti'},
        'ESTJ':{'Dominante':'Te', 'Auxiliar':'Si', 'Terciaria':'Ne', 'Inferior':'Fi'},
        'ENFJ':{'Dominante':'Fe', 'Auxiliar':'Ni', 'Terciaria':'Se', 'Inferior':'Ti'},
        'ENTJ':{'Dominante':'Te', 'Auxiliar':'Ni', 'Terciaria':'Se', 'Inferior':'Fi'},
        'ISFP':{'Dominante':'Fi', 'Auxiliar':'Se', 'Terciaria':'Ni', 'Inferior':'Te'},
        'ISTP':{'Dominante':'Ti', 'Auxiliar':'Se', 'Terciaria':'Ni', 'Inferior':'Fe'},
        'INFP':{'Dominante':'Fi', 'Auxiliar':'Ne', 'Terciaria':'Si', 'Inferior':'Te'},
        'INTP':{'Dominante':'Ti', 'Auxiliar':'Ne', 'Terciaria':'Si', 'Inferior':'Fe'},
        'ESFP':{'Dominante':'Se', 'Auxiliar':'Fi', 'Terciaria':'Te', 'Inferior':'Ni'},
        'ESTP':{'Dominante':'Se', 'Auxiliar':'Ti', 'Terciaria':'Fe', 'Inferior':'Ni'},
        'ENFP':{'Dominante':'Ne', 'Auxiliar':'Fi', 'Terciaria':'Te', 'Inferior':'Si'},
        'ENTP':{'Dominante':'Ne', 'Auxiliar':'Ti', 'Terciaria':'Fe', 'Inferior':'Si'}

    }

    funcoes = {'Si': 0, 'Se': 0, 'Ni': 0, 'Ne': 0, 'Ti': 0, 'Te': 0, 'Fi': 0, 'Fe': 0}

#---------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------
#Chama a função 'comecou', que explica como funciona o teste

    comecou()

#---------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------
#Abertura da pasta na pasta do aplicativo e do arquivo dentro dela, além de escrever um arquivo introdução pela chamada da função 'introducao'
#Verifica se a pasta já existe
#Verifica se o arquivo com aquele nome já existe, exigindo um novo

    caminho_pasta = os.getcwd()
    nome_pasta = 'Resultados Teste MBTI'

    try:

        os.mkdir(f'{caminho_pasta}\{nome_pasta}')
        introducao(caminho_pasta,nome_pasta,tipos)

    except FileExistsError:

        pass

    escrita_letra('Digite seu nome: ', k, '')
    nome_arquivo = input()
    print()
    arq_existe = os.path.isfile(f'{caminho_pasta}\{nome_pasta}\{nome_arquivo}.txt')

    while arq_existe:

        nome_arquivo = input('Já existe um arquivo com esse nome. Escolha um novo: ')
        arq_existe = os.path.isfile(f'{caminho_pasta}\{nome_pasta}\{nome_arquivo}.txt')

    arq = open(f'{caminho_pasta}\{nome_pasta}\{nome_arquivo}.txt','w')

#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------
#Obtém horario e data de realização do teste e introduz as informações do arquivo
#Chama a função 'frescura' para colocar o nome da pessoa com as iniciais maiúsculas e o escreve no arquivo

    horario = datetime.now().strftime('%H:%M')
    data = date.today().strftime('%d/%m/%Y')
    pessoa = frescura(nome_arquivo)

    arq.write(f'Olá, {pessoa}!\n')
    arq.write(f'No dia {data} às {horario} você realizou o teste. Os resultados do mesmo estão neste arquivo.\n\n')

    arq.write('Este é o backup das perguntas e de suas respostas:\n')
    arq.write('-------------------------------------------------------------------------------')
    arq.write('\n')

#---------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------
#Abre o arquivo que contém 3 informações em cada linha:
#1ª: pergunta
#2ª: função cognitiva que receberá pontos
#3ª: função cognitiva que perderá pontos

    perg = pegaPerguntas()

#Quantidade de perguntas:
#Si: 8 | Se: 8 | Ni: 8 | Ne: 8
#Ti: 8 | Te: 7 | Fi: 8 | Fe: 9
#---------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------
#Percorre o arquivo de perguntas e armazena os pontos no dic 'funcoes'
#Cria a váriavel que corresponde ao número da pergunta
#Cria a bool 'dnv' que é utilizada para que o usuário não digite valores fora do esperado

    pos_perg = 1 

    for linha in perg:

        dnv = True
        first = True

        pergunta = linha[:-6]
        adc = linha[-5:-3]
        rem = linha[-2:]

        while dnv:

            try:
                
                if first:

                    first = False
                    pontos = int(input(f'{pos_perg}. {pergunta}'))

                else:

                    pontos = int(input('Isso não é uma resposta válida. Por favor, digite um número dentre -2,-1,0,1 e 2: '))

                if pontos < -2 or pontos > 2:

                    raise ValueError

                dnv = False

            except ValueError:

                pass

        funcoes[adc] += pontos

        if abs(pontos) == 2:

            funcoes[rem] -= pontos

#---------------------------------------------------------------------------------------------
#Chama a função 'escrita' que traduz o que representa o ponto da pessoa
#Escreve a pergunta e a resposta da pessoa no arquivo

        escrita = resposta(pontos)

        arq.write(f'{pergunta}| Frequência: {escrita}\n')

        pos_perg += 1

#---------------------------------------------------------------------------------------------

    arq.write('-------------------------------------------------------------------------------\n\n')
    arq.write('Esses foram os seus resultados:\n\n')

#---------------------------------------------------------------------------------------------
#Percorre o dic 'funcoes' e escreve os resultados no arquivo de texto
#Estes são so resultados da pessoa, isto é, quantos pontos ela obteve em cada função

    for f in funcoes:

        arq.write(f'{f}: {funcoes[f]}\n')

#---------------------------------------------------------------------------------------------

    arq.write('\nCom base nos seus resultados, obtiveram-se algumas conclusões.\n\n')

#---------------------------------------------------------------------------------------------
#Chama a função 'escolher_dom' para ver qual função é a dominante (a que obteve mais pontos) e retorna uma lista com ela
#Em caso de empate, a lista retornada terá todas funções que obtiveram maior pontuação

    dominantes = escolher_dom(funcoes)

#---------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------
#Para cada item da lista de dominantes será analisada a auxiliar
#Para isso, chama-se a função 'escolher_aux', que retorna uma lista com a auxiliar que obteve mais pontos
#Em caso de empate, ambas possibilidades de auxiliar são devolvidas na lista

    for dominante in dominantes:

        auxiliares = escolher_aux(dominante,funcoes)

        for auxiliar in auxiliares:

#---------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------   
#Determina com base na dominante e na auxiliar da pessoa, qual o tipo mais provável dela
#Também pega no dic tipos quais são as funções Terciaria e Inferior, com base na dominante e na auxiliar
#Por causa dos 'for' anteriores, esse processo será repetido para toda dominante e toda auxiliar, caso a lista tenha mais de uma possibilidade

            for j in tipos:

                if tipos[j]['Dominante'] == dominante and tipos[j]['Auxiliar'] == auxiliar:

                    tipo = j
                    terciaria = tipos[j]['Terciaria']
                    inferior = tipos[j]['Inferior']

                    break

#--------------------------------------------------------------------------------------------- 

#---------------------------------------------------------------------------------------------
#Digita, no arquivo, as funções dominante, auxiliar, terciaria e inferior da pessoa e também informa o tipo da mesma
#Caso existam mais de uma possibilidade, os textos digitados são diferentes para ficar coerente 
#Além disso, caso exista mais de uma possibilidade de tipo, cada tipo é adicionado na lista 'pos_tipos'

            if len(dominantes) > 1 or len(auxiliares) > 1:

                pos_tipos.append(tipo)

                if ja_escreveu:

                    arq.write('Houve um empate na pontuação de algumas funções e, portanto, existem as seguintes possibilidades:\n\n')
                    ja_escreveu = False

                if primeira_poss:

                    arq.write('-------------------------------------------------------------------------------\n')
                    texto = 'uma'
                    primeira_poss = False

                else:

                    texto = 'outra'

                arq.write(f'Esta é {texto} possibilidade:\n\n')
                arq.write(f'Função Dominante: {dominante}\n')
                arq.write(f'Função Auxiliar: {auxiliar}\n')
                arq.write(f'Função Terciária: {terciaria}\n')
                arq.write(f'Função Inferior: {inferior}\n')
                arq.write('\n')
                arq.write(f'Logo, {texto} possibilidade de tipo é {tipo}\n')
                arq.write('-------------------------------------------------------------------------------\n')

            else:

                arq.write(f'Função Dominante: {dominante}\n')
                arq.write(f'Função Auxiliar: {auxiliar}\n')
                arq.write(f'Função Terciária: {terciaria}\n')
                arq.write(f'Função Inferior: {inferior}\n')
                arq.write('\n')
                arq.write(f'Logo, o seu tipo mais provável é {tipo}')

#---------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------
#Se houver mais de uma possibilidade de tipo, seja ela dominante ou auxiliar, é escrito no arquivo uma parte final
#Nessa parte, é indicado de forma mais direta quais são os possíveis tipos da pessoa

    if len(pos_tipos) > 1:

        arq.write('\nPortanto, conclui-se que suas possibilidades de personalidade são: ')

        for uni in range(len(pos_tipos)):

            unidade = pos_tipos[uni]

            if uni == (len(pos_tipos)-1):

                arq.write(f'e {unidade}.')
            
            elif uni == (len(pos_tipos)-2):

                arq.write(f'{unidade} ')

            else:

                arq.write(f'{unidade}, ')

#---------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------
#Chama a função 'acabou'

    acabou()

#---------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------
#Fecha o arquivo    
        
    arq.close()

#---------------------------------------------------------------------------------------------

mbti()