from tkinter import *
from tkinter import filedialog
from lxml import etree
from datetime import datetime

def processar_xml(arquivo_xml):
    """Processa o arquivo XML e retorna os dados formatados"""
    try:
        tree = etree.parse(arquivo_xml)
        root = tree.getroot()
        ns = {'ns': 'http://www.portalfiscal.inf.br/nfe'}
        
        # Extração dos dados
        nome_emitente = root.xpath('//ns:emit/ns:xNome/text()', namespaces=ns)[0]
        valor_total = float(root.xpath('//ns:total/ns:ICMSTot/ns:vNF/text()', namespaces=ns)[0])
        data_vencimento = root.xpath('//ns:cobr/ns:dup/ns:dVenc/text()', namespaces=ns)[0]
        
        # Formatação
        valor_formatado = f"R$ {valor_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        data_formatada = datetime.strptime(data_vencimento, "%Y-%m-%d").strftime("%d/%m/%Y")
        
        return {
            'emitente': nome_emitente,
            'valor': valor_formatado,
            'vencimento': data_formatada,
            'status': 'Sucesso'
        }
    except Exception as e:
        return {
            'status': f"Erro ao processar arquivo: {str(e)}"
        }

def selecionar_arquivo():
    """Função chamada quando o botão é pressionado"""
    caminho_arquivo = filedialog.askopenfilename(
        title="Selecione um arquivo XML de NF-e",
        filetypes=(("Arquivos XML", "*.xml"), ("Todos os arquivos", "*.*"))
    )
    
    if caminho_arquivo:
        resultado = processar_xml(caminho_arquivo)
        
        if resultado['status'] == 'Sucesso':
            texto_resposta.config(
                text=f"Emitente: {resultado['emitente']}\n"
                     f"Valor Total: {resultado['valor']}\n"
                     f"Data Vencimento: {resultado['vencimento']}",
                fg="green"  # Texto em verde para sucesso
            )
        else:
            texto_resposta.config(
                text=resultado['status'],
                fg="red"  # Texto em vermelho para erro
            )

# Configuração da interface gráfica
janela = Tk()
janela.title("Processador de NF-e")
janela.minsize(500, 250)

# Estilo
fonte = ("Arial", 10)
janela.option_add("*Font", fonte)

# Widgets
frame = Frame(janela, padx=20, pady=20)
frame.pack(expand=True, fill=BOTH)

Label(frame, text="Processador de Notas Fiscais Eletrônicas", font=("Arial", 12, "bold")).pack(pady=10)

Label(frame, text="Selecione um arquivo XML de NF-e para extrair informações:").pack(pady=5)

botao_selecionar = Button(
    frame,
    text="Selecionar Arquivo XML",
    command=selecionar_arquivo,
    padx=15,
    pady=8,
    bg="#4CAF50",
    fg="white",
    relief=RAISED
)
botao_selecionar.pack(pady=15)

texto_resposta = Label(
    frame,
    text="",
    wraplength=450,
    justify=LEFT,
    font=("Arial", 10),
    padx=10,
    pady=10
)
texto_resposta.pack(fill=X)

# Rodar a aplicação
janela.mainloop()