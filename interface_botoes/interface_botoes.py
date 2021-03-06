from tkinter import *
import os, getpass, time, json, requests, base64
from datetime import date, datetime

#https://www.w3schools.com/colors/colors_picker.asp
#https://www.invertexto.com/simbolos-para-copiar
#pyinstaller interface_botoes.py --onefile --windowed --distpath . --icon iconeteste.ico --name TesteDeMBTI

#---------------------------------------------------------------------------------------------
#Função que chama o método de voltar para a pergunta anterior

def moveAnterior():

    try:

        APP.anteriorMensagem()

    except:
        
        pass

#---------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------
#Função que chama o método de avançar para a próxima pergunta

def moveProximo():

    try:

        APP.proximaMensagem()

    except:
        
        pass

#---------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------
#Função que ativada quando o botão 'Enter' for pressionado
#Verifica qual das caixas de texto possui informação e executa o método de acordo com isso

def enterPressionado():

    try:
    
        pagina = APP.n_pagina.get()
        APP.pulaPagina()

    except:

        pass

#---------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------
#Função que confere se o número da página digitado é uma página de verdade

def conferePagina(pagina,perguntas):

    try:

        numero_pagina = int(pagina)

        if numero_pagina < 1 or numero_pagina > len(perguntas):

            raise ValueError

        return numero_pagina

    except ValueError:

        return 'INVALIDO'

#---------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------
#Função que obtém as perguntas para o teste de um arquivo txt ja existente

def pegaPerguntas():

    resposta_git = requests.get('https://api.github.com/repos/trevensa/mbti/contents/INFOS.txt')
    traducao_py = json.loads(resposta_git.text)
    perguntas = base64.b64decode(traducao_py['content']).decode('UTF-8')

    perguntas = perguntas.split('\n')

    return perguntas

#---------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------
#Função que divide os itens de uma lista dada em 2 linhas (coloca um '\n' perto do meio)

def quebraPergunta(perguntas):

    for i in range(len(perguntas)):

        index = perguntas[i].index(' ',int(len(perguntas[i])/2))

        p1 = perguntas[i][:index]
        p2 = perguntas[i][index+1:]

        perguntas[i] = p1 + '\n' + p2

    return perguntas

#---------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------
#Função responsável por verificar se a resposta digitada é válida ou não

def corrigeResposta(resposta):

    try:

        pontos = int(resposta)

        if pontos < -2 or pontos > 2:

            raise ValueError

        return pontos

    except ValueError:

        return 'INVALIDO'

#---------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------
#Função que cria um arquivo introdutório sobre o conteúdo de MBTI

def escreveIntroducao(way,nome_pasta):

    resposta_git = requests.get('https://api.github.com/repos/trevensa/mbti/contents/INTRO.txt')
    traducao_py = json.loads(resposta_git.text)
    texto = base64.b64decode(traducao_py['content']).decode('UTF-8')

    readme = open(f'{way}\{nome_pasta}\INTRODUCAO.txt','w')
    readme.write(texto)
    readme.close()

#---------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------
#Função responsável por criar uma pasta no mesmo lugar em que se localiza o aplicativo
#Além disso, abre um arquivo de texto dentro desta pasta onde serão armazenados os resultados do usuário

def criaPasta(nome_arquivo):

    caminho_pasta = os.getcwd()
    nome_pasta = 'Resultados Teste MBTI'

    try:

        os.mkdir(f'{caminho_pasta}\{nome_pasta}')
        escreveIntroducao(caminho_pasta,nome_pasta)

    except FileExistsError:

        pass

    arq_existe = os.path.isfile(f'{caminho_pasta}\{nome_pasta}\{nome_arquivo}.txt')

    if arq_existe:

        return 'EXISTE'

    f = open(f'{caminho_pasta}\{nome_pasta}\{nome_arquivo}.txt','w')

    return f

#---------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------
#Função que recebe uma(s) palavra(s) e coloca a(s) inicial(is) em letra maiúscula

def colocaMaiusculo(nome_arquivo):

    nomes = nome_arquivo.split()

    for qtd in range(len(nomes)):

        nomes[qtd] = nomes[qtd].capitalize()

    return ' '.join(nomes)

#---------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------
#Função responsável por escrever as informações iniciais no arquivo de resultados da pessoa

