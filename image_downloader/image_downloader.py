import pandas as pd
import requests
import re
from tkinter import *
from tkinter import filedialog
import threading

def make_download():
    if file_text_entry.get() == "" or column_text_entry.get() == "":
        return

    tocaobra_df = pd.read_excel(file_text_entry.get())


    # imagens_df = tocaobra_df[['COD TOCA OBRA', 'NOME DO PRODUTO', 'IMAGEM PRODUTO_y']].values.tolist()
    imagens_df = tocaobra_df[['COD TOCA OBRA', 'NOME DO PRODUTO', column_text_entry.get()]].values.tolist()

    i = 0
    for img in imagens_df:
        try:
            img[1] = re.sub('[^a-zA-Z0-9 \n\.]', '', img[1])

            with open(f"./imagens/{i}_{img[0]}_{img[1]}.jpg", "wb") as file:
                resp = requests.get(img[-1], stream=True)

                if not resp.ok:
                    print(resp)

                for block in resp.iter_content(1024):
                    if not block:
                        break

                    file.write(block)
        except Exception as e:
            print("Não foi possível baixar a imagem.")
            print(e)
            print('\"' in img[1])
            print(f"Imagem: {img[-1]}")

def choose_file():
    global file_path
    file_path = filedialog.askopenfilename()
    file_text_entry.delete(0, END)
    file_text_entry.insert(0, file_path)
    return file_path

def start_thread_download(event):
    global th
    th = threading.Thread(target=make_download, daemon=True)
    th.start()

    app.after(10, check_execucao_thread)

def check_execucao_thread():
    if th.is_alive():
        app.after(10, check_execucao_thread)


app = Tk()

# Label escolher arquivo
file_label = Label(app, text="Escolha o arquivo")
file_label.grid(row=0, column=0, sticky=W, padx=10)

# Edit escolher arquivo
file_text =StringVar(app)
file_text_entry = Entry(app, textvariable=file_text, width=36)
file_text_entry.grid(row=1, column=0, padx=10, pady=10)

# Botão para abrir o popup para que seja escolhido o arquivo
choose_file_btn = Button(app, text="Abrir", command=choose_file)
choose_file_btn.grid(row=1, column=1)


# Nome da coluna de imagens
column_label_images = Label(app, text="Nome da coluna")
column_label_images.grid(row=2, column=0, sticky=W, padx=10)

column_text_images = StringVar(app)
column_text_entry = Entry(app, textvariable=column_text_images, width=36)
column_text_entry.grid(row=3, column=0, pady=10, padx=10)


# botão executar
execute_btn = Button(app, text="Executar", command=lambda: start_thread_download(None))
execute_btn.grid(row=4, column=1, sticky=SE, pady=10)

app.title("Redepro - Image Downloader")
app.geometry("300x200")
app.eval("tk::PlaceWindow . center")
app.resizable(False, False)
app.mainloop()