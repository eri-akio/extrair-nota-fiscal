from tkinter import *
from tkinter import filedialog

def selecionar_arquivo():
    caminho_arquivo = filedialog.askopenfilename(
        title="Selecione um arquivo",
        filetypes=(("Arquivos XML", "*.xml"), ("Todos os arquivos", "*.*"))
    )
    
    if caminho_arquivo:
        texto_resposta.config(text=f"Arquivo selecionado:\n{caminho_arquivo}")

janela = Tk()
janela.title("Processador de NF-e")

janela.minsize(400, 200)

texto = Label(janela, text="Selecione um arquivo XML de NF-e para processar")
texto.pack(pady=10)

botao_selecionar = Button(
    janela, 
    text="Anexar Arquivo", 
    command=selecionar_arquivo,
    padx=20,
    pady=10
)
botao_selecionar.pack(pady=20)

texto_resposta = Label(janela, text="", wraplength=380, justify=LEFT)
texto_resposta.pack(pady=10)

janela.mainloop()