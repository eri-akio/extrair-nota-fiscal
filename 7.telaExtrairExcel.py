from tkinter import *
from tkinter import filedialog, messagebox
from lxml import etree
from datetime import datetime
from openpyxl import Workbook
from openpyxl.styles import Font
import os
import locale

# Configuração do locale para formatação brasileira
try:
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
except:
    locale.setlocale(locale.LC_ALL, 'Portuguese_Brazil.1252')

class NFeProcessor:
    def __init__(self, master):
        self.master = master
        self.master.title("Processador de NF-e")
        self.master.minsize(600, 400)

        # Variáveis
        self.arquivos_selecionados = []
        self.ns = {'ns': 'http://www.portalfiscal.inf.br/nfe'}
        
        # Interface
        self.criar_interface()
    
    def criar_interface(self):
        # Frame principal
        main_frame = Frame(self.master, padx=20, pady=20)
        main_frame.pack(expand=True, fill=BOTH)
        
        # Título
        Label(main_frame, 
              text="Processador de Notas Fiscais", 
              font=("Arial", 14, "bold")).pack(pady=10)
        
        # Frame de seleção
        select_frame = Frame(main_frame)
        select_frame.pack(fill=X, pady=10)
        
        # Botão para adicionar arquivos
        Button(select_frame, 
               text="Adicionar Arquivos XML", 
               command=self.adicionar_arquivos,
               padx=15, pady=8,
               bg="#4CAF50", fg="white").pack(side=LEFT, padx=5)
        
        # Botão para processar
        Button(select_frame, 
               text="Processar e Gerar Excel", 
               command=self.processar_e_gerar_excel,
               padx=15, pady=8,
               bg="#2196F3", fg="white").pack(side=LEFT, padx=5)
        
        # Lista de arquivos
        self.lista_arquivos = Listbox(main_frame, 
                                    height=8,
                                    selectmode=MULTIPLE)
        self.lista_arquivos.pack(fill=BOTH, expand=True, pady=10)
        
        # Área de resultados
        self.texto_resultado = Text(main_frame, 
                                  height=10,
                                  wrap=WORD,
                                  state=DISABLED)
        self.texto_resultado.pack(fill=BOTH, expand=True)
        
        # Barra de status
        self.status_bar = Label(main_frame, 
                               text="Pronto para processar arquivos", 
                               bd=1, relief=SUNKEN, anchor=W)
        self.status_bar.pack(fill=X)
    
    def adicionar_arquivos(self):
        arquivos = filedialog.askopenfilenames(
            title="Selecione os arquivos XML de NF-e",
            filetypes=(("Arquivos XML", "*.xml"), ("Todos os arquivos", "*.*"))
        )
        
        if arquivos:
            self.arquivos_selecionados = list(arquivos)
            self.lista_arquivos.delete(0, END)
            for arquivo in self.arquivos_selecionados:
                self.lista_arquivos.insert(END, os.path.basename(arquivo))
            self.atualizar_status(f"{len(self.arquivos_selecionados)} arquivo(s) selecionado(s)")
    
    def processar_e_gerar_excel(self):
        if not self.arquivos_selecionados:
            messagebox.showwarning("Aviso", "Nenhum arquivo selecionado!")
            return
        
        try:
            # Criar Excel
            wb = Workbook()
            ws = wb.active
            ws.title = "NF-e"
            
            # Cabeçalhos
            cabecalhos = ["Emitente", "Vencimento", "Valor", ]
            ws.append(cabecalhos)
            
            # Formatar cabeçalhos
            for col in range(1, len(cabecalhos)+1):
                ws.cell(row=1, column=col).font = Font(bold=True)
            
            # Processar arquivos
            resultados = []
            for arquivo in self.arquivos_selecionados:
                resultado = self.processar_xml(arquivo)
                if resultado and resultado['status'] == 'Sucesso':
                    resultados.append(resultado)
                    ws.append([
                        resultado['emitente'],
                        resultado['vencimento'],
                        resultado['valor']
                    ])
            
            # Ajustar colunas
            for col in ws.columns:
                max_length = max(len(str(cell.value)) for cell in col)
                ws.column_dimensions[col[0].column_letter].width = max_length + 2
            
            # Salvar Excel
            arquivo_excel = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=(("Arquivos Excel", "*.xlsx"),),
                title="Salvar relatório como",
                initialfile="notas_fiscais.xlsx")
            
            if arquivo_excel:
                wb.save(arquivo_excel)
                self.mostrar_resultados(resultados)
                self.atualizar_status(f"Relatório gerado com {len(resultados)} nota(s) processada(s)")
                messagebox.showinfo("Sucesso", f"Arquivo Excel gerado com sucesso!\n{arquivo_excel}")
        
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao processar os arquivos:\n{str(e)}")
            self.atualizar_status("Erro ao processar arquivos")
    
    def processar_xml(self, arquivo_xml):
        try:
            tree = etree.parse(arquivo_xml)
            root = tree.getroot()
            
            # Extrair dados
            emitente = root.xpath('//ns:emit/ns:xNome/text()', namespaces=self.ns)[0]
            vencimento = root.xpath('//ns:cobr/ns:dup/ns:dVenc/text()', namespaces=self.ns)[0]
            valor = float(root.xpath('//ns:total/ns:ICMSTot/ns:vNF/text()', namespaces=self.ns)[0])
            
            # Formatar
            valor_formatado = locale.currency(valor, grouping=True, symbol=True)
            data_formatada = datetime.strptime(vencimento, "%Y-%m-%d").strftime("%d/%m/%Y")
            
            return {
                'emitente': emitente,
                'vencimento': data_formatada,
                'valor': valor_formatado,
                'status': 'Sucesso'
            }
        
        except Exception as e:
            return {
                'arquivo': os.path.basename(arquivo_xml),
                'status': f"Erro: {str(e)}"
            }
    
    def mostrar_resultados(self, resultados):
        self.texto_resultado.config(state=NORMAL)
        self.texto_resultado.delete(1.0, END)
        
        for i, res in enumerate(resultados, 1):
            self.texto_resultado.insert(END, 
                f"NF-e #{i}\n"
                f"Emitente: {res['emitente']}\n"
                f"Vencimento: {res['vencimento']}\n"
                f"Valor: {res['valor']}\n"
                f"{'-'*50}\n"
            )
        
        self.texto_resultado.config(state=DISABLED)
    
    def atualizar_status(self, mensagem):
        self.status_bar.config(text=mensagem)

# Iniciar aplicação
if __name__ == "__main__":
    root = Tk()
    app = NFeProcessor(root)
    root.mainloop()