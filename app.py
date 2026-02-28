import os
import psycopg2
from psycopg2.extras import RealDictCursor, Json
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
DATABASE_URL = os.environ.get('DATABASE_URL')

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS pedidos (nome TEXT PRIMARY KEY, dados JSONB);')
    conn.commit()
    cur.close()
    conn.close()

init_db()

TIPOS = [
    ("adulto_mestre", "Mestre Adulto", 14.45), ("adulto_mestre_cd", "Mestre Adulto C.Dura", 28.05),
    ("adulto_aluno", "Aluno Adulto", 9.60), ("jovem_mestre", "Mestre Jovem", 14.45),
    ("jovem_aluno", "Aluno Jovem", 9.60), ("pre_adol_aluno", "Pré-Adol. Aluno", 9.60),
    ("pre_adol_prof", "Pre-Adol. Prof.", 14.45), ("primarios_aluno", "Primários Aluno", 8.00),
    ("primarios_prof", "Primários Prof.", 14.45), ("maternal_aluno", "Maternal Aluno", 8.00),
    ("maternal_prof", "Maternal Prof.", 14.45), ("livro_apoio", "Livro Apoio Jov./Ad.", 17.95)
]
TIPO_IDS = [t[0] for t in TIPOS]
TIPO_PRECO = {t[0]: t[2] for t in TIPOS}

TODAS_PESSOAS = sorted(["ABNER BERNARDO","AGATHA HADASSA","ANA ESTHER","ANA LÍVIA CASTRO","ANA PALOMA","ANA SOPHIA","ANDRESSA SILVA","ANTONIO JORGE","ANTTONY ICARO","APOLLO PAZ","ARLIAN FERREIRA","ARLINDO DE OLIVEIRA","BRUNA LOHANNA","CATARINA AMARANTE","CATIA FREITAS","CEZIANE","CINDY BARROS MARTINS","CLARYSSA BIANCA","DANIELA DE PAULA","DAVINIEL NOBRE","DELAIDE PROCÓPIO","DIANA GOMES","EDUARDA CASTRO","EDUARDO BEZERRA","ENEAS CARLOS","ERICK NUNES","ESTEVÃO CIPRIANO","ESTEVÃO MARQUES","ETHAN DE CASTRO","EVANIR ARAÚJO","EVERINA AMARANTE","FELIPE ARAÚJO","FELIPE BARRETO","FRANCIMAR (LUCIANA)","GABRIEL SOUSA","GEANE MARIA","GILSON VIRGÍNIO","HERIC LIMA","IANNY ALENCAR","ISAAC MORAES","ISAIAS MORAIS","JADY AMARANTE","JASMINE","JAYANE AMARANTE","JOABE ARAÚJO","JOÃO B. ARCANJO","JOÃO B. FERREIRA","JOÃO MARCOS","JOÃO MARCOS MARQUES","JOÃO MARKUS","JOÃO PAULO","JOÃO PROCÓPIO","JOSÉ IVO","JOSÉ NILSON XAVIER MARTINS","JUACI MARTINS","KAEL ARAÚJO","KAILY ANSELMO","KAUAN MARQUES","LAURA BEATRIZ","LEIDIANY ROBERTA","LENISA CASTRO","LIDIANE DO AMARANTE","LOURENÇO LUCAS","LUCAS SALES","LUCILENE SALLES","LUIS RICARDO","LUIZ NETO","MANUELA BERNARDO","MARCELLE VÍRNIA","MARCILIO VICTOR","MARCOS ANTÔNIO","MARIA EMANUELE","MARIA LOPES (ELITA)","MARESSA ROCHA","MARNIA VICTORIA","MICHELE MARQUES","MILKA KÉSIA","NAZARÉ MARQUES","NILSON MARTINS","OLIVER ROCHA","PAULLYANE PAZ","PAULO PAZ","PEDRO PAULO","RAISSA CASTRO","RAKELLY LOPES","RAIMUNDO DE FREITAS (RAY)","RAYLSON FERREIRA","REGIANE ALCÂNTARA","RONIELE MARQUES","SILVERIA CALDAS","YVANA GOMES"])

