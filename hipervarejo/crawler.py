import requests
from bs4 import BeautifulSoup
from utils.pysheets import Sheets

url_busca = 'https://www.hipervarejo.com.br/buscapagina'
url_details_produto = 'https://www.hipervarejo.com.br/api/catalog_system/pub/products/search/'

def map_urls_categorias():
    lista_codigo_categorias = [
        '11',
        '1',
        '72',
        '73',
        '74'
    ]

    lista_codigo_temp = [
        '11'
    ]
    page = 1

    for codigo in lista_codigo_temp:
        params = {
            'fq': 'C:/' + codigo + '/',
            'PS': '36',
            'sl': 'b6a75bf1-9f02-484a-ae09-f8010835d425',
            'cc': '36',
            'sm': '0',
            'PageNumber': str(page)
        }

        go_to_url_categoria(params)


def go_to_url_categoria(params):
    response = requests.get(url_busca, params=params)

    soup = BeautifulSoup(response.text, 'html.parser')

    links = soup.find_all('a', class_='product-item__img')

    for link in links:
        go_to_url_produto(link['href'])

def go_to_url_produto(url):
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    produto_id = soup.find('input', {'id': '___rc-p-id'})['value']

    get_details_produto(produto_id)

def get_details_produto(produto_id):
    params = {
        'fq': 'productId:' + produto_id
    }
    response = requests.get(url_details_produto, params=params)

    product_detail = response.json()

    codigo_produto = product_detail[0]['productReference']

    nome_produto = product_detail[0]['productName']

    preco_produto = product_detail[0]['items'][0]['sellers'][0]['commertialOffer']['ListPrice']

    categorias_produto = product_detail[0]['categories'][0].replace('/', ' > ')[3:-3]

    especificacoes_produto = product_detail[0]['Especificações']

    keys_produto_details = product_detail[0].keys()
    especs = ''

    for key in keys_produto_details:
        if key in especificacoes_produto:
            especs += key + ': '
            for espec in product_detail[0][key]:
                especs += espec + ','

            especs = especs[:-1]
            especs += '\n'

    lista_veiculos_compativeis_produto = ''

    if 'Modelo' in keys_produto_details:
        lista_veiculos_compativeis_produto = product_detail[0]['Modelo']


    print({
        'codigo_produto': codigo_produto,
        'nome_produto': nome_produto,
        'preco_produto': preco_produto,
        'categorias_produto': categorias_produto,
        'especificacoes_produto': especificacoes_produto,
        'especificacoes': especs,
        'veiculos_compativeis': lista_veiculos_compativeis_produto
    })

    my_sheet.save_content(
        cod_produto=codigo_produto,
        nome_produto=nome_produto,
        preco_produto=preco_produto,
        categorias_produto=categorias_produto,
        especificacoes=especs,
        veiculos_compativeis=str(lista_veiculos_compativeis_produto)
    )

columns = ['CÓDIGO', 'NOME DO PRODUTO', 'PREÇO DO PRODUTO', 'CATEGORIAS', 'ESPECIFICAÇÕES', 'VEÍCULOS COMPATÍVEIS']

my_sheet = Sheets(output_folder='./saida', filename='output.xlsx', fieldlist=columns)

map_urls_categorias()