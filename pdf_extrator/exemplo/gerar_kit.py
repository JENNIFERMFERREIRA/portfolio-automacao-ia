"""Gera um PDF fictício de 5 páginas (kit_exemplo.pdf) para testar o extrator."""
import os

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

PAGINAS = [
    ["PETIÇÃO INICIAL", "Texto de exemplo da petição (fictício)."],
    ["PROCURAÇÃO", "Documento fictício."],
    ["PROCESSO JUDICIAL ELETRÔNICO", "Número: 0001234-56.2026.4.01.0000", "Classe: CUMPRIMENTO DE SENTENÇA"],
    ["DEMONSTRATIVO DE CÁLCULO", "Requerente: Fulano de Tal (fictício)", "Principal: R$ 9.500,00",
     "Juros: R$ 1.250,40", "VALOR TOTAL: R$ 10.750,40"],
    ["COMPROVANTE DE ENDEREÇO", "Documento fictício."],
]

c = canvas.Canvas(os.path.join(os.path.dirname(os.path.abspath(__file__)), "kit_exemplo.pdf"), pagesize=A4)
for linhas in PAGINAS:
    y = 780
    for i, linha in enumerate(linhas):
        c.setFont("Helvetica-Bold" if i == 0 else "Helvetica", 16 if i == 0 else 12)
        c.drawString(60, y, linha)
        y -= 28
    c.showPage()
c.save()
print("kit_exemplo.pdf criado")
