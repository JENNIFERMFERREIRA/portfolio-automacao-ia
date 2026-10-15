# Automação de Escritório com Python e IA

Automações que desenvolvi para transformar rotinas administrativas e financeiras de um escritório de advocacia em processos rápidos, confiáveis e documentados. O trabalho combina **Python** com o **Claude** (IA da Anthropic) atuando como agente: ele executa os scripts, lê sistemas web e prepara os resultados para revisão humana.

> **Privacidade:** este repositório contém versões reescritas e genéricas das automações. Todos os nomes, valores, processos e planilhas dos exemplos são **fictícios**. Nenhum dado de clientes ou do escritório foi publicado.

## Projetos

| Módulo | Problema | Solução | Técnicas |
| --- | --- | --- | --- |
| [`conciliacao/`](conciliacao/) | Conferir manualmente dezenas de boletos do banco contra a planilha de controle | Cruza os dados, aponta o que confere, o que diverge e o que falta lançar, e gera relatório em Excel | correspondência aproximada de nomes, soma de subconjuntos (programação dinâmica), openpyxl |
| [`pdf_extrator/`](pdf_extrator/) | Encontrar, num PDF de dezenas de páginas, só o demonstrativo que precisa ir anexado no e-mail | Localiza as páginas pelo conteúdo, lê nº do processo (padrão CNJ) e valor, gera um PDF novo nomeado | pypdf, expressões regulares |
| [`legendas_video/`](legendas_video/) | Editar vídeos curtos do perfil profissional com legendas modernas | Gera legendas animadas palavra a palavra a partir da transcrição do Whisper, prontas para o FFmpeg | Whisper, formato ASS, FFmpeg |

## Como o Claude entra no processo

```
Rotina agendada ──► Claude (agente) ──► scripts Python ──► relatório / rascunho
        │                 │                                      │
        │                 └─ lê sistemas web (banco, sistema     └─ revisão humana
        │                    jurídico, e-mail) pelo navegador        antes de qualquer envio
        └─ ex.: toda sexta às 11h
```

Princípios que sigo nas automações:

- **Rascunho, nunca envio automático**: e-mails e lançamentos ficam prontos para uma pessoa revisar.
- **Nada é apagado**: a automação só acrescenta ou marca; correções ficam a cargo de quem revisa.
- **Regras documentadas**: cada rotina tem um arquivo de instruções versionado, atualizado quando a regra de negócio muda.

## Como rodar os exemplos

```bash
pip install -r requirements.txt

# conciliação bancária
python conciliacao/exemplo/gerar_controle.py
python conciliacao/conciliador.py --boletos conciliacao/exemplo/boletos.csv \
       --controle conciliacao/exemplo/controle.xlsx --creditos 1042.50,1002.50

# extração de páginas de PDF
python pdf_extrator/exemplo/gerar_kit.py
python pdf_extrator/extrair_paginas.py pdf_extrator/exemplo/kit_exemplo.pdf saida \
       --chave "DEMONSTRATIVO DE CÁLCULO"

# legendas palavra a palavra
python legendas_video/legendas_ass.py legendas_video/exemplo/transcricao_exemplo.json \
       legendas.ass --destaques PYTHON
```

Saída da conciliação com os dados fictícios:

```
MARIA S OLIVEIRA         R$   350.00  CONFERE                     Maria da Silva Oliveira
FERNANDA R ALVES         R$   300.00  VALOR DIFERENTE             Fernanda Ribeiro Alves
PEDRO H COSTA            R$   200.00  SEM LANÇAMENTO NA PLANILHA
Líquido: R$ 2045.00 em 2 crédito(s)
```

## Tecnologias

Python · openpyxl · pypdf · reportlab · Whisper · FFmpeg · Claude (Anthropic) · Git/GitHub

## Autora

**Jennifer Ferreira**, graduada em Análise e Desenvolvimento de Sistemas (UCB) e estudante de Engenharia de Software.
[LinkedIn](https://www.linkedin.com/in/jennifer-ferreira-223183243)
