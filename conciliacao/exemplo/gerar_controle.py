"""Gera a planilha de controle fictícia usada no exemplo (controle.xlsx)."""
import datetime as dt
import os

import openpyxl

wb = openpyxl.Workbook()
ws = wb.active
ws.append(["VALOR", "DATA", "CLIENTE", "CONFERIDO"])
for valor, dia, cliente in [(350.00, 3, "Maria da Silva Oliveira"), (420.00, 3, "João Pedro dos Santos"),
                            (280.00, 4, "Ana Clara Ferreira Lima"), (510.00, 4, "Carlos Eduardo Souza"),
                            (330.00, 5, "Fernanda Ribeiro Alves"), (150.00, 6, "Lucas Martins")]:
    ws.append([valor, dt.datetime(2026, 3, dia), cliente, None])
wb.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), "controle.xlsx"))
print("controle.xlsx criado")