FAMILIAS = [
    {"nome":"Família Isaías Morais", "membros":["ISAIAS MORAIS","ISAAC MORAES","LEIDIANY ROBERTA"]},
    {"nome":"Família Marcelle Vírnia", "membros":["MARCELLE VÍRNIA","MARCILIO VICTOR","MARNIA VICTORIA","ANA SOPHIA"]},
    {"nome":"Família Daniela de Paula", "membros":["DANIELA DE PAULA","JOÃO MARCOS"]},
    {"nome":"Família Marcos Antônio/Michele", "membros":["MARCOS ANTÔNIO","MICHELE MARQUES","JOÃO MARCOS MARQUES","ESTEVÃO MARQUES"]},
    {"nome":"Família Juaci Martins", "membros":["JUACI MARTINS","REGIANE ALCÂNTARA","GEANE MARIA"]},
    {"nome":"Família Gilson Virgínio", "membros":["GILSON VIRGÍNIO","ANA ESTHER"]},
    {"nome":"Família Felipe Araújo", "membros":["FELIPE ARAÚJO","YVANA GOMES","KAILY ANSELMO","KAEL ARAÚJO"]},
    {"nome":"Núcleo Diana Gomes", "membros":["DIANA GOMES","AGATHA HADASSA","LOURENÇO LUCAS"]},
    {"nome":"Família Nazaré Marques", "membros":["NAZARÉ MARQUES","RONIELE MARQUES","KAUAN MARQUES"]},
    {"nome":"Família Lidiane do Amarante", "membros":["LIDIANE DO AMARANTE","LAURA BEATRIZ"]},
    {"nome":"Família Lenisa Castro", "membros":["LENISA CASTRO","ETHAN DE CASTRO","ANA LÍVIA CASTRO"]},
    {"nome":"Família Felipe Barreto", "membros":["FELIPE BARRETO","RAISSA CASTRO"]},
    {"nome":"Família Paulo Paz", "membros":["PAULO PAZ","CEZIANE","APOLLO PAZ","PAULLYANE PAZ"]},
    {"nome":"Família José Ivo", "membros":["JOSÉ IVO","JASMINE","JAYANE AMARANTE","JADY AMARANTE","DAVINIEL NOBRE"]},
    {"nome":"Família Lucilene Salles", "membros":["LUCILENE SALLES","LUCAS SALES"]},
    {"nome":"Família Arlian Ferreira", "membros":["ARLIAN FERREIRA","MARESSA ROCHA","OLIVER ROCHA"]},
    {"nome":"Núcleo Eduarda Castro", "membros":["EDUARDA CASTRO","ERICK NUNES"]},
    {"nome":"Família Silvéria Caldas", "membros":["SILVERIA CALDAS","ENEAS CARLOS"]},
    {"nome":"Família Arlindo de Oliveira", "membros":["ARLINDO DE OLIVEIRA","ANDRESSA SILVA"]},
    {"nome":"Família Nilson Martins", "membros":["NILSON MARTINS","CINDY BARROS MARTINS"]},
    {"nome":"Família Batista Ferreira", "membros":["CATIA FREITAS","CLARYSSA BIANCA","JOÃO B. FERREIRA"]},
    {"nome":"Família Raimundo (Ray)", "membros":["RAIMUNDO DE FREITAS (RAY)","ABNER BERNARDO","MANUELA BERNARDO"]},
    {"nome":"Família Milka Késia", "membros":["MILKA KÉSIA","EDUARDO BEZERRA"]},
]

_m_fam = {m for f in FAMILIAS for m in f["membros"]}
SOLTOS = sorted([p for p in TODAS_PESSOAS if p not in _m_fam])

@app.route("/")
def index():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT * FROM pedidos')
    rows = cur.fetchall()
    db = {row['nome']: row['dados'] for row in rows}
    cur.close()
    conn.close()
    
    pessoas_data =
    
