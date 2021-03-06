# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/17_ldxr7RBPuLSAcoalsZBYt6xOYSDszR

***Análisis de una molécula mediante Deep Learning***

Instalación de Conda y RDKit
"""

! wget https://repo.anaconda.com/miniconda/Miniconda3-py37_4.8.2-Linux-x86_64.sh
! chmod +x Miniconda3-py37_4.8.2-Linux-x86_64.sh
! bash ./Miniconda3-py37_4.8.2-Linux-x86_64.sh -b -f -p /usr/local
! conda install -c rdkit rdkit -y
import sys
sys.path.append('/usr/local/lib/python3.7/site-packages/')

"""Tomamos la información del posible medicamento de la base de datos de **chMBL** que nos muestra los fármacos estudiados al momento"""

import pandas as pd                        #Llamamos a la librería pandas

df = pd.read_csv('https://raw.githubusercontent.com/dataprofessor/data/master/acetylcholinesterase_03_bioactivity_data_curated.csv')
df

"""Evaluación de la molécula mediante los descriptores de Lipinski"""

#Librerías necesarias
import numpy as np
from rdkit import Chem
from rdkit.Chem import Descriptors, Lipinski

#Cálculo de los descriptores
def lipinski(smiles, verbose=False):

    moldata= []
    for elem in smiles:
        mol=Chem.MolFromSmiles(elem) 
        moldata.append(mol)
       
    baseData= np.arange(1,1)
    i=0  
    for mol in moldata:        
       
        desc_MolWt = Descriptors.MolWt(mol)
        desc_MolLogP = Descriptors.MolLogP(mol)
        desc_NumHDonors = Lipinski.NumHDonors(mol)
        desc_NumHAcceptors = Lipinski.NumHAcceptors(mol)
           
        row = np.array([desc_MolWt,
                        desc_MolLogP,
                        desc_NumHDonors,
                        desc_NumHAcceptors])   
    
        if(i==0):
            baseData=row
        else:
            baseData=np.vstack([baseData, row])
        i=i+1      
    
    columnNames=["MW","LogP","NumHDonors","NumHAcceptors"]   
    descriptors = pd.DataFrame(data=baseData,columns=columnNames)
    
    return descriptors

df_lipinski = lipinski(df['canonical_smiles'])
df_lipinski

df_combined = pd.concat([df,df_lipinski], axis=1)
df_combined

"""Removemos los compuestos con actividad intermedia o sin actividad"""

df_2class = df_combined[df_combined['class'] != 'intermediate''inactive']
df_2class

"""*Ya que obtuvimos el análisis de las moléculas, supimos cuáles serían buenos candidatos para un fármaco mediante el descarte de las condiciones idóneas establecidas como leyes de Lipinski.*

**Análisis de datos obtenidos**

Importación de librerías
"""

import seaborn as sns
sns.set(style='ticks')
import matplotlib.pyplot as plt

"""La librería nos va a permitir obtener gráficas de los datos que queramos resumir sin necesidad de utilizar alguna otra herramienta"""

sns.countplot(x='class', data=df_2class, edgecolor='black')

plt.xlabel('Bioactividad', fontsize=15, fontweight='bold')
plt.ylabel('Frecuencia', fontsize=15, fontweight='bold')

plt.show()