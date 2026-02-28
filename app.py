"""
📋 APP PEDIDOS REVISTAS EBD – 1º TRIMESTRE 2026
App Web Flask — banco de dados compartilhado entre usuários
"""

from flask import Flask, render_template, request, jsonify
import json, os

app = Flask(__name__)

# ══════════════════════════════════════════════════════
# DADOS
# ══════════════════════════════════════════════════════
TIPOS = [
    ("adulto_mestre",    "Mestre Adulto",       14.45, "ADULTO",   "#2E4057"),
    ("adulto_mestre_cd", "Mestre Adulto C.Dura", 28.05, "ADULTO",  "#2E4057"),
    ("adulto_aluno",     "Aluno Adulto",          9.60, "ADULTO",   "#2E4057"),
    ("jovem_mestre",     "Mestre Jovem",         14.45, "JOVENS",   "#1B6CA8"),
    ("jovem_aluno",      "Aluno Jovem",           9.60, "JOVENS",   "#1B6CA8"),
    ("pre_adol_aluno",   "Pré-Adol. Aluno",       9.60, "INFANTIL", "#0E7C4C"),
    ("pre_adol_prof",    "Pré-Adol. Prof.",      14.45, "INFANTIL", "#0E7C4C"),
    ("primarios_aluno",  "Primários Aluno",        8.00, "INFANTIL", "#0E7C4C"),
    ("primarios_prof",   "Primários Prof.",       14.45, "INFANTIL", "#0E7C4C"),
    ("maternal_aluno",   "Maternal Aluno",         8.00, "INFANTIL", "#0E7C4C"),
    ("maternal_prof",    "Maternal Prof.",        14.45, "INFANTIL", "#0E7C4C"),
    ("livro_apoio",      "Livro Apoio Jov./Ad.", 17.95, "APOIO",    "#7B3F00"),
]
TIPO_IDS   = [t[0] for t in TIPOS]
TIPO_PRECO = {t[0]: t[2] for t in TIPOS}

TODAS_PESSOAS = sorted([
    "ABNER BERNARDO","AGATHA HADASSA","ANA ESTHER","ANA LÍVIA CASTRO",
    "ANA PALOMA","ANA SOPHIA","ANDRESSA SILVA","ANTONIO JORGE",
    "ANTTONY ICARO","APOLLO PAZ","ARLIAN FERREIRA","ARLINDO DE OLIVEIRA",
    "BRUNA LOHANNA","CATARINA AMARANTE","CATIA FREITAS","CEZIANE",
    "CINDY BARROS MARTINS","CLARYSSA BIANCA","DANIELA DE PAULA",
    "DAVINIEL NOBRE","DELAIDE PROCÓPIO","DIANA GOMES","EDUARDA CASTRO",
    "EDUARDO BEZERRA","ENEAS CARLOS","ERICK NUNES","ESTEVÃO CIPRIANO",
    "ESTEVÃO MARQUES","ETHAN DE CASTRO","EVANIR ARAÚJO","EVERINA AMARANTE",
    "FELIPE ARAÚJO","FELIPE BARRETO","FRANCIMAR (LUCIANA)","GABRIEL SOUSA",
    "GEANE MARIA","GILSON VIRGÍNIO","HERIC LIMA","IANNY ALENCAR",
    "ISAAC MORAES","ISAIAS MORAIS","JADY AMARANTE","JASMINE",
    "JAYANE AMARANTE","JOABE ARAÚJO","JOÃO B. ARCANJO","JOÃO B. FERREIRA",
    "JOÃO MARCOS","JOÃO MARCOS MARQUES","JOÃO MARKUS","JOÃO PAULO",
    "JOÃO PROCÓPIO","JOSÉ IVO","JOSÉ NILSON XAVIER MARTINS","JUACI MARTINS",
    "KAEL ARAÚJO","KAILY ANSELMO","KAUAN MARQUES","LAURA BEATRIZ",
    "LEIDIANY ROBERTA","LENISA CASTRO","LIDIANE DO AMARANTE",
    "LOURENÇO LUCAS","LUCAS SALES","LUCILENE SALLES","LUIS RICARDO",
    "LUIZ NETO","MANUELA BERNARDO","MARCELLE VÍRNIA","MARCILIO VICTOR",
    "MARCOS ANTÔNIO","MARIA EMANUELE","MARIA LOPES (ELITA)","MARESSA ROCHA",
    "MARNIA VICTORIA","MICHELE MARQUES","MILKA KÉSIA","NAZARÉ MARQUES",
    "NILSON MARTINS","OLIVER ROCHA","PAULLYANE PAZ","PAULO PAZ",
    "PEDRO PAULO","RAISSA CASTRO","RAKELLY LOPES",
    "RAIMUNDO DE FREITAS (RAY)","RAYLSON FERREIRA","REGIANE ALCÂNTARA",
    "RONIELE MARQUES","SILVERIA CALDAS","YVANA GOMES",
])

