from tkinter import *

def pegaPerguntas():

    try:
        f = open('C:/Users/Mateus/Desktop/perguntas.txt','r',encoding='UTF-8')
        perguntas = []

        for linha in f:
            perguntas.append(linha.replace('\n',''))

    finally:
        f.close()

    return perguntas

def corrigeResposta(resposta):

    try:

        pontos = int(resposta)

        if pontos < -2 or pontos > 2:

            raise ValueError

        return pontos

    except ValueError:

        return 'INVALIDO'

class Aplicativo:

    def __init__(self, master=None):

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

    def proximaMensagem(self):

        if self.k < len(self.mensagens)-1:
            self.k += 1
            self.pos += 1

        self.pergunta['text'] = self.mensagens[self.k]
        self.progresso['text'] = str(self.pos) + '/' + str(len(self.mensagens))
        self.status['text'] = 'Sua resposta: ' + self.respostas[self.k]
        self.aviso['text'] = ''

    def anteriorMensagem(self):

        if self.k > 0:
            self.k -= 1
            self.pos -= 1

        self.pergunta['text'] = self.mensagens[self.k]
        self.progresso['text'] = str(self.pos) + '/' + str(len(self.mensagens))
        self.status['text'] = 'Sua resposta: ' + self.respostas[self.k]
        self.aviso['text'] = ''

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

        print(self.barra)

    def finalizaTeste(self):

        vazios = self.respostas.count('-')

        if vazios == 0:

            print('Tudo foi respondido')

        else:

            self.aviso['text'] = 'Responda todas as perguntas antes de finalizar o teste'


root = Tk()
Aplicativo(root)
root.title('Teste MBTI')
root.mainloop()

