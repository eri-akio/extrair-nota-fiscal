from tkinter import *
from tkinter import filedialog

def selecionar_arquivo():
    # Abre a janela de seleção de arquivo
    caminho_arquivo = filedialog.askopenfilename(
        title="Selecione um arquivo",
        filetypes=(("Arquivos XML", "*.xml"), ("Todos os arquivos", "*.*"))
    )
    
    if caminho_arquivo:
        texto_resposta.config(text=f"Arquivo selecionado:\n{caminho_arquivo}")
        # Aqui você pode adicionar o código para processar o arquivo selecionado
        # Exemplo: processar_xml(caminho_arquivo)

# Criar a janela principal
janela = Tk()
janela.title("Processador de NF-e")

# Configurar o tamanho mínimo da janela
janela.minsize(400, 200)

# Widgets da interface
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

# Rodar a aplicação
janela.mainloop()