def escreveCabecalho(nome_arquivo,f):

    horario = datetime.now().strftime('%H:%M')
    data = date.today().strftime('%d/%m/%Y')
    pessoa = colocaMaiusculo(nome_arquivo)

    f.write(f'Olá, {pessoa}!\n')
    f.write(f'No dia {data} às {horario} você realizou o teste. Os resultados do mesmo estão neste arquivo.\n')

#---------------------------------------------------------------------------------------------

def escreveBackup(escritas,perguntas,f):

    f.write('\n\n-------------------------------------------------------------------------------\n')
    f.write('Este é o backup das perguntas e de suas respostas:\n')
    f.write('-------------------------------------------------------------------------------')
    f.write('\n')

    for p in range(len(perguntas)):

        f.write(f'{perguntas[p][:-6]}| {escritas[p]}\n')

    f.write('-------------------------------------------------------------------------------')

#---------------------------------------------------------------------------------------------
#Função que 'traduz' o ponto do usuário para a palavra associada àquele valor

def traduzPontos(pontos):

    if pontos == -2:
        return 'Raramente'
    
    elif pontos == -1:
        return 'Ocasionalmente'

    elif pontos == 0:
        return 'Neutro'

    elif pontos == 1:
        return 'Comumente'

    elif pontos == 2:
        return 'Muito Frequentemente'

    elif pontos == '':
        return ''

#---------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------
#Função que contabiliza os pontos do usuário

def contabilizaPontos(perguntas,respostas,f):

    funcoes = {'Si': 0, 'Se': 0, 'Ni': 0, 'Ne': 0, 'Ti': 0, 'Te': 0, 'Fi': 0, 'Fe': 0}
    escritas = []

    for linha in range(len(perguntas)):

        pergunta = perguntas[linha][:-6]
        adc = perguntas[linha][-5:-3]
        rem = perguntas[linha][-2:]

        pontos = int(respostas[linha])
        escrita = traduzPontos(pontos)
        escritas.append(escrita)

        funcoes[adc] += pontos

        if pontos == 2:

            funcoes[rem] -= pontos
    
    return funcoes, escritas

#---------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------
#Função que escreve as pontuações finais no arquivo de texto

def escrevePontos(funcoes,f):

    f.write('\nEsses foram os seus resultados:\n\n')

    for item in funcoes:

        f.write(f'{item}: {funcoes[item]}\n')

    f.write('\nCom base nos seus resultados, obtiveram-se algumas conclusões.\n\n')

#---------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------
#Função que seleciona as funções cognitivas com maiores pontuações
#Retorna uma lista

def escolheDominante(funcoes):

    dominantes = []

    pos = max(funcoes, key = lambda k: funcoes[k])
    maior_valor = funcoes[pos]

    for item in funcoes:

        if funcoes[item] == maior_valor:

            dominantes.append(item)
        
    return dominantes

#---------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------
#Função que seleciona a função cognitva auxiliar com mais pontos para a função dominante fornecida
#Retorna uma lista

def escolheAuxiliar(funcoes,dominante):

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
#Obtém-se a(s) dominante(s) do teste do usuário
#Para cada dominante possível, analisa-se a(s) auxiliar(es) com maior pontuação
#Para cada combinação de dominante e auxiliar possível, escreve-se no arquivo de texto
#Por fim, escreve no arquivo de texto qual(is) a(s) possibilidade(s) de tipo mais provável(is)
#Fecha o arquivo de texto

