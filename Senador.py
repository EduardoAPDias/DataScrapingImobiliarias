from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import time
import re

#clicar no veja mais 5 vezes
def carregar_mais(page, num_clicks=5):
    for _ in range(num_clicks):
        try:
            
            # Clique no botão "mostrar mais"
            button = page.locator('xpath=/html/body/div[4]/section[1]/div/div/div/div/div[1]/div[2]/div[2]/div[2]/div/div/div/button')
            button.click()
            time.sleep(2)
        
        except Exception as e:
            print(f"Erro ao clicar no botão 'mostrar mais': {e}")
            break

def collect_data(url):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)        
        
        carregar_mais(page)
        
        # Coletar o conteúdo da página após todos os cliques
        page_content = page.content()
        browser.close()

    #Coletar os dados da classe
    sp = BeautifulSoup(page_content, 'html.parser')
    contents = sp.find_all(class_='card-with-buttons__footer')

    data = []
    for content in contents:
        edificio = content.find(class_='card-with-buttons__condo')
        endereco = content.find(class_='card-with-buttons__heading')
        ul_items = content.find('ul')
        preco = content.find(class_='card-with-buttons__value')

        #pegar texto
        if edificio and endereco and ul_items and preco:
            edificio_text = edificio.get_text(strip=True)
            endereco_text = re.sub(r'\s+', ' ', endereco.get_text(separator=' ', strip=True))
            preco_text = preco.get_text(strip=True)
            
            # Formatar o texto
            li_items = ul_items.find_all('li')
            area_text = re.sub(r'[^\d.]', '', li_items[0].get_text(strip=True)) if len(li_items) > 0 else ''
            quartos_text = re.sub(r'[^\d]', '', li_items[1].get_text(strip=True)) if len(li_items) > 1 else ''
            suite_text = re.sub(r'[^\d]', '', li_items[2].get_text(strip=True)) if len(li_items) > 2 else ''
            banheiros_text = re.sub(r'[^\d]', '', li_items[3].get_text(strip=True)) if len(li_items) > 3 else ''
            vagas_text = re.sub(r'[^\d]', '', li_items[4].get_text(strip=True)) if len(li_items) > 4 else ''
            preco_text = re.sub(r'[^\d,]', '', preco_text).replace(',', '.')
            
            # Append
            data.append({
                "edificio": edificio_text,
                "endereco": endereco_text,
                "area": area_text,
                "quartos": quartos_text,
                "banheiros": banheiros_text,
                "suite": suite_text,
                "vagas": vagas_text,
                "preco": preco_text,
                "imobiliaria": "Senador"
            })
    return data


# Exemplo de uso
url = 'https://www.imobiliariasenador.com.br/imoveis/para-alugar/apartamento/londrina?finalidade=residencial'
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