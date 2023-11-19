import streamlit as st
import pandas as pd
import plotly.express as px
import json

with open('data.json', 'r', encoding='utf-8') as file:
    data = file.read()
    
data_dict = json.loads(data)
df = pd.DataFrame(data_dict['data'])

df['selectedDate'] = pd.to_datetime(df['selectedDate'], format='%d/%m/%Y')
df=df.sort_values('selectedDate')

df['Month'] = df['selectedDate'].apply(lambda x: str(x.month) + "/" + str(x.year))
month = st.sidebar.selectbox("Mês", df['Month'].unique())
df_filtrada = df[df['Month'] == month]


df_filtrada.loc[:, 'finalValue'] = pd.to_numeric(df_filtrada['finalValue'])
total_faturado_por_dia = df_filtrada.groupby('selectedDate')['finalValue'].sum().reset_index()

fig_date = px.bar(total_faturado_por_dia, title='Faturamento por Dia', x="selectedDate", y="finalValue",
                              labels={'selectedDate': 'Data', 'finalValue': 'Faturamento (R$)'})

st.plotly_chart(fig_date)


vendas_por_dia = df_filtrada['selectedDate'].value_counts().sort_index()
fig_vendas_por_dia = px.bar(x=vendas_por_dia.index, y=vendas_por_dia.values, labels={'x': 'Data', 'y': 'Vendas'}, title='Vendas por Dia')
st.plotly_chart(fig_vendas_por_dia)


items_data = df.explode('selectedItems')
items_data['qtd'] = items_data['selectedItems'].apply(lambda x: int(x['qtd']))
items_data['item_name'] = items_data['selectedItems'].apply(lambda x: x['item']['name'])

items_data_filtrado = items_data[items_data['Month'] == month]

items_data_filtrado['total_count'] = items_data_filtrado['qtd']

itens_por_dia = items_data_filtrado.groupby(['selectedDate', 'item_name'])['total_count'].sum().reset_index()

fig_itens_por_dia = px.bar(itens_por_dia, x='selectedDate', y='total_count', color='item_name',
                                      labels={'selectedDate': 'Data', 'total_count': 'Contagem', 'item_name': 'Item'},
                                      title='Contagem de Itens Vendidos por Dia')

st.plotly_chart(fig_itens_por_dia)

contagem_total_itens = items_data_filtrado.groupby('item_name')['qtd'].sum()
most_sold_item_total = contagem_total_itens.idxmax()
least_sold_item_total = contagem_total_itens.idxmin()
most_sold_quantity_total = contagem_total_itens.max()
least_sold_quantity_total = contagem_total_itens.min()

items_data_filtrado['total_value'] = pd.to_numeric(items_data_filtrado['qtd']) * items_data_filtrado['selectedItems'].apply(
    lambda x: pd.to_numeric(x['item']['value']))
venda_de_itens = items_data_filtrado.groupby('item_name')['total_value'].sum()
mais_vendido = venda_de_itens.idxmax()
menos_vendido = venda_de_itens.idxmin()
mais_faturamento = venda_de_itens.max()
menos_faturamento = venda_de_itens.min()

st.subheader("Itens Mais e Menos Vendidos")
tabela_vendas = pd.DataFrame({
    'Item': [most_sold_item_total, least_sold_item_total],
    'Quantidade': [most_sold_quantity_total, least_sold_quantity_total]
})
st.table(tabela_vendas)

st.subheader("Itens que Mais e Menos Faturaram")
tabela_faturamento = pd.DataFrame({
    'Item': [mais_vendido, menos_vendido],
    'Faturamento (R$)': [mais_faturamento, menos_faturamento]
})
st.table(tabela_faturamento)