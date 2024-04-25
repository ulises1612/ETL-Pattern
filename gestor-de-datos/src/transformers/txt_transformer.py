##!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------
# Archivo: txt_transformer.py
# Capitulo: Flujo de Datos
# Autor(es): Perla Velasco & Yonathan Mtz. & Jorge Solís, modificado por Omar Luna
# Version: 1.0.1 Abril 2024
# Descripción:
#
#   Este archivo define un procesador de datos que se encarga de transformar
#   y formatear el contenido de un archivo TXT
#-------------------------------------------------------------------------
from src.extractors.txt_extractor import TXTExtractor
from os.path import join
import luigi, os, json, re

class TXTTransformer(luigi.Task):

    def requires(self):
        return TXTExtractor()

    def run(self):
        result = []
        for file in self.input():
            with file.open() as txt_file:
                header = []
                regex = re.compile('[^a-zA-Z]')
                firstLine = txt_file.readline()
                firstLine = firstLine.lower()
                header = [regex.sub('', column) for column in firstLine.split(',')]
                for row in txt_file.read().split(';'):
                    if(len(row)<=0):
                        continue
                    row = row.replace('\n','')
                    row = row.split(',')
                    entry = dict(zip(header, row))

                    if not entry["descricao"]:
                        continue

                    result.append(
                        {
                            "description": entry["descricao"],
                            "quantity": entry["montante"],
                            "price": entry["precounitario"],
                            "total": float(entry["montante"]) * float(entry["precounitario"]),
                            "invoice": entry["numerodafatura"],
                            "provider": entry["iddocliente"],
                            "country": entry["pais"]
                        }
                    )
        with self.output().open('w') as out:
            out.write(json.dumps(result, indent=4))

    def output(self):
        project_dir = os.path.dirname(os.path.abspath("loader.py"))
        result_dir = join(project_dir, "result")
        return luigi.LocalTarget(join(result_dir, "txt.json"))