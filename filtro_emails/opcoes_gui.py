from tkinter import *

class GUIOptions(Frame):
    def __init__(self, master, *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)
        self.master = master
        self.meu_frame = Frame(self.master)
        self.meu_frame.pack()

        self.btn1 = Button(self.master, text="Abre uma nova janela", command=self.abre_tela)
        self.btn1.pack()

        self.text = Text(self.master, width=20, height=3)
        self.text.pack()
        self.text.insert(END, 'Antes\ntela\ninteração')

    def abre_tela(self):
        self.top = Toplevel(self.master)
        self.top.grab_set()

        def replace_text():
            self.text.delete(1.0, END)
            self.text.insert(END, 'Text do\nToplevel')

        top_btn = Button(self.top, text='Substitui na tela principal', command=replace_text)
        top_btn.pack()

if __name__ == '__main__':
    opcoes = Tk()
    app = GUIOptions(opcoes)
    opcoes.mainloop()