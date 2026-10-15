#!/usr/bin/env python3
"""Gera legendas animadas palavra a palavra (formato ASS) a partir da transcrição do Whisper.

Usado na edição automatizada de vídeos curtos (Reels/Shorts): o Whisper transcreve com o tempo de
cada palavra, este script agrupa as palavras em blocos curtos e cada palavra "acende" no momento exato
da fala (fade + desfoque). O FFmpeg queima a legenda no vídeo.

Uso:
    python -m whisper video.mp4 --language pt --word_timestamps True --output_format json
    python legendas_ass.py video.json legendas.ass --destaques INSS,APOSENTADORIA
    ffmpeg -i video.mp4 -vf "ass=legendas.ass" -c:a copy video_legendado.mp4
"""
import argparse
import json

ESTILO = ("Style: Cap,Arial,46,&H00FFFFFF,&H00FFFFFF,&H90000000,&H78000000,-1,0,0,0,100,100,1,0,1,2,3,5,"
          "80,80,0,1")
ENTRADA = r"{\alpha&HFF&\blur2.5\t(%d,%d,\alpha&H00&\blur0.4)}"   # palavra aparece e fica nítida
DOURADO = "&H0062AEED&"


def tempo_ass(t: float) -> str:
    t = max(0.0, t)
    return f"{int(t // 3600)}:{int(t % 3600 // 60):02d}:{t % 60:05.2f}"


def blocos(palavras, max_palavras=3, max_chars=16):
    """Quebra em blocos curtos: no máximo N palavras, ou na pontuação, ou se ficar longo demais."""
    atual = []
    for p in palavras:
        if atual and len(" ".join(x["w"] for x in atual + [p])) > max_chars:
            yield atual
            atual = []
        atual.append(p)
        if len(atual) == max_palavras or p["w"][-1] in ",.?!":
            yield atual
            atual = []
    if atual:
        yield atual


def main():
    ap = argparse.ArgumentParser(description="Whisper JSON -> legendas ASS palavra a palavra")
    ap.add_argument("whisper_json")
    ap.add_argument("saida_ass")
    ap.add_argument("--largura", type=int, default=1080)
    ap.add_argument("--altura", type=int, default=1920)
    ap.add_argument("--y", type=int, default=1265, help="altura da legenda na tela")
    ap.add_argument("--destaques", default="", help="palavras em dourado, separadas por vírgula")
    a = ap.parse_args()

    destaques = {d.strip().upper() for d in a.destaques.split(",") if d.strip()}
    with open(a.whisper_json, encoding="utf-8") as f:
        segmentos = json.load(f)["segments"]
    palavras = [{"t": w["start"], "e": w["end"], "w": w["word"].strip()}
                for s in segmentos for w in s.get("words", []) if w["word"].strip()]

    linhas = ["[Script Info]", "ScriptType: v4.00+", f"PlayResX: {a.largura}", f"PlayResY: {a.altura}",
              "WrapStyle: 2", "ScaledBorderAndShadow: yes", "", "[V4+ Styles]",
              "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, "
              "Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, "
              "Alignment, MarginL, MarginR, MarginV, Encoding", ESTILO, "", "[Events]",
              "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
    grupos = list(blocos(palavras))
    for i, g in enumerate(grupos):
        inicio = g[0]["t"] - 0.04
        prox = grupos[i + 1][0]["t"] - 0.04 if i + 1 < len(grupos) else None
        fim = prox if prox is not None and prox - g[-1]["e"] < 0.45 else g[-1]["e"] + 0.18
        partes = []
        for p in g:
            d = int((p["t"] - inicio) * 1000)
            txt = p["w"].upper().strip(",.")
            cor = r"{\c" + DOURADO + "}" if txt.strip("?!") in destaques else r"{\c&HFFFFFF&}"
            partes.append(ENTRADA % (d, d + 90) + cor + txt)
        linhas.append(f"Dialogue: 2,{tempo_ass(inicio)},{tempo_ass(fim)},Cap,,0,0,0,,"
                      f"{{\\move(540,{a.y + 6},540,{a.y},0,120)}}" + " ".join(partes))
    with open(a.saida_ass, "w", encoding="utf-8") as f:
        f.write("\n".join(linhas) + "\n")
    print(f"{len(grupos)} blocos de legenda -> {a.saida_ass}")


if __name__ == "__main__":
    main()