FAMILIAS = [
    {"nome":"Família Isaías Morais",         "resp":"ISAIAS MORAIS",
     "membros":["ISAIAS MORAIS","ISAAC MORAES","LEIDIANY ROBERTA"]},
    {"nome":"Família Marcelle Vírnia",        "resp":"MARCELLE VÍRNIA",
     "membros":["MARCELLE VÍRNIA","MARCILIO VICTOR","MARNIA VICTORIA","ANA SOPHIA"]},
    {"nome":"Família Daniela de Paula",       "resp":"DANIELA DE PAULA",
     "membros":["DANIELA DE PAULA","JOÃO MARCOS"]},
    {"nome":"Família Marcos Antônio/Michele", "resp":"MARCOS ANTÔNIO",
     "membros":["MARCOS ANTÔNIO","MICHELE MARQUES","JOÃO MARCOS MARQUES","ESTEVÃO MARQUES"]},
    {"nome":"Família Juaci Martins",          "resp":"JUACI MARTINS",
     "membros":["JUACI MARTINS","REGIANE ALCÂNTARA","GEANE MARIA"]},
    {"nome":"Família Gilson Virgínio",        "resp":"GILSON VIRGÍNIO",
     "membros":["GILSON VIRGÍNIO","ANA ESTHER"]},
    {"nome":"Família Felipe Araújo",          "resp":"FELIPE ARAÚJO",
     "membros":["FELIPE ARAÚJO","YVANA GOMES","KAILY ANSELMO","KAEL ARAÚJO"]},
    {"nome":"Núcleo Diana Gomes",             "resp":"DIANA GOMES",
     "membros":["DIANA GOMES","AGATHA HADASSA","LOURENÇO LUCAS"]},
    {"nome":"Família Nazaré Marques",         "resp":"NAZARÉ MARQUES",
     "membros":["NAZARÉ MARQUES","RONIELE MARQUES","KAUAN MARQUES"]},
    {"nome":"Família Lidiane do Amarante",    "resp":"LIDIANE DO AMARANTE",
     "membros":["LIDIANE DO AMARANTE","LAURA BEATRIZ"]},
    {"nome":"Família Lenisa Castro",          "resp":"LENISA CASTRO",
     "membros":["LENISA CASTRO","ETHAN DE CASTRO","ANA LÍVIA CASTRO"]},
    {"nome":"Família Felipe Barreto",         "resp":"FELIPE BARRETO",
     "membros":["FELIPE BARRETO","RAISSA CASTRO"]},
    {"nome":"Família Paulo Paz",              "resp":"PAULO PAZ",
     "membros":["PAULO PAZ","CEZIANE","APOLLO PAZ","PAULLYANE PAZ"]},
    {"nome":"Família José Ivo",               "resp":"JOSÉ IVO",
     "membros":["JOSÉ IVO","JASMINE","JAYANE AMARANTE","JADY AMARANTE","DAVINIEL NOBRE"]},
    {"nome":"Família Lucilene Salles",        "resp":"LUCILENE SALLES",
     "membros":["LUCILENE SALLES","LUCAS SALES"]},
    {"nome":"Família Arlian Ferreira",        "resp":"ARLIAN FERREIRA",
     "membros":["ARLIAN FERREIRA","MARESSA ROCHA","OLIVER ROCHA"]},
    {"nome":"Núcleo Eduarda Castro",          "resp":"EDUARDA CASTRO",
     "membros":["EDUARDA CASTRO","ERICK NUNES"]},
    {"nome":"Família Silvéria Caldas",        "resp":"SILVERIA CALDAS",
     "membros":["SILVERIA CALDAS","ENEAS CARLOS"]},
    {"nome":"Família Arlindo de Oliveira",    "resp":"ARLINDO DE OLIVEIRA",
     "membros":["ARLINDO DE OLIVEIRA","ANDRESSA SILVA"]},
    {"nome":"Família Nilson Martins",         "resp":"NILSON MARTINS",
     "membros":["NILSON MARTINS","CINDY BARROS MARTINS"]},
    {"nome":"Família Batista Ferreira",       "resp":"CATIA FREITAS",
     "membros":["CATIA FREITAS","CLARYSSA BIANCA","JOÃO B. FERREIRA"]},
    {"nome":"Família Raimundo (Ray)",         "resp":"RAIMUNDO DE FREITAS (RAY)",
     "membros":["RAIMUNDO DE FREITAS (RAY)","ABNER BERNARDO","MANUELA BERNARDO"]},
    {"nome":"Família Milka Késia",            "resp":"MILKA KÉSIA",
     "membros":["MILKA KÉSIA","EDUARDO BEZERRA"]},
]

