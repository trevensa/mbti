from tkinter import *

#https://www.w3schools.com/colors/colors_picker.asp
#https://www.invertexto.com/simbolos-para-copiar

#---------------------------------------------------------------------------------------------
#Função que obtém as perguntas para o teste de um arquivo txt ja existente

def pegaPerguntas():

    try:
        f = open('C:/Users/Mateus/Desktop/perguntas.txt','r',encoding='UTF-8')
        perguntas = []

        for linha in f:
            perguntas.append(linha.replace('\n',''))

    finally:
        f.close()

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
        self.bemvindo['text'] = 'Bem-Vindo ao teste de MBTI!'
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
        self.instrucoes2['bg'] = '#99ccff'
        self.instrucoes2['pady'] = 10
        self.instrucoes2['padx'] = 30
        self.instrucoes2['justify'] = 'left'
        self.instrucoes2['text'] = 'O teste é composto de 72 questões, as quais você\ndeve responder um número de -2 a 2 com base\nna frequência em que você realiza o que está escrito.\n\nLegenda:\n\n-2 = Raramente\n-1 = Ocasionalmente\n0 = Neutro\n1 = Comumente\n2 = Muito frequentemente\n\nTente ser honesto com as respostas mesmo que elas te\ndesagradem ou te envergonhem de alguma forma.\nVale ressaltar que, nesses casos, geralmente\na resposta verdadeira é aquela que você sente\ndesconforto em pensar.\n\nBom teste!\n\n\n'
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
        self.comecar.pack()

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

        self.pos = 1
        self.k = 0
        self.mensagens = pegaPerguntas()
        self.respostas = []
        self.barra = []

        for item in self.mensagens:

            self.respostas.append('-')
            self.barra.append('☐')

        self.bloco1 = Frame(master)
        self.bloco1['bg'] = '#99ccff'
        self.bloco1.pack()

        self.pergunta = Label(self.bloco1, text=self.mensagens[self.k])
        self.pergunta['pady'] = 25
        self.pergunta['font'] = ('Century Gothic','16','bold')
        self.pergunta['bg'] = '#99ccff'
        self.pergunta.pack()

        self.status = Label(self.bloco1, text='Sua resposta: ' + self.respostas[self.k])
        self.status['font'] = ('Courier New','11','bold')
        self.status['bg'] = '#99ccff'
        self.status['pady'] = 15
        self.status.pack(side=BOTTOM)

        self.bloco2 = Frame(master)
        self.bloco2['bg'] = '#99ccff'
        self.bloco2.pack()

        self.resposta = Entry(self.bloco2)
        self.resposta['width'] = 15
        self.resposta['justify'] = ('center')
        self.resposta.pack()

        self.aviso = Label(self.bloco2)
        self.aviso['font'] = ('Courier New','11','bold')
        self.aviso['pady'] = 15
        self.aviso['fg'] = '#ff0000'
        self.aviso['bg'] = '#99ccff'
        self.aviso.pack(side=BOTTOM)

        self.bloco3 = Frame(master)
        self.bloco3['bg'] = '#99ccff'
        self.bloco3.pack()

        self.confirma = Button(self.bloco3)
        self.confirma['width'] = 10
        self.confirma['text'] = 'Confirmar'
        self.confirma['font'] = ('Calibri','12','bold')
        self.confirma['bd'] = 3
        self.confirma['relief'] = 'raised'
        self.confirma['cursor'] = 'hand2'
        self.confirma['bg'] = '#cce6ff'
        self.confirma['command'] = self.enviaResposta
        self.confirma.pack(pady=(10,30))

        self.proximo = Button(self.bloco3)
        self.proximo['width'] = 10
        self.proximo['text'] = 'Próxima >>'
        self.proximo['font'] = ('Calibri','12','bold')
        self.proximo['bd'] = 3
        self.proximo['relief'] = 'raised'
        self.proximo['cursor'] = 'hand2'
        self.proximo['bg'] = '#cce6ff'
        self.proximo['command'] = self.proximaMensagem
        self.proximo.pack(side=RIGHT,padx=(0,15))

        self.anterior = Button(self.bloco3)
        self.anterior['width'] = 10
        self.anterior['text'] = '<< Anterior'
        self.anterior['font'] = ('Calibri','12','bold')
        self.anterior['bd'] = 3
        self.anterior['relief'] = 'raised'
        self.anterior['cursor'] = 'hand2'
        self.anterior['bg'] = '#cce6ff'
        self.anterior['command'] = self.anteriorMensagem
        self.anterior.pack(side=LEFT,padx=(15,0))

        self.bloco4 = Frame(master)
        self.bloco4['bg'] = '#99ccff'
        self.bloco4.pack()

        self.termina = Button(self.bloco4)
        self.termina['width'] = 20
        self.termina['text'] = 'Finalizar Teste'
        self.termina['font'] = ('Calibri','12','bold')
        self.termina['bd'] = 3
        self.termina['relief'] = 'raised'
        self.termina['cursor'] = 'hand2'
        self.termina['bg'] = '#cce6ff'
        self.termina['command'] = self.finalizaTeste
        self.termina.pack(pady=(100,10))

        self.barrinha = Label(self.bloco4, text=''.join(self.barra))
        self.barrinha['fg'] = '#00264d'
        self.barrinha['bg'] = '#99ccff'
        self.barrinha['font'] = ('Courier New', '10')
        self.barrinha.pack(pady=(10,70))

        self.progresso = Label(self.bloco4, text= str(self.pos) + '/' + str(len(self.mensagens)))
        self.progresso['font'] = ('Courier New','10','italic')
        self.progresso['bg'] = '#99ccff'
        self.progresso.pack()

