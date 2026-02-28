import os
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Conexão com o Banco de Dados que você criou no Render
DATABASE_URL = os.environ.get('DATABASE_URL')

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

# Criar a tabela se ela não existir (A mágica acontece aqui)
def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS pedidos (
            nome TEXT PRIMARY KEY,
            dados JSONB
        );
    ''')
    conn.commit()
    cur.close()
    conn.close()

init_db()

TIPOS = [
    ("adulto_mestre", "Mestre Adulto", 14.45),
    ("adulto_mestre_cd", "Mestre Adulto C.Dura", 28.05),
    ("adulto_aluno", "Aluno Adulto", 9.60),
    ("jovem_mestre", "Mestre Jovem", 14.45),
    ("jovem_aluno", "Aluno Jovem", 9.60),
    ("pre_adol_aluno", "Pré-Adol. Aluno", 9.60),
    ("pre_adol_prof", "Pré-Adol. Prof.", 14.45),
    ("primarios_aluno", "Primários Aluno", 8.00),
    ("primarios_prof", "Primários Prof.", 14.45),
    ("maternal_aluno", "Maternal Aluno", 8.00),
    ("maternal_prof", "Maternal Prof.", 14.45),
    ("livro_apoio", "Livro Apoio Jov./Ad.", 17.95),
]
TIPO_IDS = [t[0] for t in TIPOS]
TIPO_PRECO = {t[0]: t[2] for t in TIPOS}

TODAS_PESSOAS = sorted(["ABNER BERNARDO","AGATHA HADASSA","ANA ESTHER","ANA LÍVIA CASTRO","ANA PALOMA","ANA SOPHIA","ANDRESSA SILVA","ANTONIO JORGE","ANTTONY ICARO","APOLLO PAZ","ARLIAN FERREIRA","ARLINDO DE OLIVEIRA","BRUNA LOHANNA","CATARINA AMARANTE","CATIA FREITAS","CEZIANE","CINDY BARROS MARTINS","CLARYSSA BIANCA","DANIELA DE PAULA","DAVINIEL NOBRE","DELAIDE PROCÓPIO","DIANA GOMES","EDUARDA CASTRO","EDUARDO BEZERRA","ENEAS CARLOS","ERICK NUNES","ESTEVÃO CIPRIANO","ESTEVÃO MARQUES","ETHAN DE CASTRO","EVANIR ARAÚJO","EVERINA AMARANTE","FELIPE ARAÚJO","FELIPE BARRETO","FRANCIMAR (LUCIANA)","GABRIEL SOUSA","GEANE MARIA","GILSON VIRGÍNIO","HERIC LIMA","IANNY ALENCAR","ISAAC MORAES","ISAIAS MORAIS","JADY AMARANTE","JASMINE","JAYANE AMARANTE","JOABE ARAÚJO","JOÃO B. ARCANJO","JOÃO B. FERREIRA","JOÃO MARCOS","JOÃO MARCOS MARQUES","JOÃO MARKUS","JOÃO PAULO","JOÃO PROCÓPIO","JOSÉ IVO","JOSÉ NILSON XAVIER MARTINS","JUACI MARTINS","KAEL ARAÚJO","KAILY ANSELMO","KAUAN MARQUES","LAURA BEATRIZ","LEIDIANY ROBERTA","LENISA CASTRO","LIDIANE DO AMARANTE","LOURENÇO LUCAS","LUCAS SALES","LUCILENE SALLES","LUIS RICARDO","LUIZ NETO","MANUELA BERNARDO","MARCELLE VÍRNIA","MARCILIO VICTOR","MARCOS ANTÔNIO","MARIA EMANUELE","MARIA LOPES (ELITA)","MARESSA ROCHA","MARNIA VICTORIA","MICHELE MARQUES","MILKA KÉSIA","NAZARÉ MARQUES","NILSON MARTINS","OLIVER ROCHA","PAULLYANE PAZ","PAULO PAZ","PEDRO PAULO","RAISSA CASTRO","RAKELLY LOPES","RAIMUNDO DE FREITAS (RAY)","RAYLSON FERREIRA","REGIANE ALCÂNTARA","RONIELE MARQUES","SILVERIA CALDAS","YVANA GOMES"])

@app.route("/")
def index():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT * FROM pedidos')
    rows = cur.fetchall()
    db = {row['nome']: row['dados'] for row in rows}
    cur.close()
    conn.close()

    pessoas_data = {}
    for nome in TODAS_PESSOAS:
        p = db.get(nome, {})
        data_p = {tid: p.get(tid, 0) for tid in TIPO_IDS}
        data_p.update({
            "status": p.get("status", ""),
            "forma": p.get("forma", ""),
            "valor_pago": p.get("valor_pago", 0),
            "data": p.get("data", ""),
            "qtd_total": sum(p.get(tid, 0) for tid in TIPO_IDS),
            "valor_total": sum(p.get(tid, 0) * TIPO_PRECO[tid] for tid in TIPO_IDS)
        })
        pessoas_data[nome] = data_p

    return render_template("index.html", tipos=TIPOS, pessoas=TODAS_PESSOAS, pessoas_data=pessoas_data)

@app.route("/salvar", methods=["POST"])
def salvar():
    req = request.get_json()
    nome = req.get("nome")
    campo = req.get("campo")
    valor = req.get("valor")

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT dados FROM pedidos WHERE nome = %s', (nome,))
    res = cur.fetchone()
    
    p = res['dados'] if res else {tid: 0 for tid in TIPO_IDS}
    if not res:
        p.update({"status": "", "forma": "", "valor_pago": 0, "data": ""})

    if campo in TIPO_IDS: p[campo] = int(valor)
    elif campo == "valor_pago": p[campo] = float(str(valor).replace(",", "."))
    else: p[campo] = valor

    cur.execute('''
        INSERT INTO pedidos (nome, dados) VALUES (%s, %s)
        ON CONFLICT (nome) DO UPDATE SET dados = EXCLUDED.dados
    ''', (nome, psycopg2.extras.Json(p)))
    
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"ok": True})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
