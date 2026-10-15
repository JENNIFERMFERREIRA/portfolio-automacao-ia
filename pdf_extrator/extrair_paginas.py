#!/usr/bin/env python3
"""Extrai de um PDF grande apenas as páginas de um documento específico e lê os dados principais.

Caso real (anonimizado): o setor jurídico recebe um "kit" com dezenas de páginas e o financeiro só
precisa do demonstrativo de cálculo para anexar ao e-mail de repasse. O script:
  1. encontra as páginas pelo texto (palavras-chave configuráveis);
  2. inclui a capa imediatamente anterior, se existir;
  3. lê por expressão regular o nº do processo (padrão CNJ) e o valor total;
  4. grava um PDF novo, nomeado pelo nº do processo, e imprime um resumo em JSON.

Uso:
    python extrair_paginas.py exemplo/kit_exemplo.pdf saida/ --chave "DEMONSTRATIVO DE CÁLCULO"
"""
import argparse
import json
import os
import re

from pypdf import PdfReader, PdfWriter

PROCESSO_CNJ = re.compile(r"\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}")
VALOR_TOTAL = re.compile(r"VALOR TOTAL[^\d]*([\d\.]+,\d{2})", re.IGNORECASE)


def main():
    ap = argparse.ArgumentParser(description="Recorta páginas de um PDF pelo conteúdo.")
    ap.add_argument("pdf")
    ap.add_argument("saida")
    ap.add_argument("--chave", action="append", required=True, help="texto que identifica as páginas (repita para várias)")
    ap.add_argument("--capa", default="Número:", help="texto que identifica a capa logo antes do documento")
    a = ap.parse_args()

    leitor = PdfReader(a.pdf)
    textos = [" ".join((p.extract_text() or "").split()) for p in leitor.pages]
    alvo = [i for i, t in enumerate(textos) if all(ch.upper() in t.upper() for ch in a.chave)]
    if not alvo:
        print(json.dumps({"erro": "páginas não encontradas", "pdf": a.pdf}, ensure_ascii=False))
        raise SystemExit(1)
    if alvo[0] > 0 and a.capa in textos[alvo[0] - 1]:
        alvo.insert(0, alvo[0] - 1)

    texto = " ".join(textos[i] for i in alvo)
    processo = (PROCESSO_CNJ.search(texto) or [None])[0] or ""
    valor = VALOR_TOTAL.search(texto)

    escritor = PdfWriter()
    for i in alvo:
        escritor.add_page(leitor.pages[i])
    os.makedirs(a.saida, exist_ok=True)
    destino = os.path.join(a.saida, (re.sub(r"\D", "", processo) or "sem_processo") + "_documento.pdf")
    with open(destino, "wb") as f:
        escritor.write(f)

    print(json.dumps({"arquivo": destino, "processo": processo, "valor_total": valor.group(1) if valor else "",
                      "paginas": [i + 1 for i in alvo]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
