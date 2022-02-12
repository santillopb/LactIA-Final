# -*- coding: utf-8 -*-
"""notebook_final (2).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1tG-BjcWQ5TyLJK1vqFTCawLlSmTdgglL
"""

"""!pip install spacy
!pip install spacy --upgrade --pre
!python -m spacy download es_core_news_lg
!pip install BeautifulSoup4
!pip install requests
!pip install openpyxl
!pip install openpyxl --upgrade --pre
!pip install -U sentence-transformers"""
from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer('hiiamsid/sentence_similarity_spanish_es')
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import csv
import openpyxl
import spacy
nlp = spacy.load("es_core_news_lg")
print(openpyxl.__version__)

data_elactancia=pd.read_excel('nombres_e_lactancia.xlsx')
data_preguntas=pd.read_excel('base1.xlsx')
data_excepciones=pd.read_excel('excepciones_lactIA.xlsx')

def word2vec(word):
    from collections import Counter
    from math import sqrt

    # count the characters in word
    cw = Counter(word)
    # precomputes a set of the different characters
    sw = set(cw)
    # precomputes the "length" of the word vector
    lw = sqrt(sum(c*c for c in cw.values()))

    # return a tuple
    return cw, sw, lw

def cosdis(v1, v2):
    # which characters are common to the two words?
    common = v1[1].intersection(v2[1])
    # by definition of cosine distance we have
    return sum(v1[0][ch]*v2[0][ch] for ch in common)/v1[2]/v2[2]


def cosdis2(a, b):
    if len(a)==1:
      a1=a
      a2=a
    else:
      if len(a)%2==0:
        num=int(len(a)/2)
        a1=a[:num]
        a2=a[num:]
      if len(a)%2!=0:
        num=int((len(a)+1)/2)
        a1=a[:num]
        a2=a[num:]

    if len(b)==1:
      b1=b
      b2=b
    else:
      if len(b)%2==0:
        num=int(len(b)/2)
        b1=b[:num]
        b2=b[num:]
      if len(b)%2!=0:
        num=int((len(b)+1)/2)
        b1=b[:num]
        b2=b[num:]
      

    va1 = word2vec(a1)
    va2 = word2vec(a2)
    vb1 = word2vec(b1)
    vb2 = word2vec(b2)
    return ( ( cosdis(va1,vb1)+cosdis(va2,vb2) ) /2 )

def normalize(s):
    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
        ("?", ""),
        ("¿", ""),
        (",", ""),
    )
    for a, b in replacements:
        s = s.replace(a, b).replace(a.upper(), b.upper())
    return s

def sust(a):
  temp=''
  a=normalize(a).lower()
  doc = nlp(a)
  for token in doc:
    if token.pos_=='NOUN' or token.pos_=='PROPN' or token.pos_=='VERB' or token.pos_=='ADJ':
      temp=temp+token.text+' '
  a=temp
  a = a.split()
  return(a)

def ain(a):
  temp=''
  a=normalize(a).lower()
  doc = nlp(a)
  for token in doc:
    if token.pos_=='NOUN' or token.pos_=='PROPN' or token.pos_=='VERB' or token.pos_=='ADJ':
      temp=temp+token.text+' '
  a=temp
  return(a)

def preg(a):
  temp=''
  doc = nlp(a)
  for token in doc:
    if token.pos_=='NOUN' or token.pos_=='ADV' or token.pos_=='ADJ' or token.pos_=='PROPN' or token.pos_=='VERB' or token.pos_=='PRON' or token.pos_=='X':
      temp=temp+token.text+' '
  a=temp
  a=normalize(a).lower()
  return(a)

def guardaEmbeddings2(nombreFichero):
  lista = np.loadtxt(nombreFichero) 
  rows = int(lista[0]) 
  columns = int(lista[1]) 
  lista = lista[2:] 
  embeddings3 = lista.reshape(rows, columns) 
  emb = embeddings3.astype(np.float32)
  return emb

#Englobamos a partir de aqui funcion parametro pregunta devuelve respuesta

