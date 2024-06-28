from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import time
import re

def carregar_mais(page, num_clicks=5):
    for _ in range(num_clicks):
        try:
            page.locator('xpath=/html/body/div/main/div[3]/section/div[5]/div[4]/button').click()
            time.sleep(1)
        except Exception as e:
            print(f"Erro ao clicar no botão 'veja mais': {e}")
            break

def collect_data(url):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)
        
        # Clicar no botão "veja mais" antes de coletar os dados
        carregar_mais(page)
        
        # Coletar o conteúdo da página após todos os cliques
        page_content = page.content()
        browser.close()

    # Processar o conteúdo da página com BeautifulSoup
    sp = BeautifulSoup(page_content, 'html.parser')
    contents = sp.find_all(class_='list__description jetgrid jetgrid--align-content-between')

    data = []
    for content in contents:
        edificio = content.find(class_='list__building')
        endereco = content.find(class_='list__address')
        items = content.find_all(class_='list__item')
        preco = content.find(class_='ui__text--green')

        # Pegar texto
        if edificio and endereco and items and preco:
            edificio_text = edificio.get_text(strip=True)
            endereco_text = re.sub(r'\s+', ' ', endereco.get_text(separator=' ', strip=True))
            preco_text = preco.get_text(strip=True)
            
            # Formatar o texto
            area_text = re.sub(r'[^\d.]', '', items[0].get_text(strip=True)) if len(items) > 0 else ''
            quartos_text = re.sub(r'[^\d]', '', items[1].get_text(strip=True)) if len(items) > 1 else ''
            vagas_text = re.sub(r'[^\d]', '', items[2].get_text(strip=True)) if len(items) > 2 else ''
            preco_text = re.sub(r'[^\d,]', '', preco_text).replace(',', '.')
            
            # Append
            data.append({
                "edificio": edificio_text,
                "endereco": endereco_text,
                "area": area_text,
                "quartos": quartos_text,
                "suite": "0",
                "banheiros": "0",
                "vagas": vagas_text,
                "preco": preco_text,
                "imobiliaria": "Veneza"
            })

    return data

# Exemplo de uso
url = 'https://www.veneza.com.br/imoveis/apartamento-alugar'
data = collect_data(url)

for item in data:
    print("Edifício:", item['edificio'])
    print("Endereço:", item['endereco'])
    print("Área:", item['area'])
    print("Quartos:", item['quartos'])
    print("Banheiros:", item['banheiros'])
    print("Suíte:", item['suite'])
    print("Vagas:", item['vagas'])
    print("Preço:", item['preco'])
    print("Imobiliária:", item['imobiliaria'])
    print('-' * 40)