def analisaPontos(funcoes,f):

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

    dominantes = escolheDominante(funcoes)

    for dominante in dominantes:

        auxiliares = escolheAuxiliar(funcoes,dominante)

        for auxiliar in auxiliares:

            for j in tipos:

                if tipos[j]['Dominante'] == dominante and tipos[j]['Auxiliar'] == auxiliar:

                    tipo = j
                    terciaria = tipos[j]['Terciaria']
                    inferior = tipos[j]['Inferior']

                    break

            if len(dominantes) > 1 or len(auxiliares) > 1:

                pos_tipos.append(tipo)

                if ja_escreveu:

                    f.write('Houve um empate na pontuação de algumas funções e, portanto, existem as seguintes possibilidades:\n\n')
                    ja_escreveu = False

                if primeira_poss:

                    f.write('-------------------------------------------------------------------------------\n')
                    texto = 'uma'
                    primeira_poss = False

                else:

                    texto = 'outra'

                f.write(f'Esta é {texto} possibilidade:\n\n')
                f.write(f'Função Dominante: {dominante}\n')
                f.write(f'Função Auxiliar: {auxiliar}\n')
                f.write(f'Função Terciária: {terciaria}\n')
                f.write(f'Função Inferior: {inferior}\n')
                f.write('\n')
                f.write(f'Logo, {texto} possibilidade de tipo é {tipo}\n')
                f.write('-------------------------------------------------------------------------------\n')

            else:

                f.write(f'Função Dominante: {dominante}\n')
                f.write(f'Função Auxiliar: {auxiliar}\n')
                f.write(f'Função Terciária: {terciaria}\n')
                f.write(f'Função Inferior: {inferior}\n')
                f.write('\n')
                f.write(f'Logo, o seu tipo mais provável é {tipo}')

    if len(pos_tipos) > 1:

        f.write('\nPortanto, conclui-se que suas possibilidades de personalidade são: ')

        for uni in range(len(pos_tipos)):

            unidade = pos_tipos[uni]

            if uni == (len(pos_tipos)-1):

                f.write(f'e {unidade}.')
            
            elif uni == (len(pos_tipos)-2):

                f.write(f'{unidade} ')

            else:

                f.write(f'{unidade}, ')

#---------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------
#Função que executa toda a análise dos resultados e os escreve no arquivo de texto

def analisaResultados(nome_arquivo,perguntas,respostas,f):

    escreveCabecalho(nome_arquivo,f)
    funcoes,escritas = contabilizaPontos(perguntas,respostas,f)
    escrevePontos(funcoes,f)
    analisaPontos(funcoes,f)
    escreveBackup(escritas,perguntas,f)

#---------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------
#Criação de uma classe 'Aplicativo' que contém a interface do teste

class Aplicativo:

#---------------------------------------------------------------------------------------------
#Montagem do layout da página 1 do aplicativo
#Essa página contém uma saudação à quem está realizando o teste

    def __init__(self,master=None):

        self.bloco1 = Frame(master)
        self.bloco1['bg'] = '#99ccff'
        self.bloco1.pack()

        self.bemvindo = Label(self.bloco1)
        self.bemvindo['text'] = 'Bem-Vindo ao teste de MBTI-Tipologia de Jung!'
        self.bemvindo['font'] = ('Rockwell','20','bold')
        self.bemvindo['bg'] = '#99ccff'
        self.bemvindo['pady'] = 200
        self.bemvindo['padx'] = 200
        self.bemvindo.pack()

        self.iniciar_teste = Button(self.bloco1)
        self.iniciar_teste['width'] = 20
        self.iniciar_teste['text'] = 'Iniciar o teste'
        self.iniciar_teste['font'] = ('Calibri','12','bold')
        self.iniciar_teste['bd'] = 3
        self.iniciar_teste['relief'] = 'raised'
        self.iniciar_teste['cursor'] = 'hand2'
        self.iniciar_teste['bg'] = '#cce6ff'
        self.iniciar_teste['command'] = self.segundaPagina
        self.iniciar_teste.pack(side=BOTTOM)

        self.bloco2 = Frame(master)
        self.bloco2['bg'] = '#99ccff'
        self.bloco2.pack()

        self.copyright = Label(self.bloco2)
        self.copyright['text'] = 'Feito por Mateus Henrique Trevensoli Travagin e João Henri Carrenho Rocha'
        self.copyright['font'] = ('Rockwell','10')
        self.copyright['bg'] = '#99ccff'
        self.copyright['padx'] = 200
        self.copyright.pack(pady=(100,0))

