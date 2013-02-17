#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import requests
from bs4 import BeautifulSoup

def tagWords(tag):
    return(re.sub(r'\W+', ' ', tag.text).strip())

def horarios():
    jornadas = dict()
    url = "http://www.lfp.es/lfpimprimir.aspx?controltype=hor"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, from_encoding="UTF-8")
    for table in soup.findAll("table"):
        jornada = None
        for row in table.findAll('tr'):
            cols = row.findAll('td')
            rowWords = tagWords(row)
            titleMatch = re.match(".+Jornada \d+", rowWords)
            if titleMatch and (len(cols) == 1):
                jornada = rowWords
                continue
            else:
                if jornada and (len(cols) == 9):
                    partido = list()
                    for col in cols:
                        if len(col.text):
                            partido.append(col.text)
                    if len(partido):
                        partido = dict(zip(['Local','Visitante','Fecha','Hora', 'Arbitro', 'Detalles'], partido))
                        if not jornada in jornadas:
                            jornadas[jornada] = list()
                        jornadas[jornada].append(partido)
    return jornadas