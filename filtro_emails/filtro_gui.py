import os.path
from tkinter import *
from filtro import Filtro
from configparser import ConfigParser

class FiltroGUI(Frame):
    def __init__(self, master, *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)

        self.master = master
        self.a_frame = Frame(self.master)
        self.a_frame.grid()

        self.title_text = StringVar(self.master)
        self.title_label = Label(self.master, textvariable=self.title_text, font=("Arial", 14))
        self.title_text.set("Filtro de emails")
        self.title_label.grid(row=0, column=0, sticky=W, columnspan=3, pady=5, padx=90)

        self.grava_database = BooleanVar(self.master)
        self.check_database = Checkbutton(self.master, text='Grava na base', variable=self.grava_database)
        self.check_database.grid(row=1, column=0, sticky=W, pady=5, padx=10)

        self.filtra_in_check = BooleanVar(self.master)
        self.check_filtra_in = Checkbutton(self.master, text='Filtra IN', variable=self.filtra_in_check, command=self.change_state_in)
        self.check_filtra_in.grid(row=2, column=0, sticky=W, pady=5, padx=10)

        self.palavras_in_entry_text = StringVar(self.master)
        self.palavras_in_entry = Entry(self.master, textvariable=self.palavras_in_entry_text, width=20)
        self.palavras_in_entry.grid(row=2, column=0, sticky=W, pady=5, padx=90)

        self.filtra_out_check = BooleanVar(self.master)
        self.check_filtra_out = Checkbutton(self.master, text='Filtra OUT', variable=self.filtra_out_check, command=self.change_state_out)
        self.check_filtra_out.grid(row=3, column=0, sticky=W, pady=5, padx=10)

        self.palavras_out_entry_text = StringVar(master)
        self.palavras_out_entry = Entry(master, textvariable=self.palavras_out_entry_text, width=20)
        self.palavras_out_entry.grid(row=3)

        self.config_btn = Button(self.master, text='Opções', command=lambda: self.abre_config())
        self.config_btn.grid(row=4, column=0, sticky=W, columnspan=2, pady=20, ipady=10, padx=10)

        self.execute_btn = Button(self.master, text='Executar', command=lambda: self.execute())
        self.execute_btn.grid(row=4, column=0, columnspan=3, pady=20, ipady=10)

        if os.path.exists('config.ini'):
            self.read_config()
        else:
            self.filtra_in_check.set(True)
            self.filtra_out_check.set(True)
            filtra_presuf_in = False
            self.create_config()

    def create_config(self):
        conf['PALAVRAS.IN'] = {
            'palavras': self.palavras_in_entry.get(),
            'status': self.filtra_in_check.get(),
            'filtra_presuf_in': filtra_presuf_in
        }
        conf['PALAVRAS.OUT'] = {
            'palavras': self.palavras_out_entry.get(),
            'status': self.filtra_out_check.get()
        }

        with open('config.ini', 'w') as file:
            conf.write(file)

    def execute(self):
        self.write_config()

        self.aplica_filtros_in = self.filtra_in_check.get()
        self.aplica_filtros_out = self.filtra_out_check.get()

        filtro = Filtro()
        filtro.filter_emails(
            self.palavras_in_entry_text.get(),
            self.palavras_out_entry_text.get(),
            self.aplica_filtros_in,
            self.aplica_filtros_out,
            self.grava_database.get(),
            filtra_presuf_in
        )

    def change_state_in(self,event=None):
        if self.palavras_in_entry['state'] == 'disabled':
            self.palavras_in_entry['state'] = 'normal'
            self.aplica_filtros_in = True
        else:
            self.palavras_in_entry['state'] = 'disabled'
            self.aplica_filtros_in = False

    def change_state_out(self,event=None):
        if self.palavras_out_entry['state'] == 'disabled':
            self.palavras_out_entry['state'] = 'normal'
            self.aplica_filtros_out = True
        else:
            self.palavras_out_entry['state'] = 'disabled'
            self.aplica_filtros_out = False

    def write_config(self):
        conf['PALAVRAS.IN'] = {
            'palavras': self.palavras_in_entry.get(),
            'status': self.filtra_in_check.get(),
            'filtra_presuf_in': filtra_presuf_in
        }
        conf['PALAVRAS.OUT'] = {
            'palavras': self.palavras_out_entry.get(),
            'status': self.filtra_out_check.get()
        }

        with open('config.ini', 'w') as file:
            conf.write(file)

    def abre_config(self):
        dialog = ConfigGUI(root, '', 'Configurações', '')
        root.wait_window(dialog.top)


    def read_config(self):
        conf.read('config.ini')
        if 'PALAVRAS.IN' in conf.sections():
            if conf['PALAVRAS.IN']['status'] == 'True':
                self.filtra_in_check.set(True)
            else:
                self.filtra_in_check.set(False)

            if conf['PALAVRAS.IN']['filtra_presuf_in'] == 'True':
                filtra_presuf_in = True
            else:
                filtra_presuf_in = False

            self.palavras_in_entry.insert(0, conf['PALAVRAS.IN']['palavras'])

        if 'PALAVRAS.OUT' in conf.sections():
            if conf['PALAVRAS.OUT']['status'] == 'True':
                self.filtra_out_check.set(True)
            else:
                self.filtra_out_check.set(False)

            self.palavras_out_entry.insert(0, conf['PALAVRAS.OUT']['palavras'])

        if self.filtra_in_check.get():
            self.palavras_in_entry['state'] = 'normal'
            self.aplica_filtros_in = True
        else:
            self.palavras_in_entry['state'] = 'disabled'
            self.aplica_filtros_in = False

        if self.filtra_out_check.get():
            self.palavras_out_entry['state'] = 'normal'
            self.aplica_filtros_out = True
        else:
            self.palavras_out_entry['state'] = 'disabled'
            self.aplica_filtros_out = False