#---------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------
#Destruição do layout anterior (página 1) e montagem de um novo para a página 2
#Esta página contém as instruções a respeito do teste e sua realização

    def segundaPagina(self,master=None):

        self.bemvindo.destroy()
        self.iniciar_teste.destroy()
        self.bloco1.destroy()
        self.bloco2.destroy()

        self.bloco1 = Frame(master)
        self.bloco1['bg'] = '#99ccff'
        self.bloco1.pack()

        self.instrucoes = Label(self.bloco1)
        self.instrucoes['font'] = ('Berlin Sans','15','bold')
        self.instrucoes['pady'] = 25
        self.instrucoes['padx'] = 300
        self.instrucoes['text'] = 'Instruções'
        self.instrucoes['bg'] = '#99ccff'
        self.instrucoes.pack()

        self.instrucoes2 = Label(self.bloco1)
        self.instrucoes2['font'] = ('Courier New','12')
        self.instrucoes2['bg'] = '#ffffff'
        self.instrucoes2['borderwidth'] = 5
        self.instrucoes2['relief'] = 'ridge'
        self.instrucoes2['pady'] = 10
        self.instrucoes2['padx'] = 30
        self.instrucoes2['justify'] = 'left'
        self.instrucoes2['text'] = 'O teste é composto de 72 questões, as quais você\ndeve responder com base na frequência em que\nvocê realiza o que está escrito.\nSuas opções são:\n\n- Raramente\n- Ocasionalmente\n- Neutro\n- Comumente\n- Muito frequentemente\n\nTente ser honesto com as respostas mesmo que elas te\ndesagradem ou te envergonhem de alguma forma.\nVale ressaltar que, nesses casos, geralmente\na resposta verdadeira é aquela que você sente\ndesconforto em pensar.\n\nBom teste!'
        self.instrucoes2.pack(side=BOTTOM)

        self.bloco2 = Frame(master)
        self.bloco2['bg'] = '#99ccff'
        self.bloco2.pack()

        self.comecar = Button(self.bloco2)
        self.comecar['width'] = 25
        self.comecar['text'] = 'Começar o Questionário'
        self.comecar['font'] = ('Calibri','12','bold')
        self.comecar['bd'] = 3
        self.comecar['relief'] = 'raised'
        self.comecar['cursor'] = 'hand2'
        self.comecar['bg'] = '#cce6ff'
        self.comecar['command'] = self.terceiraPagina
        self.comecar.pack(pady=(25,0))

