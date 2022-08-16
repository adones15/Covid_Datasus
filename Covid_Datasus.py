#!/usr/bin/env python
# coding: utf-8

# In[8]:


#importando asbibliotecas necessárias
import requests
import rarfile
import io
import warnings
import json
import pandas as pd
import shutil
import os, stat
import sqlalchemy as sq
import pymysql
from datetime import date
import time


# In[11]:


#removendo o diretório antigo do dia anterior para criarmos o novo diretório do dia atual
def remove_readonly(func, path, _):
    os.chmod(path, stat.S_IWRITE)
    func(path)

shutil.rmtree(r"C:\Users\win\Notebooks\Pessoal\Covid\covid_csvs", onerror=remove_readonly)


# In[41]:


#obtendo a URL atual
url = "https://qd28tcd6b5.execute-api.sa-east-1.amazonaws.com/prod/PortalGeral"
head = {"X-Parse-Application-Id": "unAFkcaNDeXajurGB7LChj8SgQYS2ptm"}
req = requests.get(url, headers=head)
c_json = json.loads(req.content)
url2 = c_json["results"][0]["arquivo"]["url"]
m = url2[136:139]


# In[42]:


#descompactando os arquivos
warnings.filterwarnings('ignore')
response = requests.get(url2, verify = False, stream = True)
file = rarfile.RarFile(io.BytesIO(response.content))
file.extractall(r"C:\Users\win\Notebooks\Pessoal\Covid\covid_csvs")


# In[72]:


#Obtendo os valores referente as datas
d_h = date.today().strftime("%d/%m/%Y")#verificar sabado domingo e feriado
dia = int(d_h[0:2])
mes = d_h[3:5]
ano = d_h[6:10]


# In[73]:


#Tratando sábado e domingo
DIAS = ['Segunda-feira','Terça-feira','Quarta-feira','Quinta-Feira','Sexta-feira','Sábado','Domingo']
data = date.today()
dia_v = 0
i_semana = data.weekday()
d_semana = DIAS[i_semana]
if d_semana == "Sábado":
    dia_v = dia - 1
elif d_semana == "Domingo":
    dia_v = dia - 2
else:
    dia_v = dia


# In[74]:


#carregando os csv's extraidos
csv20p1 = pd.read_csv(fr"C:\Users\win\Notebooks\Pessoal\Covid\covid_csvs\HIST_PAINEL_COVIDBR_2020_Parte1_{dia_v-1}{m}{ano}.csv", encoding='utf-8', sep=';')
csv20p2 = pd.read_csv(fr"C:\Users\win\Notebooks\Pessoal\Covid\covid_csvs\HIST_PAINEL_COVIDBR_2020_Parte2_{dia_v-1}{m}{ano}.csv", encoding='utf-8', sep=';')
csv21p1 = pd.read_csv(fr"C:\Users\win\Notebooks\Pessoal\Covid\covid_csvs\HIST_PAINEL_COVIDBR_2021_Parte1_{dia_v-1}{m}{ano}.csv", encoding='utf-8', sep=';')
csv21p2 = pd.read_csv(fr"C:\Users\win\Notebooks\Pessoal\Covid\covid_csvs\HIST_PAINEL_COVIDBR_2021_Parte2_{dia_v-1}{m}{ano}.csv", encoding='utf-8', sep=';')
csv22p1 = pd.read_csv(fr"C:\Users\win\Notebooks\Pessoal\Covid\covid_csvs\HIST_PAINEL_COVIDBR_2022_Parte1_{dia_v-1}{m}{ano}.csv", encoding='utf-8', sep=';')
csv22p2 = pd.read_csv(fr"C:\Users\win\Notebooks\Pessoal\Covid\covid_csvs\HIST_PAINEL_COVIDBR_2022_Parte2_{dia_v-1}{m}{ano}.csv", encoding='utf-8', sep=';')


# In[45]:


#juntando todos os df's em um só
dff = pd.concat([csv20p1, csv20p2, csv21p1, csv21p2, csv22p1, csv22p2])


# In[48]:


#excluindo algumas colunas que não tem muita relevância
dff.drop(columns=["coduf","codmun", "codRegiaoSaude", "nomeRegiaoSaude", "interior/metropolitana",
                 "Recuperadosnovos", "emAcompanhamentoNovos"], inplace=True)


# In[50]:


#enviando os dados do df para o mysql
con = sq.create_engine(f"mysql+pymysql://root:{senha}a@localhost/{schema}")
dff.to_sql("covid_data", con, if_exists="replace", index=False)

