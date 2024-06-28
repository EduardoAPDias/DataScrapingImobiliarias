import pandas as pd
import matplotlib.pyplot as plt
import database

# Buscar dados do banco de dados
def fetch_data():
    return database.fetch_data()

# Criar DataFrame com os dados do banco
data = fetch_data()
df = pd.DataFrame(data)

# Remover linhas com valores de preço inválidos (None)
df = df.dropna(subset=['preco'])

# Remover um apartamento com preço específico(estava com preço de compra)
df = df[df['preco'] != 115000.00]

# Verificar se a coluna 'quartos' contém strings válidas antes de extrair números
df['quartos'] = df['quartos'].astype(str)  # Converter para string se não for

# Extrair número de quartos
df['quartos'] = df['quartos'].str.extract('(\d+)').astype(float)

# Converter área para float
df['area'] = df['area'].astype(float)

# Relatório simples
print("Relatório Simples")
print("=================")

# Número total de dados coletados
num_dados_coletados = len(df)
print(f"\nNúmero total de dados coletados: {num_dados_coletados}")

# Imobiliária que mais apareceu
imobiliaria_mais_frequente = df['imobiliaria'].value_counts().idxmax()
print(f"\nImobiliária que mais apareceu: {imobiliaria_mais_frequente}")

print("\nEstatísticas Descritivas:")
print(df.describe())

print("\nNúmero de apartamentos por número de quartos:")
print(df['quartos'].value_counts())

# Gráfico de pizza do número de quartos
plt.figure(figsize=(10, 6))
quartos_counts = df['quartos'].value_counts().sort_index()
plt.pie(quartos_counts, labels=quartos_counts.index, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
plt.title('Distribuição do Número de Quartos')
plt.axis('equal')
plt.show()

# Gráfico de barras da média de preços por número de quartos
plt.figure(figsize=(10, 6))
df.groupby('quartos')['preco'].mean().plot(kind='bar', color='skyblue', edgecolor='black')
plt.title('Média de Preço por Número de Quartos')
plt.xlabel('Número de Quartos')
plt.ylabel('Média de Preço')
plt.grid(True)
plt.show()

# Gráfico de barras da média do preço por m²
plt.figure(figsize=(10, 6))
df['preco_por_m2'] = df['preco'] / df['area']
df.groupby('quartos')['preco_por_m2'].mean().plot(kind='bar', color='lightgreen', edgecolor='black')
plt.title('Média do Preço por m² por Número de Quartos')
plt.xlabel('Número de Quartos')
plt.ylabel('Média do Preço por m²')
plt.grid(True)
plt.show()

# Boxplot das estatísticas descritivas
plt.figure(figsize=(15, 10))
df.boxplot(column=['area', 'quartos', 'suite', 'banheiros', 'vagas', 'preco'])
plt.title('Boxplot das Estatísticas Descritivas')
plt.ylabel('Valor')
plt.grid(True)
plt.show()

# Histogramas de área e preço
fig, axs = plt.subplots(1, 2, figsize=(15, 5))

# Histograma da área
axs[0].hist(df['area'], bins=20, color='skyblue', edgecolor='black')
axs[0].set_title('Distribuição da Área')
axs[0].set_xlabel('Área')
axs[0].set_ylabel('Frequência')

# Histograma do preço
axs[1].hist(df['preco'], bins=20, color='lightgreen', edgecolor='black')
axs[1].set_title('Distribuição do Preço')
axs[1].set_xlabel('Preço')
axs[1].set_ylabel('Frequência')

plt.tight_layout()
plt.show()