_em_familia = {m for f in FAMILIAS for m in f["membros"]}
SOLTOS = sorted([p for p in TODAS_PESSOAS if p not in _em_familia])

# ══════════════════════════════════════════════════════
# BANCO DE DADOS (arquivo JSON)
# ══════════════════════════════════════════════════════
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ebd_dados.json")

def load_db():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return {}

def save_db(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_pessoa(db, nome):
    if nome not in db:
        db[nome] = {tid: 0 for tid in TIPO_IDS}
        db[nome].update(status="", forma="", valor_pago=0.0, data="")
    return db[nome]

def qtd_total(db, nome):
    return sum(get_pessoa(db, nome).get(t, 0) for t in TIPO_IDS)

def valor_total(db, nome):
    return sum(get_pessoa(db, nome).get(t, 0) * TIPO_PRECO[t] for t in TIPO_IDS)

# ══════════════════════════════════════════════════════
# ROTAS
# ══════════════════════════════════════════════════════
@app.route("/")
def index():
    db = load_db()
    resumo = {
        "pediu":  sum(1 for n in TODAS_PESSOAS if qtd_total(db, n) > 0),
        "qtd":    sum(qtd_total(db, n) for n in TODAS_PESSOAS),
        "valor":  sum(valor_total(db, n) for n in TODAS_PESSOAS),
        "vpago":  sum(get_pessoa(db, n).get("valor_pago", 0) or 0 for n in TODAS_PESSOAS),
        "pago":   sum(1 for n in TODAS_PESSOAS if get_pessoa(db, n).get("status") == "PAGO"),
        "pend":   sum(1 for n in TODAS_PESSOAS if get_pessoa(db, n).get("status") == "PENDENTE"),
        "parc":   sum(1 for n in TODAS_PESSOAS if get_pessoa(db, n).get("status") == "PARCIAL"),
    }
    pessoas_data = {}
    for nome in TODAS_PESSOAS:
        p = get_pessoa(db, nome)
        pessoas_data[nome] = {
            **{tid: p.get(tid, 0) for tid in TIPO_IDS},
            "status": p.get("status", ""),
            "forma":  p.get("forma", ""),
            "valor_pago": p.get("valor_pago", 0) or 0,
            "data":   p.get("data", ""),
            "qtd_total":   qtd_total(db, nome),
            "valor_total": valor_total(db, nome),
        }
    return render_template("index.html",
        tipos=TIPOS, pessoas=TODAS_PESSOAS,
        familias=FAMILIAS, soltos=SOLTOS,
        pessoas_data=pessoas_data, resumo=resumo)

@app.route("/salvar", methods=["POST"])
def salvar():
    data = request.get_json()
    nome  = data.get("nome")
    campo = data.get("campo")
    valor = data.get("valor")
    if not nome or not campo:
        return jsonify({"ok": False, "erro": "dados inválidos"})
    db = load_db()
    p = get_pessoa(db, nome)
    if campo in TIPO_IDS:
        try:
            p[campo] = max(0, int(valor))
        except:
            p[campo] = 0
    elif campo == "valor_pago":
        try:
            p[campo] = float(str(valor).replace(",", "."))
        except:
            p[campo] = 0.0
    else:
        p[campo] = valor
    save_db(db)
    # Retorna totais atualizados
    return jsonify({
        "ok": True,
        "qtd_total":   qtd_total(db, nome),
        "valor_total": round(valor_total(db, nome), 2),
        "resumo": {
            "pediu": sum(1 for n in TODAS_PESSOAS if qtd_total(db, n) > 0),
            "qtd":   sum(qtd_total(db, n) for n in TODAS_PESSOAS),
            "valor": round(sum(valor_total(db, n) for n in TODAS_PESSOAS), 2),
            "vpago": round(sum(get_pessoa(db, n).get("valor_pago", 0) or 0 for n in TODAS_PESSOAS), 2),
            "pago":  sum(1 for n in TODAS_PESSOAS if get_pessoa(db, n).get("status") == "PAGO"),
            "pend":  sum(1 for n in TODAS_PESSOAS if get_pessoa(db, n).get("status") == "PENDENTE"),
            "parc":  sum(1 for n in TODAS_PESSOAS if get_pessoa(db, n).get("status") == "PARCIAL"),
        }
    })

@app.route("/dados")
def dados():
    db = load_db()
    return jsonify(db)

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