class ConfigGUI:
    def __init__(self, parent, valor, title, label_text=''):
        global filtra_presuf_in
        self.valor = valor
        self.top = Toplevel(parent)
        self.top.transient(parent)
        self.top.grab_set()

        self.filtra_presuf_in = BooleanVar(self.top)
        self.check_presuf_in = Checkbutton(self.top, text='Aplica filtros IN para prefixo e sufixo do email', variable=self.filtra_presuf_in, command=self.change_state_presuf)
        self.check_presuf_in.grid(row=2, column=0, sticky=W, pady=5, padx=10)

        self.grava_config_btn = Button(self.top, text='Gravar', command=lambda: self.grava())
        self.grava_config_btn.grid(row=4, column=0, columnspan=3, pady=20, ipady=10)

        self.top.title(title)
        root.eval(f'tk::PlaceWindow {str(self.top)} center')
        self.top.resizable(False, False)

        self.read_config()

    def change_state_presuf(self):
        global filtra_presuf_in
        filtra_presuf_in = not filtra_presuf_in

    def read_config(self):
        conf.read('config.ini')
        if 'PALAVRAS.IN' in conf.sections():
            if conf['PALAVRAS.IN']['filtra_presuf_in'] == 'True':
                self.filtra_presuf_in.set(True)
                filtra_presuf_in = True
            else:
                self.filtra_presuf_in.set(False)
                filtra_presuf_in = False

    def grava(self):
        conf['PALAVRAS.IN'] = {
            'palavras': conf['PALAVRAS.IN']['palavras'],
            'status': conf['PALAVRAS.IN']['status'],
            'filtra_presuf_in': filtra_presuf_in
        }

        conf['PALAVRAS.OUT'] = {
            'palavras': conf['PALAVRAS.OUT']['palavras'],
            'status': conf['PALAVRAS.OUT']['status']
        }

        with open('config.ini', 'w') as file:
            conf.write(file)

        self.top.destroy()

filtra_presuf_in = False

root = Tk()

img = PhotoImage(file="./assets/loguinho_caneta.png")

root.iconphoto(False, img)

conf = ConfigParser()

a = FiltroGUI(root)

root.title("Filtro de emails")
root.geometry("300x220")
root.eval("tk::PlaceWindow . center")
root.resizable(False, False)




root.mainloop()