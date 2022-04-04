# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import csv 
from datetime import datetime


def cargaPaginaObtieneLinks (url):
   #codigo https://chromedriver.chromium.org/getting-started  
    driver = webdriver.Chrome(executable_path=r"D:\personal\2022\maestria\aulas\M2.851 - Tipología y ciclo de vida de los datos aula 1\practica 1\chromedriver.exe")
    driver.get(url)
    time.sleep(2)  # Espera 2 segundos para abrir la pagina
    scroll_pause_time = 1 # Tiempo de pausa para que el scroll baje 
    screen_height = driver.execute_script("return window.screen.height;")   # obtiene la altura de la pagina
    i = 1

    while True:
        # desplazarse una altura de pantalla cada vez
        driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))  
        i += 1
        time.sleep(scroll_pause_time)
        # actualizar la altura de desplazamiento cada vez que se desplazace hacia abajo
        scroll_height = driver.execute_script("return document.body.scrollHeight;")  
        # sale del bucle cuando ya no existe desplazarnos mas 
        if (screen_height) * i > scroll_height:
            break


#Llena la lista con los links 
    soup = BeautifulSoup(driver.page_source,"html.parser");
    propiedades=soup.find (id='propiedades');
    links = [];
    for etiqueta_padre in propiedades.find_all('li'):
        for etiqueta_a in etiqueta_padre.find_all('a'):
            links.append('https://www.inmovision.com.ec'+etiqueta_a.get('href'))  
    
    return links;   

#cargaPaginaScrollInfinito ('https://www.inmovision.com.ec/Venta');
def obtieneInformacionLinks(links):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,\
            */*;q=0.8",
            "Accept-Encoding": "gzip, deflate, sdch, br",
            "Accept-Language": "en-US,en;q=0.8",
            "Cache-Control": "no-cache",
            "dnt": "1",
            "Pragma": "no-cache",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/5\
                37.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
                }
        
    lista=[]
    for link in links:
        diccionario = {};
        page = requests.get(link, headers=headers, timeout=10);
        if page.status_code == 200:
            soup = BeautifulSoup(page.content);
            detalle=soup.find (id='ficha_detalle_cuerpo');   
            for etiqueta_div in detalle.find_all('div',attrs={'class':'ficha_detalle_item'}):
                tag=etiqueta_div.contents[0];
                diccionario[tag.text]=etiqueta_div.contents[2];
            
            precio=soup.find ('div',attrs={'class':'operation-val op-venta'})
            diccionario['Precio']=precio.find('span').text ;
             
            referencia=soup.find ('div',attrs={'class':'title-address'})
            diccionario['Referencia']=referencia.text ;

            diccionario['Fecha']=datetime.today().strftime('%d-%m-%Y') ;
            lista.append(diccionario)
    return lista;

#guarda la informacion en archivo csv
def guardaInformacion(lista):
    FIELDS =['Tipo de Propiedad','Sector','Total construido','Precio','Referencia','Dormitorios','Baños','Antiguedad','Superficie','Ambientes','24 Hours Security','Alcantarillado','Parqueadero fijo','Seguridad 24Hs','Expensas','Fecha de entrega','Fecha']
    with open('datos.csv', 'w', newline="") as csvfile: 
        writer = csv.DictWriter(csvfile, fieldnames = FIELDS) 
        writer.writeheader() 
        writer.writerows(lista)
 
##Llamada  a los metodos
links=cargaPaginaObtieneLinks ('https://www.inmovision.com.ec/Venta');
listaDiccionarios = obtieneInformacionLinks(links);
guardaInformacion(listaDiccionarios);

    
