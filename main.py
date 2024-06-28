import Veneza
import Inglaterra
import Senador
import database 
from dotenv import load_dotenv
import analise

# Carregar variáveis do arquivo .env
load_dotenv()

# URLs das imobiliárias
urls = {
    "Veneza" : 'https://www.veneza.com.br/imoveis/apartamento-alugar',
    "Inglaterra" : 'https://www.imobiliariainglaterra.com.br/imoveis/para-alugar/apartamento/londrina?finalidade=residencial',
    "Senador" : 'https://www.imobiliariasenador.com.br/imoveis/para-alugar/apartamento/londrina?finalidade=residencial'
}

# Criar o banco de dados se ainda não existir
database.create_db()

# Iterar sobre cada imobiliária e coletar os dados
for imobiliaria, url in urls.items():
    if imobiliaria == "Veneza":
        data = Veneza.collect_data(url)
    elif imobiliaria == "Inglaterra":
        data = Inglaterra.collect_data(url)
    elif imobiliaria == "Senador":
        data = Senador.collect_data(url)

    # Inserir os dados coletados no banco de dados
    for item in data:
        print("Edifício:", item['edificio'])
        print("Endereço:", item['endereco'])
        print("Items:", f"{item['area']}, {item['quartos']}, {item['suite']}, {item['banheiros']}, {item['vagas']}")
        print("Preço:", item['preco'])
        print("Imobiliária:", item['imobiliaria'])
        print('-' * 40)
        
        # Inserir no banco de dados
        database.insert_data(
            item['edificio'], 
            item['endereco'], 
            item['area'], 
            item['quartos'],
            item['suite'],
            item['banheiros'], 
            item['vagas'],
            item['preco'],
            item['imobiliaria']
        )

#analise.run_analysis()