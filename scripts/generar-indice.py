#!/usr/bin/env python3
"""Genera indice.json con todas las prácticas .html del repositorio.

Uso:  python3 scripts/generar-indice.py [carpeta_raiz] [salida.json]

Lo ejecuta el workflow de GitHub cada vez que haces push, así que no hace
falta lanzarlo a mano. También puedes ejecutarlo en tu ordenador para probarlo.
"""
import json
import os
import re
import subprocess
import sys
from html.parser import HTMLParser

RAIZ = sys.argv[1] if len(sys.argv) > 1 else "."
SALIDA = sys.argv[2] if len(sys.argv) > 2 else "indice.json"
IGNORAR = {"node_modules", "scripts", "_site"}

# Qué técnicas usa cada práctica (mismas reglas que index.html).
DETECTAR = [
    ("innerHTML", r"innerHTML"),
    ("textContent", r"textContent|innerText"),
    ("onclick", r"onclick"),
    ("eventos", r"addEventListener|onchange|oninput|onmouse|onkey|onsubmit"),
    ("console.log", r"console\.log"),
    ("alert", r"\balert\s*\("),
    ("prompt", r"\bprompt\s*\("),
    ("document.write", r"document\.write"),
    ("arrays", r"\.push\(|\.length|=\s*\[[^\]]*,[^\]]*\]"),
    ("condicionales", r"\bif\s*\(|\bswitch\s*\("),
    ("bucles", r"\bfor\s*\(|\bwhile\s*\("),
    ("funciones", r"function\s+\w+|=>"),
    ("style", r"\.style\."),
    ("img.src", r"\.src\s*="),
    ("fetch", r"\bfetch\s*\("),
    ("localStorage", r"localStorage"),
]
GENERICO = re.compile(r"^(document|mi p[aá]gina|untitled|sin t[ií]tulo|prueba)?$", re.I)


class Lector(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = ""
        self.h1 = ""
        self.meta = ""
        self.parrafos = []
        self.codigo = []
        self._en = None
        self._buf = []
        self._script = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "script":
            self._script = True
        for nombre, valor in attrs:
            if nombre.lower().startswith("on"):
                self.codigo.append(f"{nombre}={valor or ''}")
        if tag == "meta" and (a.get("name") or "").lower() == "description":
            self.meta = (a.get("content") or "").strip()
        if tag in ("title", "h1", "p") and self._en is None:
            if tag == "h1" and self.h1:
                return
            self._en, self._buf = tag, []

    def handle_data(self, data):
        if self._script:
            self.codigo.append(data)
        if self._en:
            self._buf.append(data)

    def handle_endtag(self, tag):
        if tag == "script":
            self._script = False
        if tag != self._en:
            return
        texto = " ".join("".join(self._buf).split())
        if tag == "title":
            self.title = texto
        elif tag == "h1":
            self.h1 = texto
        else:
            self.parrafos.append(texto)
        self._en = None


def bonito(archivo):
    s = re.sub(r"\.html?$", "", archivo, flags=re.I)
    s = re.sub(r"[-_]+", " ", s)
    s = re.sub(r"([a-z])([A-Z])", r"\1 \2", s)
    return s[:1].upper() + s[1:]


def palabras(texto):
    return {w for w in re.findall(r"\w+", texto.lower()) if len(w) > 2}


def parecidos(a, b):
    pa, pb = palabras(a), palabras(b)
    return bool(pa and pb) and len(pa & pb) / min(len(pa), len(pb)) >= 0.5


def analizar(texto, archivo):
    p = Lector()
    try:
        p.feed(texto)
    except Exception:
        pass
    t, h = p.title.strip(), p.h1.strip()
    codigo = "\n".join(p.codigo)
    tags = [n for n, rx in DETECTAR if re.search(rx, codigo)][:4]

    if GENERICO.match(t):
        nombre = h or bonito(archivo)
    elif not h or h.lower() in t.lower() or t.lower() in h.lower():
        nombre = t
    elif parecidos(t, h):
        nombre = h
    else:
        nombre = f"{t}: {h}"

    primero = next((x for x in p.parrafos if len(x) > 24 and not re.match(r"^\d+[.)]", x)), "")
    if p.meta:
        desc = p.meta
    elif primero:
        desc = primero
    elif tags:
        desc = "Práctica con " + ", ".join(tags) + "."
    else:
        desc = "Práctica en HTML."
    return {"nombre": nombre, "desc": desc, "tags": tags}


def main():
    practicas = []
    for carpeta, subdirs, archivos in os.walk(RAIZ):
        subdirs[:] = sorted(d for d in subdirs if not d.startswith(".") and d not in IGNORAR)
        for f in sorted(archivos):
            if not f.lower().endswith((".html", ".htm")):
                continue
            ruta = os.path.relpath(os.path.join(carpeta, f), RAIZ).replace(os.sep, "/")
            if ruta.lower() in ("index.html", "index.htm"):
                continue
            with open(os.path.join(carpeta, f), encoding="utf-8", errors="replace") as fh:
                datos = analizar(fh.read(), f)
            practicas.append({"path": ruta, **datos})

    ultimo = None
    try:
        ultimo = subprocess.run(
            ["git", "-C", RAIZ, "log", "-1", "--format=%cI"],
            capture_output=True, text=True, check=True,
        ).stdout.strip() or None
    except Exception:
        pass

    with open(SALIDA, "w", encoding="utf-8") as out:
        json.dump({"ultimo": ultimo, "practicas": practicas}, out, ensure_ascii=False, indent=2)
        out.write("\n")
    print(f"{len(practicas)} prácticas escritas en {SALIDA}")


if __name__ == "__main__":
    main()