#---------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------
#Destruição do layout anterior (página 2) e montagem de um novo para a página 3
#Esta página apresenta as perguntas e um possui espaço para a pessoa colocar sua resposta

    def terceiraPagina(self, master=None):

        self.bloco1.destroy()
        self.bloco2.destroy()
        self.instrucoes.destroy()
        self.instrucoes2.destroy()
        self.comecar.destroy()

        self.v = IntVar(value=5)

        self.k = 0
        self.perguntas = pegaPerguntas()
        #self.perguntas = ['feijao: $Si$Se','batata: $Fe$Fi','manga: $Ti$Te']
        self.mensagens = self.perguntas[:]

        for w in range (len(self.mensagens)):
        
            self.mensagens[w] = self.mensagens[w][:-6]

        self.mensagens = quebraPergunta(self.mensagens)

        self.respostas = []
        self.barra = []

        for item in self.mensagens:

            self.respostas.append('')
            self.barra.append('☐')

        self.pos_barra = self.barra[:]
        self.pos_barra[self.k] = '•'

        self.bloco1 = Frame(master)
        self.bloco1['bg'] = '#99ccff'
        self.bloco1.pack()

        self.pergunta = Label(self.bloco1, text=self.mensagens[self.k])
        self.pergunta['pady'] = 25
        self.pergunta['font'] = ('Century Gothic','18','bold')
        self.pergunta['bg'] = '#99ccff'
        self.pergunta.pack()

        self.status = Label(self.bloco1, text='Sua resposta: ' + str(self.respostas[self.k]))
        self.status['font'] = ('Courier New','11','bold')
        self.status['bg'] = '#99ccff'
        self.status['pady'] = 15
        self.status.pack(side=BOTTOM)

        self.bloco2 = Frame(master)
        self.bloco2['bg'] = '#99ccff'
        self.bloco2.pack()

        self.opcao1 = Radiobutton(self.bloco2)
        self.opcao1['text'] = 'Raramente'
        self.opcao1['font'] = ('Courier New','11','bold')
        self.opcao1['command'] = self.selecionaBotao
        self.opcao1['variable'] = self.v
        self.opcao1['value'] = -2
        self.opcao1['bg'] = '#99ccff'
        self.opcao1.pack(side=LEFT, padx=20)

        self.opcao2 = Radiobutton(self.bloco2)
        self.opcao2['text'] = 'Ocasionalmente'
        self.opcao2['font'] = ('Courier New','11','bold')
        self.opcao2['command'] = self.selecionaBotao
        self.opcao2['variable'] = self.v
        self.opcao2['value'] = -1
        self.opcao2['bg'] = '#99ccff'
        self.opcao2.pack(side=LEFT, padx=20)

        self.opcao3 = Radiobutton(self.bloco2)
        self.opcao3['text'] = 'Neutro'
        self.opcao3['font'] = ('Courier New','11','bold')
        self.opcao3['command'] = self.selecionaBotao
        self.opcao3['variable'] = self.v
        self.opcao3['value'] = 0
        self.opcao3['bg'] = '#99ccff'
        self.opcao3.pack(side=LEFT, padx=20)

        self.opcao4 = Radiobutton(self.bloco2)
        self.opcao4['text'] = 'Comumente'
        self.opcao4['font'] = ('Courier New','11','bold')
        self.opcao4['command'] = self.selecionaBotao
        self.opcao4['variable'] = self.v
        self.opcao4['value'] = 1
        self.opcao4['bg'] = '#99ccff'
        self.opcao4.pack(side=LEFT, padx=20)

        self.opcao5 = Radiobutton(self.bloco2)
        self.opcao5['text'] = 'Muito Frequentemente'
        self.opcao5['font'] = ('Courier New','11','bold')
        self.opcao5['command'] = self.selecionaBotao
        self.opcao5['variable'] = self.v
        self.opcao5['value'] = 2
        self.opcao5['bg'] = '#99ccff'
        self.opcao5.pack(side=LEFT, padx=20)

        self.aviso = Label()
        self.aviso['font'] = ('Courier New','11','bold')
        self.aviso['pady'] = 15
        self.aviso['fg'] = '#ff0000'
        self.aviso['bg'] = '#99ccff'
        self.aviso.pack()

        self.bloco3 = Frame(master)
        self.bloco3['bg'] = '#99ccff'
        self.bloco3.pack()

        self.proximo = Button(self.bloco3)
        self.proximo['width'] = 10
        self.proximo['text'] = 'Próxima >>'
        self.proximo['font'] = ('Calibri','12','bold')
        self.proximo['bd'] = 3
        self.proximo['relief'] = 'raised'
        self.proximo['cursor'] = 'hand2'
        self.proximo['bg'] = '#cce6ff'
        self.proximo['command'] = self.proximaMensagem
        self.proximo.pack(side=RIGHT)

        self.anterior = Button(self.bloco3)
        self.anterior['width'] = 10
        self.anterior['text'] = '<< Anterior'
        self.anterior['font'] = ('Calibri','12','bold')
        self.anterior['bd'] = 3
        self.anterior['relief'] = 'raised'
        self.anterior['cursor'] = 'hand2'
        self.anterior['bg'] = '#cce6ff'
        self.anterior['command'] = self.anteriorMensagem
        self.anterior.pack(side=LEFT)

        self.bloco4 = Frame(master)
        self.bloco4['bg'] = '#99ccff'
        self.bloco4.pack(pady=(20,10))

        self.ir_pagina = Label(self.bloco4)
        self.ir_pagina['text'] = 'Insira a página de destino: '
        self.ir_pagina['bg'] = '#99ccff'
        self.ir_pagina['font'] = ('Courier New','11','bold')
        self.ir_pagina.pack(side=LEFT,padx=(20,10),pady=(20,5))

        self.ir = Button(self.bloco4)
        self.ir['width'] = 10
        self.ir['text'] = 'Ir'
        self.ir['font'] = ('Calibri','12','bold')
        self.ir['bd'] = 3
        self.ir['relief'] = 'raised'
        self.ir['cursor'] = 'hand2'
        self.ir['bg'] = '#cce6ff'
        self.ir['command'] = self.pulaPagina
        self.ir.pack(side=RIGHT,padx=(20,20),pady=(20,5))

        self.n_pagina = Entry(self.bloco4)
        self.n_pagina['width'] = 15
        self.n_pagina['justify'] = ('center')
        self.n_pagina.pack(side=RIGHT,pady=(20,5))

        self.bloco5 = Frame(master)
        self.bloco5['bg'] = '#99ccff'
        self.bloco5['height'] = 35
        self.bloco5.pack(pady=30)

        self.termina = Button(self.bloco5)
        self.termina['width'] = 20
        self.termina['text'] = 'Finalizar Teste'
        self.termina['font'] = ('Calibri','12','bold')
        self.termina['bd'] = 3
        self.termina['relief'] = 'raised'
        self.termina['cursor'] = 'hand2'
        self.termina['bg'] = '#cce6ff'
        self.termina['command'] = self.finalizaTeste
        self.termina.pack()
        self.termina.pack_forget()

        self.bloco6 = Frame(master)
        self.bloco6['bg'] = '#99ccff'
        self.bloco6.pack()

        self.barrinha = Label(self.bloco6, text=''.join(self.pos_barra))
        self.barrinha['fg'] = '#00264d'
        self.barrinha['bg'] = '#99ccff'
        self.barrinha['font'] = ('Courier New', '8')
        self.barrinha.pack()

        self.progresso = Label(self.bloco6, text= str(self.k+1) + '/' + str(len(self.mensagens)))
        self.progresso['font'] = ('Courier New','10','italic')
        self.progresso['bg'] = '#99ccff'
        self.progresso.pack(pady=(60,0))