#---------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------
#Destruição do layout anterior (página 3) e montagem de um novo para a página 4
#Esta página informa onde os resultados estarão disponibilizados e se despede

    def ultimaPagina(self,master=None):

        self.bloco1.destroy()
        self.pergunta.destroy()
        self.status.destroy()
        self.bloco2.destroy()
        self.resposta.destroy()
        self.aviso.destroy()
        self.bloco3.destroy()
        self.confirma.destroy()
        self.proximo.destroy()
        self.anterior.destroy()
        self.bloco4.destroy()
        self.termina.destroy()
        self.barrinha.destroy()
        self.progresso.destroy()

        self.bloco1 = Frame(master)
        self.bloco1.pack()

        self.despedida = Label(self.bloco1)
        self.despedida['bg'] = '#99ccff'
        self.despedida['pady'] = 250
        self.despedida['text'] = 'Obrigado por realizar o teste!\nSeus resultados estão em uma pasta\nlocalizada junto com seu aplicativo.'
        self.despedida['font'] = ('Century Gothic','20','bold')
        self.despedida.pack()

#---------------------------------------------------------------------------------------------
#Método responsável por atualizar as informações da tela:
#a pergunta, a página, o status de resposta e o aviso

    def atualizaInfos(self):

        self.pergunta['text'] = self.mensagens[self.k]
        self.progresso['text'] = str(self.pos) + '/' + str(len(self.mensagens))
        self.status['text'] = 'Sua resposta: ' + self.respostas[self.k]
        self.aviso['text'] = ''

#---------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------
#Método responsável por somar 1 ao contador 'k'
#Com isso, a pergunta, a página, o status de resposta e o aviso são atualizados

    def proximaMensagem(self):

        if self.k < len(self.mensagens)-1:
            self.k += 1
            self.pos += 1

        self.atualizaInfos()

#---------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------
#Método responsável por subtrair 1 do contador 'k'
#Com isso, a pergunta, a página, o status de resposta e o aviso são atualizados

    def anteriorMensagem(self):

        if self.k > 0:
            self.k -= 1
            self.pos -= 1

        self.atualizaInfos()

#---------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------
#Método responsável por captar a resposta digitada na caixa de texto
#A função 'corrigeResposta' é chamada para verificar a validez do que foi digitado pelo usuário
#Caso seja inválida, um aviso na tela aparece
#Caso seja válida, a resposta é adicionada na lista 'respostas'
#O status de resposta é alterado e o método 'proximaMensagem' é chamado
#Em ambos os casos, o conteúdo digitado é apagado da caixa de texto

    def enviaResposta(self):

        resposta = self.resposta.get()
        condicao = corrigeResposta(resposta)

        if condicao == 'INVALIDO':

            self.aviso['text'] = 'Isto não é uma resposta válida'

        else:

            self.respostas[self.k] = resposta
            self.status['text'] = 'Sua resposta: ' + self.respostas[self.k]

            self.barra[self.k] = '☑'

            self.barrinha['text'] = ''.join(self.barra)

            self.proximaMensagem()

        self.resposta.delete(first='0',last='end')

#---------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------
#Método responsável por verificar se todas perguntas foram respondidas
#Em caso afirmativo, executa-se o método 'ultimaPagina'
#Caso contrário, um aviso aparece na tela

    def finalizaTeste(self):

        vazios = self.respostas.count('-')

        if vazios == 0:

            self.ultimaPagina()

        else:

            self.aviso['text'] = 'Responda todas as perguntas antes de finalizar o teste'

#---------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------
#Inicialização do Aplicativo com o módulo Tkinter
#Definição do nome do teste e do tamanho da janela

root = Tk()
Aplicativo(root)
root.title('Teste MBTI')
root.geometry('600x600')
root.maxsize(600,600)
root.configure(bg='#99ccff')
root.mainloop()

#---------------------------------------------------------------------------------------------