from tkinter import *

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
        self.bloco1['width'] = 700
        self.bloco1['height'] = 350
        self.bloco1.pack()

        self.bemvindo = Label(self.bloco1)
        self.bemvindo['text'] = 'Bem-Vindo ao teste de MBTI!'
        self.bemvindo['font'] = ('Arial','20','bold')
        self.bemvindo.pack()

        self.bloco2 = Frame(master)
        self.bloco2['width'] = 700
        self.bloco2['height'] = 350
        self.bloco2.pack()

        self.iniciar_teste = Button(self.bloco2)
        self.iniciar_teste['width'] = 20
        self.iniciar_teste['text'] = 'Iniciar o teste'
        self.iniciar_teste['command'] = self.segundaPagina
        self.iniciar_teste.pack(side=RIGHT)

#---------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------
#Destruição do layout anterior (página 1) e montagem de um novo para a página 2
#Esta página contém as instruções a respeito do teste e sua realização

    def segundaPagina(self,master=None):

        self.bemvindo.destroy()
        self.iniciar_teste.destroy()

        self.instrucoes = Label(self.bloco1)
        self.instrucoes['text'] = 'Trocamos de Pagina'
        self.instrucoes.pack()

        self.comecar = Button(self.bloco2)
        self.comecar['text'] = 'Começar o questionário'
        self.comecar['width'] = 25
        self.comecar['command'] = self.terceiraPagina
        self.comecar.pack(side=RIGHT)

#---------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------
#Destruição do layout anterior (página 2) e montagem de um novo para a página 3
#Esta página apresenta as perguntas e um possui espaço para a pessoa colocar sua resposta

    def terceiraPagina(self, master=None):

        self.bloco1.destroy()
        self.bloco2.destroy()
        self.instrucoes.destroy()
        self.comecar.destroy()

        self.pos = 1
        self.k = 0
        self.mensagens = pegaPerguntas()
        self.respostas = []
        self.barra = []

        for item in self.mensagens:

            self.respostas.append('-')
            self.barra.append('_')

        self.quadrante1 = Frame(master)
        self.quadrante1['padx'] = 50
        self.quadrante1['pady'] = 25
        #self.quadrante1['bg'] = '#993399'
        self.quadrante1.pack()

        self.pergunta = Label(self.quadrante1, text=self.mensagens[self.k])
        self.pergunta['width'] = 50
        self.pergunta['font'] = ('Calibri','16')
        self.pergunta.pack()

        self.status = Label(self.quadrante1, text='Sua resposta: ' + self.respostas[self.k])
        self.status['font'] = ('Calibri','10','bold')
        self.status['pady'] = 20
        self.status.pack(side=BOTTOM)

        self.quadrante2 = Frame(master)
        self.quadrante2['padx'] = 50
        self.quadrante2['pady'] = 25
        #self.quadrante2['bg'] = '#ffff99'
        self.quadrante2.pack()

        self.resposta = Entry(self.quadrante2)
        self.resposta['width'] = 15
        self.resposta['justify'] = ('center')
        self.resposta.pack()

        self.aviso = Label(self.quadrante2)
        self.aviso['font'] = ('Calibri','10','bold')
        self.aviso['fg'] = '#ff0000'
        self.aviso['height'] = 5
        self.aviso.pack(side=BOTTOM)

        self.quadrante3 = Frame(master)
        self.quadrante3['padx'] = 50
        self.quadrante3['pady'] = 25
        #self.quadrante3['bg'] = '#66ffff'
        self.quadrante3.pack()

        self.confirma = Button(self.quadrante3)
        self.confirma['text'] = 'Confirmar'
        self.confirma['width'] = 10
        self.confirma['command'] = self.enviaResposta
        self.confirma.pack()

        self.proximo = Button(self.quadrante3)
        self.proximo['text'] = 'Próxima >>'
        self.proximo['width'] = 10
        self.proximo['command'] = self.proximaMensagem
        self.proximo.pack(side=RIGHT)

        self.anterior = Button(self.quadrante3)
        self.anterior['text'] = '<< Anterior'
        self.anterior['width'] = 10
        self.anterior['command'] = self.anteriorMensagem
        self.anterior.pack(side=LEFT)

        self.espaco = Label(self.quadrante3, text=10*' ')
        self.espaco['height'] = 5
        self.espaco.pack(side=BOTTOM)

        self.quadrante4 = Frame(master)
        self.quadrante4['padx'] = 50
        self.quadrante4['pady'] = 25
        #self.quadrante4['bg'] = '#ff9933'
        self.quadrante4.pack()

        self.termina = Button(self.quadrante4)
        self.termina['text'] = 'Finalizar Teste'
        self.termina['width'] = 15
        self.termina['command'] = self.finalizaTeste
        self.termina.pack()

        self.barrinha = Label(self.quadrante4, text=''.join(self.barra))
        self.barrinha['fg'] = '#00cc00'
        self.barrinha['font'] = ('Arial', '15')
        self.barrinha.pack()

        self.progresso = Label(self.quadrante4, text= str(self.pos) + '/' + str(len(self.mensagens)))
        self.progresso['font'] = ('Arial','8','italic')
        self.progresso['height'] = 5
        self.progresso.pack()

#---------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------
#Destruição do layout anterior (página 3) e montagem de um novo para a página 4
#Esta página informa onde os resultados estarão disponibilizados e se despede

    def ultimaPagina(self,master=None):

        self.quadrante1.destroy()
        self.pergunta.destroy()
        self.status.destroy()
        self.quadrante2.destroy()
        self.resposta.destroy()
        self.aviso.destroy()
        self.quadrante3.destroy()
        self.confirma.destroy()
        self.proximo.destroy()
        self.anterior.destroy()
        self.espaco.destroy()
        self.quadrante4.destroy()
        self.termina.destroy()
        self.barrinha.destroy()
        self.progresso.destroy()

        self.quadro1 = Frame(master)
        self.quadro1.pack()

        self.despedida = Label(self.quadro1)
        self.despedida['text'] = 'Obrigado por realizar o teste!\nSeus resultados estão em uma pasta\nlocalizada junto com seu aplicativo.'
        self.despedida['font'] = ('Verdana','20','bold')
        self.despedida.pack()

#---------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------
#Método responsável por somar 1 ao contador 'k'
#Com isso, a pergunta, a página, o status de resposta e o aviso são atualizados

    def proximaMensagem(self):

        if self.k < len(self.mensagens)-1:
            self.k += 1
            self.pos += 1

        self.pergunta['text'] = self.mensagens[self.k]
        self.progresso['text'] = str(self.pos) + '/' + str(len(self.mensagens))
        self.status['text'] = 'Sua resposta: ' + self.respostas[self.k]
        self.aviso['text'] = ''

#---------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------
#Método responsável por subtrair 1 do contador 'k'
#Com isso, a pergunta, a página, o status de resposta e o aviso são atualizados

    def anteriorMensagem(self):

        if self.k > 0:
            self.k -= 1
            self.pos -= 1

        self.pergunta['text'] = self.mensagens[self.k]
        self.progresso['text'] = str(self.pos) + '/' + str(len(self.mensagens))
        self.status['text'] = 'Sua resposta: ' + self.respostas[self.k]
        self.aviso['text'] = ''

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

            self.barra[self.k] = '-'

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
root.mainloop()

#---------------------------------------------------------------------------------------------