#---------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------
#Destruição do layout anterior (página 3) e montagem de um novo para a página 4
#Esta página informa onde os resultados estarão disponibilizados e se despede

    def ultimaPagina(self,master=None):

        self.bloco1.destroy()
        self.pergunta.destroy()
        self.status.destroy()
        self.bloco2.destroy()
        self.opcao1.destroy()
        self.opcao2.destroy()
        self.opcao3.destroy()
        self.opcao4.destroy()
        self.opcao5.destroy()
        self.aviso.destroy()
        self.bloco3.destroy()
        self.proximo.destroy()
        self.anterior.destroy()
        self.bloco4.destroy()
        self.termina.destroy()
        self.barrinha.destroy()
        self.progresso.destroy()
        self.ir_pagina.destroy()
        self.n_pagina.destroy()
        self.ir.destroy()
        self.bloco5.destroy()
        self.bloco6.destroy()

        self.bloco1 = Frame(master)
        self.bloco1['bg'] = '#99ccff'
        self.bloco1.pack()

        self.despedida = Label(self.bloco1)
        self.despedida['bg'] = '#99ccff'
        self.despedida['text'] = 'Obrigado por realizar o teste!\nPara salvar seus resultados, digite seu nome e clique\nem "Escolher Nome". Feito isso, seus resultados estarão\nem uma pasta localizada junto com seu aplicativo.\nDentro dela, haverá um arquivo com seus resultados.\n\nDigite seu nome aqui:'
        self.despedida['font'] = ('Century Gothic','20','bold')
        self.despedida.pack(pady=(50,50))

        self.nome = Entry(self.bloco1)
        self.nome['width'] = 25
        self.nome['justify'] = ('center')
        self.nome.pack()

        self.aviso = Label(self.bloco1)
        self.aviso['font'] = ('Courier New','11','bold')
        self.aviso['pady'] = 15
        self.aviso['fg'] = '#ff0000'
        self.aviso['bg'] = '#99ccff'
        self.aviso.pack()

        self.reinicia = Button(self.bloco1)
        self.reinicia['width'] = 20
        self.reinicia['text'] = 'Refazer o Teste'
        self.reinicia['font'] = ('Calibri','12','bold')
        self.reinicia['bd'] = 3
        self.reinicia['relief'] = 'raised'
        self.reinicia['cursor'] = 'hand2'
        self.reinicia['bg'] = '#cce6ff'
        self.reinicia['command'] = self.reiniciaTeste
        self.reinicia.pack(side=BOTTOM,pady=(25,25))

        self.envia_nome = Button(self.bloco1)
        self.envia_nome['width'] = 20
        self.envia_nome['text'] = 'Escolher Nome'
        self.envia_nome['font'] = ('Calibri','12','bold')
        self.envia_nome['bd'] = 3
        self.envia_nome['relief'] = 'raised'
        self.envia_nome['cursor'] = 'hand2'
        self.envia_nome['bg'] = '#cce6ff'
        self.envia_nome['command'] = self.enviaNome
        self.envia_nome.pack(side=BOTTOM,pady=(25,25))

