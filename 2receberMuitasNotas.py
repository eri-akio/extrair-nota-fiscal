from lxml import etree
from datetime import datetime
import os

# Configurações
diretorio = "./xmls"  # Pasta contendo os XMLs
ns = {'ns': 'http://www.portalfiscal.inf.br/nfe'}

def processar_xml(arquivo_xml):
    """Processa um único arquivo XML e retorna os dados"""
    try:
        tree = etree.parse(arquivo_xml)
        root = tree.getroot()
        
        dados = {
            'emitente': root.xpath('//ns:emit/ns:xNome/text()', namespaces=ns)[0],
            'valor': float(root.xpath('//ns:total/ns:ICMSTot/ns:vNF/text()', namespaces=ns)[0]),
            'vencimento': datetime.strptime(
                root.xpath('//ns:cobr/ns:dup/ns:dVenc/text()', namespaces=ns)[0], 
                "%Y-%m-%d"
            ).strftime("%d/%m/%Y")
        }
        return dados
    
    except Exception as e:
        print(f"Erro ao processar {arquivo_xml}: {str(e)}")
        return None

# Lista e processa todos os XMLs no diretório
resultados = []
for arquivo in os.listdir(diretorio):
    if arquivo.lower().endswith('.xml'):
        caminho = os.path.join(diretorio, arquivo)
        dados = processar_xml(caminho)
        if dados:
            resultados.append(dados)

# Exibir resultados consolidados
print("\nRESULTADO DA CONSOLIDAÇÃO:")
print("-" * 50)
for i, nota in enumerate(resultados, start=1):
    print(f"\nNota Fiscal #{i}:")
    print(f"Emitente: {nota['emitente']}")
    print(f"Valor: R$ {nota['valor']:.2f}")
    print(f"Vencimento: {nota['vencimento']}")
print("-" * 50)
print(f"\nTotal de notas processadas: {len(resultados)}")