#pregunta ="Cuál es el riesgo de precose?"
def devRespuesta(pregunta):
  respuesta=""

  etapa=1
  if etapa==1:

    """pregunta_e1=preg(pregunta)

    for i in range(len(data_preguntas["Question"])-data_preguntas["Question"].isnull().sum(axis=0)):
      b=normalize(data_preguntas.iloc[i,0]).lower()
      b=preg(data_preguntas.iloc[i,0])
      print(b)"""

    pregunta_e1=normalize(pregunta).lower()

    embeddings1 = model.encode(pregunta_e1)
    #embeddings2 = model.encode(data_preguntas["Question"].array)
    embeddings2 = guardaEmbeddings2("test.txt")
    print(embeddings2)
    score_preg = util.semantic_search(embeddings1, embeddings2, top_k=1)
    score_preg = score_preg[0] 

    for max_preg in score_preg:
      data_preguntas.iloc[max_preg['corpus_id']]
    if max_preg['score'] > 0.4:
      respuesta=data_preguntas.iloc[max_preg['corpus_id'],-1]
      print("TIPO VBLE RESPUESTA: " + str(type(respuesta)))
    else: 
      etapa=2

  if etapa==2:
    c=ain(pregunta)
    a=sust(pregunta)
    
    array_prod=[]
    array_fila_prod=[]
    max_prod=0.0
    n_prod=0

    #Productos
    for i in range(len(data_elactancia)-data_elactancia['producto'].isnull().sum(axis=0)):
      array_fila_prod=[]
      max_prod=0.0
      b=normalize(data_elactancia.iloc[i,1]).lower()
      b=b.split()
      for k in range(len(a)):
        for j in range(len(b)):
          if cosdis2(a[k],b[j]) > max_prod:
            max_prod=cosdis2(a[k],b[j])
            """if a[k][:2]==b[j][:2]:
              max_prod+=0.1
            if a[k][:3]==b[j][:3]:
              max_prod+=0.1
            if a[k][:4]==b[j][:4]:
              max_prod+=0.1
            if a[k][2:]==b[j][2:]:
              max_prod+=0.1
            if a[k][3:]==b[j][3:]:
              max_prod+=0.1
            if a[k][4:]==b[j][4:]:
              max_prod+=0.1
            if cosdis2(c,data_elactancia.iloc[i,1])<0.65:
              max_prod-=0.8"""
            if a[k][:2]==b[j][:2]:
              max_prod+=0.1
            if a[k][:3]==b[j][:3]:
              max_prod+=0.1
            if a[k][:4]==b[j][:4]:
              max_prod+=0.1
            if a[k][len(a[k])-2:]==b[j][len(b[j])-2:]:
              max_prod+=0.1
            if a[k][len(a[k])-3:]==b[j][len(b[j])-3:]:
              max_prod+=0.1
            if a[k][len(a[k])-4:]==b[j][len(b[j])-4:]:
              max_prod+=0.1
            if cosdis2(c,data_elactancia.iloc[i,1])<0.5:
              max_prod-=0.8
        array_fila_prod.append(max_prod)
        max_prod=0.0
      for n in range(len(array_fila_prod)):
        if array_fila_prod[n]>max_prod:
          max_prod=array_fila_prod[n]
      array_prod.append(max_prod)
    max_prod=0
    for i in range(len(array_prod)):
      if array_prod[i] > max_prod:
        n_prod=i
        max_prod=array_prod[i]


  # revisar este pedazo de código
    array_marca=[]
    max_preg=0.0

    array_marca=[]
    array_fila_marca=[]
    max_marca=0.0
    n_marca=0



    #Marcas
    for i in range(len(data_elactancia)-data_elactancia['marca'].isnull().sum(axis=0)):
      array_fila_marca=[]
      max_marca=0.0
      b=normalize(data_elactancia.iloc[i,3]).lower()
      b=b.split()
      for k in range(len(a)):
        for j in range(len(b)):
          if cosdis2(a[k],b[j]) > max_marca:
            max_marca=cosdis2(a[k],b[j])
            """if a[k][:2]==b[j][:2]:
              max_marca+=0.1
            if a[k][:3]==b[j][:3]:
              max_marca+=0.1
            if a[k][:4]==b[j][:4]:
              max_marca+=0.1
            if a[k][2:]==b[j][2:]:
              max_marca+=0.1
            if a[k][3:]==b[j][3:]:
              max_marca+=0.1
            if a[k][4:]==b[j][4:]:
              max_marca+=0.1
            if cosdis2(c,data_elactancia.iloc[i,3])<0.65:
              max_marca-=0.8"""
            if a[k][:2]==b[j][:2]:
              max_marca+=0.1
            if a[k][:3]==b[j][:3]:
              max_marca+=0.1
            if a[k][:4]==b[j][:4]:
              max_marca+=0.1
            if a[k][len(a[k])-2:]==b[j][len(b[j])-2:]:
              max_marca+=0.1
            if a[k][len(a[k])-3:]==b[j][len(b[j])-3:]:
              max_marca+=0.1
            if a[k][len(a[k])-4:]==b[j][len(b[j])-4:]:
              max_marca+=0.1
            if cosdis2(c,data_elactancia.iloc[i,3])<0.5:
              max_marca-=0.8
        array_fila_marca.append(max_marca)
        max_marca=0.0
      for n in range(len(array_fila_marca)):
        if array_fila_marca[n]>max_marca:
          max_marca=array_fila_marca[n]
      array_marca.append(max_marca)
    max_marca=0
    for i in range(len(array_marca)):
      if array_marca[i] > max_marca:
        n_marca=i
        max_marca=array_marca[i]

    ok_elactancia=False

    if(max_prod>=max_marca):
      if(max_prod>0.8):
        #print(n_prod,max_prod,data_elactancia.iloc[n_prod,1],'producto')
        i=n_prod
        j=0
        etapa=3
      else:
        etapa=4
    else:
      if(max_marca>0.8):
          #print(n_marca, max_marca, data_elactancia.iloc[n_marca,3],'marca')
          i=n_marca
          j=2
          etapa=3
      else:
        etapa=4
    print(n_prod,max_prod,data_elactancia.iloc[n_prod,1],'producto')
    print(n_marca, max_marca, data_elactancia.iloc[n_marca,3],'marca')
  if etapa==3:
    n_punto=0

    url_producto = data_elactancia.iloc[i,j]
    page = requests.get(url_producto).text
    soup = BeautifulSoup(page, "html.parser")
    try:
        name=''
        #Realizamos Webscrapping y declaramos varias variables que contendrán parte del texto de la página.
        counter_items= soup.find_all('div',class_='col-xs-10')
        numero=0
        for item in counter_items:
          if(numero==0):
            name = item.h1.text
            name = name.replace("\n        ", "")
          numero+=1
    except Exception:
      name='*****'
    try:
      Texto1=''
      Texto2=''
      Texto3_temp=''
      Texto3=''
      #Realizamos Webscrapping y declaramos varias variables que contendrán parte del texto de la página.
      counter_items= soup.find_all('div',class_='column col-xs-12 col-sm-12 col-md-3 no-lateral-padding')
      numero=0
      for item in counter_items:
        if(numero==0):
          Texto1 = item.h2.p.text
          Texto2 = item.h4.text
        numero+=1

      counter_items= soup.find_all('div',class_='column col-xs-12 col-sm-12 col-md-6 no-lateral-padding')
      numero=0
      for item in counter_items:
        if(numero==0):
          Texto3_temp = item.text
        numero+=1
    except Exception:
      Texto1='*****'
      Texto2='*****'
      Texto3='*****'

    i=0
    for caracter in Texto3_temp:
      if n_punto<5:
        if caracter=='.':
          n_punto+=1
        Texto3=Texto3+caracter

    name=name.strip()
    Texto1=Texto1.strip()
    Texto2=Texto2.strip()
    Texto2_5='Si quieres más información:'
    Texto3=Texto3.strip()
    Texto3=Texto3+'..'

    """resp_adic=1
    for i in range(len(data_excepciones)):
      if data_excepciones.iloc[i,0] in normalize(pregunta).lower():
        resp_adic=0"""
    
    """if resp_adic==1:
      resp_adic='No se ha encontrado la pregunta, pero te dejamos información adicional:'
      print(resp_adic)"""


    """print(name)
    print(Texto1)
    print(Texto2)
    print(Texto3)
    print(Texto2_5)
    print(url_producto)"""
    
    respuesta = ""+name+"<br>"+Texto1+"<br>"+Texto2+"<br>"+Texto3+"<br>"+Texto2_5+"<br>"+"<a href='"+url_producto+"'"+">"+url_producto+"</a>"
    #respuesta = "<a href='"+url_producto+"'"+">"+url_producto+"</a>"
    #respuesta = ""+name+"<br>"+Texto1+"<br>"+Texto2+"<br>"+Texto3+"<br>"+Texto2_5+"<br>"+url_producto

  if etapa==4:
    respuesta='No he entendido la pregunta, puedes repetirla?'

  print(respuesta)
  respuesta = str(respuesta)
  respuesta = respuesta.replace("\n","<br>")
  respuesta = respuesta.replace("\r","")

  
  
  return respuesta