#---------------------------------------------------------------------------------------------
#Método responsável por atualizar as informações da tela:
#a pergunta, a página, o status de resposta e o aviso

    def atualizaInfos(self):

        self.pergunta['text'] = self.mensagens[self.k]
        self.progresso['text'] = str(self.k+1) + '/' + str(len(self.mensagens))
        self.status['text'] = 'Sua resposta: ' + traduzPontos(self.respostas[self.k])
        self.aviso['text'] = ''
        
        self.pos_barra = self.barra[:]
        self.pos_barra[self.k] = '•'

        self.barrinha['text'] = ''.join(self.pos_barra)

        if self.respostas[self.k] == '':

            valor = None
        
        else:

            valor = self.respostas[self.k]

        self.v.set(valor)

#---------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------
#Método responsável por somar 1 ao contador 'k'
#Com isso, a pergunta, a página, o status de resposta e o aviso são atualizados

    def proximaMensagem(self):

        if self.k < len(self.mensagens)-1:
            self.k += 1

        self.atualizaInfos()

#---------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------
#Método responsável por subtrair 1 do contador 'k'
#Com isso, a pergunta, a página, o status de resposta e o aviso são atualizados

    def anteriorMensagem(self):

        if self.k > 0:
            self.k -= 1

        self.atualizaInfos()

#---------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------
#Método chamado ao selecionar um dos botões com as opções
#Pega o valor que aquele botão representa, marca a questão como respondida e passa para a próxima pergunta

    def selecionaBotao(self):

        pontos = self.v.get()
        self.respostas[self.k] = pontos
        self.barra[self.k] = self.barra[self.k].replace('☐','☑')

        vazios = self.respostas.count('')
        if vazios == 0:

            self.termina.pack()

        self.atualizaInfos()

#---------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------
#Método responsável por verificar se todas perguntas foram respondidas
#Em caso afirmativo, executa-se o método 'ultimaPagina'
#Caso contrário, um aviso aparece na tela

    def finalizaTeste(self):

        vazios = self.respostas.count('')

        if vazios == 0:

            self.ultimaPagina()

        else:

            self.aviso['text'] = 'Responda todas as perguntas antes de finalizar o teste'

#---------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------
#Método que cria uma pasta, executa a análise do teste e salva os resultados dentro de um arquivo de texto
#Para isso verifica se a pasta já existe e se já existe um arquivo com o nome digitado pelo usuário

    def enviaNome(self):

        nome_arquivo = self.nome.get()

        f = criaPasta(nome_arquivo)

        if f == 'EXISTE':

            self.aviso['text'] = 'Já existe um arquivo com esse nome. Insira outro nome.'
            self.nome.delete(first='0',last='end')

        else:

            analisaResultados(nome_arquivo,self.perguntas,self.respostas,f)

            f.close()

            self.aviso['fg'] = '#009933'
            self.aviso['text'] = 'Arquivo criado!'

            self.nome.delete(first='0',last='end')

#---------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------
#Método que pula para a página digitada, caso esta exista

    def pulaPagina(self):

        pagina = self.n_pagina.get()

        numero_pagina = conferePagina(pagina,self.perguntas)

        if numero_pagina == 'INVALIDO':

            self.aviso['text'] = 'Essa página não existe. Tente outra.'

        else:

            self.k = numero_pagina-1
            self.atualizaInfos()

        self.n_pagina.delete(first='0',last='end')

#---------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------
#Método que reinicia o teste

    def reiniciaTeste(self):

        self.bloco1.destroy()
        self.despedida.destroy()
        self.nome.destroy()
        self.aviso.destroy()
        self.envia_nome.destroy()
        self.reinicia.destroy()

        self.__init__()

#---------------------------------------------------------------------------------------------

#Inicialização do Aplicativo com o módulo Tkinter
#Definição do nome do teste e do tamanho da janela

root = Tk()
APP = Aplicativo(root)
root.title('Teste MBTI-Tipologia de Jung')
root.geometry('1000x600')
root.maxsize(1000,600)
root.configure(bg='#99ccff')
root.bind('<KP_Enter>',lambda x: enterPressionado())
root.bind('<Return>',lambda x: enterPressionado())
root.bind('<Left>',lambda z: moveAnterior())
root.bind('<Right>',lambda t: moveProximo())
root.mainloop()

#---------------------------------------------------------------------------------------------