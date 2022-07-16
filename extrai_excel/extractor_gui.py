import os.path
from tkinter import *
from configparser import ConfigParser

def execute():
    pass

def change_state_in(event=None):
    global aplica_filtros_in
    if palavras_in_entry['state'] == 'disabled':
        palavras_in_entry['state'] = 'normal'
        aplica_filtros_in = True
    else:
        palavras_in_entry['state'] = 'disabled'
        aplica_filtros_in = False

def change_state_out(event=None):
    global aplica_filtros_out
    if palavras_out_entry['state'] == 'disabled':
        palavras_out_entry['state'] = 'normal'
        aplica_filtros_out = True
    else:
        palavras_out_entry['state'] = 'disabled'
        aplica_filtros_out = False

def write_config():
    conf['PALAVRAS.IN'] = {
        'palavras': palavras_in_entry.get(),
        'status': filtra_in_check.get()
    }
    conf['PALAVRAS.OUT'] = {
        'palavras': palavras_out_entry.get(),
        'status': filtra_out_check.get()
    }

    with open('config.ini', 'w') as file:
        conf.write(file)

def read_config():
    global aplica_filtros_in
    global aplica_filtros_out

    conf.read('config.ini')
    if 'PALAVRAS.IN' in conf.sections():
        if conf['PALAVRAS.IN']['status'] == 'True':
            filtra_in_check.set(True)
        else:
            filtra_in_check.set(False)

        palavras_in_entry.insert(0, conf['PALAVRAS.IN']['palavras'])

    if 'PALAVRAS.OUT' in conf.sections():
        if conf['PALAVRAS.OUT']['status'] == 'True':
            filtra_out_check.set(True)
        else:
            filtra_out_check.set(False)

        palavras_out_entry.insert(0, conf['PALAVRAS.OUT']['palavras'])

    if filtra_in_check.get():
        palavras_in_entry['state'] = 'normal'
        aplica_filtros_in = True
    else:
        palavras_in_entry['state'] = 'disabled'
        aplica_filtros_in = False

    if filtra_out_check.get():
        palavras_out_entry['state'] = 'normal'
        aplica_filtros_out = True
    else:
        palavras_out_entry['state'] = 'disabled'
        aplica_filtros_out = False

app = Tk()



conf = ConfigParser()

title_text = StringVar(app)
title_label = Label(app, textvariable=title_text, font=("Arial", 14))
title_text.set("Gerador de relatórios")
title_label.grid(row=0, column=0, sticky=W, pady=10, padx=60)

grava_database = BooleanVar(app)
check_database = Checkbutton(app, text='Filtra por período', variable=grava_database)
check_database.grid(row=1, column=0, sticky=W, pady=10, padx=25)

palavras_in_entry_text =StringVar(app)
palavras_in_entry = Entry(app, textvariable=palavras_in_entry_text, width=15)
palavras_in_entry.grid(row=2, column=0, sticky=W, pady=5, padx=32)


# palavras_out_label = Label(app, text="Palavras OUT:  ")
# palavras_out_label.grid(row=3, column=0, sticky=W, pady=5, padx=10)

palavras_out_entry_text =StringVar(app)
palavras_out_entry = Entry(app, textvariable=palavras_out_entry_text, width=15)
palavras_out_entry.grid(row=2, sticky=W, pady=5, padx=165)

execute_btn = Button(app, text="Executar", command=lambda : execute())
execute_btn.grid(row=4, column=0, columnspan=3, sticky=W, pady=30, ipady=8, ipadx=10, padx=105)

if os.path.exists('config.ini'):
    read_config()
else:
    grava_database.set(True)
app.title("Gerador de relatórios")
app.geometry("300x220")
app.eval("tk::PlaceWindow . center")
app.resizable(False, False)
app.mainloop()