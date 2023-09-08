import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import streamlit as st

if __name__ == "__main__":

	df_dict = {
	    k.split('.')[0]: pd.read_csv('datasets/' + k)
	    for k in os.listdir('datasets/')
	}

	df_loan = df_dict['D_loan'].merge(df_dict['D_close_loan'], on='ID_LOAN', how='left').copy()
	df_loan = df_loan.groupby('ID_CLIENT',as_index=False)\
    	.agg(LOAN_NUM_TOTAL=("CLOSED_FL", 'count'),
        	LOAN_NUM_CLOSED=("CLOSED_FL", 'sum'))

    df_client = df_dict['D_clients'].copy().rename(columns={'ID': 'ID_CLIENT'})
    df_client = df_client.merge(df_dict['D_target'], on='ID_CLIENT', how='right')
	df_client = df_client.merge(df_dict['D_salary'], on='ID_CLIENT', how='right')
	df_client = df_client.merge(df_loan, on='ID_CLIENT', how='right')
	df_client = df_client.drop_duplicates(ignore_index=True)
	education_dict = {'Неполное среднее': 1, 'Среднее': 2, 'Среднее специальное': 3,
	                  'Неоконченное высшее': 4, 'Высшее': 5, 
	                  'Два и более высших образования': 6, 'Ученая степень': 7}

	family_income_dict = {'до 5000 руб.': 1, 'от 5000 до 10000 руб.': 2,
	                      'от 10000 до 20000 руб.': 3, 'от 20000 до 50000 руб.': 4,
	                      'свыше 50000 руб.': 5}

	df_client.EDUCATION = df_client.EDUCATION.replace(education_dict)
	df_client.FAMILY_INCOME = df_client.FAMILY_INCOME.replace(family_income_dict)
	df_client.to_csv('datasets/clients_info.csv', index=False)