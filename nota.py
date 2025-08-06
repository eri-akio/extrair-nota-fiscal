from lxml import etree
from datetime import datetime 

# Carregar o arquivo XML
xml_file = "nota.xml"
tree = etree.parse(xml_file)
root = tree.getroot()

# Definir o namespace da NF-e
ns = {'ns': 'http://www.portalfiscal.inf.br/nfe'}

# Extrair os dados
nomeEmitente= root.xpath('//ns:emit/ns:xNome/text()', namespaces=ns)[0]
vNF = root.xpath('//ns:total/ns:ICMSTot/ns:vNF/text()', namespaces=ns)[0]
data_venc = root.xpath('//ns:cobr/ns:dup/ns:dVenc/text()', namespaces=ns)[0]

# Converter a data para formato brasileiro
data_br = datetime.strptime(data_venc, "%Y-%m-%d").strftime("%d/%m/%Y")

# Formatar e exibir os resultados
print(f"Nome de FABRICANTE/EMITENTE: {nomeEmitente}")
print(f"Valor total da NF-e (vNF): R$ {float(vNF):.2f}")
print(f"Data de vencimento: {data_br}")