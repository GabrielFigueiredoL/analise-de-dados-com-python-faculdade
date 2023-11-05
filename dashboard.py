import streamlit as st
import pandas as pd
import plotly.express as px
import json

st.set_page_config(layout='wide')

#Configuração do JSON para dataFrame
with open('data.json', 'r', encoding='utf-8') as file:
    data = file.read()
    
data_dict = json.loads(data)
df = pd.DataFrame(data_dict['data'])

df['selectedDate'] = pd.to_datetime(df['selectedDate'], format='%d/%m/%Y')
df=df.sort_values('selectedDate')

df['Month'] = df['selectedDate'].apply(lambda x: str(x.month) + "/" + str(x.year))
month = st.sidebar.selectbox("Mês", df['Month'].unique())


df_filtered = df[df['Month'] == month]

col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

fig_date = px.bar(df_filtered, title='Faturamento por Dia', x="selectedDate", y="finalValue", labels={'selectedDate': 'Data', 'finalValue': 'Faturamento (R$)'})
col1.plotly_chart(fig_date)

sales_per_day = df_filtered['selectedDate'].value_counts().sort_index()
fig_sales_per_day = px.bar(x=sales_per_day.index, y=sales_per_day.values, labels={'x': 'Data', 'y': 'Vendas'}, title='Vendas por Dia')
col2.plotly_chart(fig_sales_per_day)

items_data = df.explode('selectedItems')
items_data['qtd'] = items_data['selectedItems'].apply(lambda x: int(x['qtd']))
items_data['item_name'] = items_data['selectedItems'].apply(lambda x: x['item']['name'])

items_data_filtered = items_data[items_data['Month'] == month]

# Criar um DataFrame para contagem real de itens por dia
items_data_filtered['total_count'] = items_data_filtered['qtd']  # Renomear para melhor clareza

# Agrupar por data e item_name e multiplicar a quantidade do item pelo total_count
item_counts_per_day_real = items_data_filtered.groupby(['selectedDate', 'item_name'])['total_count'].sum().reset_index()

# Criar o gráfico de barras para cada dia com os respectivos itens e suas contagens reais
fig_item_counts_per_day_real = px.bar(item_counts_per_day_real, x='selectedDate', y='total_count', color='item_name',
                                      labels={'selectedDate': 'Data', 'total_count': 'Contagem', 'item_name': 'Item'},
                                      title='Contagem Real de Itens por Dia')

col3.plotly_chart(fig_item_counts_per_day_real)





