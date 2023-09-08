import numpy as np
from scipy import stats
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os

plt.rcParams.update({
        'font.size': 14,
        'axes.titlesize': 15,
        'axes.labelsize': 15,
        'xtick.labelsize': 15,
        'ytick.labelsize': 15,
        'font.size': 13,
        'figure.figsize': (8, 6),
        'axes.grid': True,
        'grid.linestyle': '-',
        'grid.alpha': 0.3,
        'lines.markersize': 5.0,
        'xtick.minor.visible': True,
        'xtick.direction': 'in',
        'xtick.major.size': 20.0,
        'xtick.minor.size': 10.0,
        'xtick.top': False,
        'xtick.bottom': True,
        'ytick.minor.visible': True,
        'ytick.direction': 'in',
        'ytick.major.size': 12.0,
        'ytick.minor.size': 6.0,
        'ytick.right': True,
        'errorbar.capsize': 0.0,
    })

import warnings
warnings.filterwarnings('ignore')
import streamlit as st

# Подгружаем заранее поготовленные данные
df_client = pd.read_csv('datasets/clients_info.csv')

# Заголовок
st.title('Предложение новой услуги клиентам банка')

st.header('Классификация клиентов на основе вероятности принять предложение')

st.markdown("Табличка с данными о клиентах")
st.table(df_client.head(10))

st.markdown("Изучить распределение предикторов")

# Select box
cols_to_not_show = ['REG_ADDRESS_PROVINCE', 'FACT_ADDRESS_PROVINCE', 'ID_CLIENT', 'AGREEMENT_RK']
option = st.selectbox(
     'Выберете предиктор, чтобы посмотреть его распределение',
     tuple(df_client.columns.drop(cols_to_not_show))
     )
st.write('Вы выбрали:', option)

with st.spinner('загрузка гистграммы...'):
	fig, ax = plt.subplots()
	ax.set(ylabel='Count', title='Histogram')
	discrete = True
	if option == 'PERSONAL_INCOME':
		discrete = False
	sns.histplot(data=df_client,
			     x=option,
			     hue="TARGET",
			     multiple="layer",
			     ax=ax,
			     discrete=discrete)
	if option == 'MARITAL_STATUS':
		plt.xticks(rotation=60)
	st.pyplot(fig)


st.markdown("Изучить корреляцию между признаками (а также целевой переменной TARGET), выберите 2 и более признака")

#choice = ['TARGET']
choice = st.multiselect("Выберите признаки", list(df_client.columns.drop(cols_to_not_show)))

with st.spinner('загрузка матрицы корреляции...'):
	if len(choice) > 1:
		fig, ax = plt.subplots(figsize=(10, 8))
		df_corr = df_client[choice]
		sns.heatmap(df_corr.corr(method='spearman'),
					annot=True,
					ax=ax,
					cmap='Blues')
		plt.title('Spearman correlation matrix')
		plt.show()
		st.pyplot(fig)
	else:
		st.markdown("Выберите больше признаков для построения матрицы корреляции")