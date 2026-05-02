import streamlit as st

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st

def conectar_planilha():
    # 👇 AQUI entra o secrets
    creds_dict = st.secrets["gcp_service_account"]

    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)

    return client.open("Anamnese Clientes").sheet1

st.set_page_config(page_title="Anamnese - Dani", page_icon="📋")

st.title("📋 Anamnese Nutricional")
st.markdown("Preencha com atenção para seu plano personalizado 💛")

# ------------------------
# DADOS PESSOAIS
# ------------------------
st.header("🧍‍♀️ Dados pessoais")

nome = st.text_input("Nome completo")
idade = st.text_input("Idade")
altura = st.text_input("Altura")
peso = st.text_input("Peso atual")
peso_desejado = st.text_input("Peso desejado")
profissao = st.text_input("Profissão")
rotina = st.text_area("Como é sua rotina de trabalho?")

# ------------------------
# OBJETIVO
# ------------------------
st.header("🎯 Objetivo")

objetivo = st.radio("Qual seu objetivo principal?", [
    "Emagrecimento",
    "Ganho de massa muscular",
    "Definição corporal",
    "Saúde geral",
    "Melhorar alimentação",
    "Outro"
])

tempo_objetivo = st.text_input("Em quanto tempo deseja atingir?")

# ------------------------
# SAÚDE
# ------------------------
st.header("🩺 Saúde")

condicoes = st.multiselect("Você possui algum desses?", [
    "Gastrite", "Ansiedade", "Compulsão alimentar",
    "Diabetes", "Hipotireoidismo", "Intestino preso",
    "Intestino solto", "Nenhum", "Outro"
])

medicamentos = st.text_input("Faz uso de medicamentos?")

dieta = st.radio("Já fez dieta antes?", ["Sim", "Não"])

dieta_desc = st.text_area("Se sim, qual foi e funcionou?")

# ------------------------
# ROTINA ALIMENTAR
# ------------------------
st.header("🍽️ Rotina alimentar")

acorda = st.text_input("Horário que acorda")
dorme = st.text_input("Horário que dorme")
alimentacao = st.text_area("Descreva um dia da sua alimentação")

# ------------------------
# RELAÇÃO COM COMIDA
# ------------------------
st.header("⚠️ Relação com a comida")

come_por = st.radio("Você come mais por:", ["Fome", "Emoção", "Ambos"])
compulsao = st.radio("Tem compulsão?", ["Sim", "Não", "Às vezes"])
desafio = st.radio("Seu maior desafio é:", [
    "Ansiedade", "Falta de tempo", "Vontade de doce",
    "Falta de disciplina", "Outro"
])

# ------------------------
# ATIVIDADE FÍSICA
# ------------------------
st.header("🏋️‍♀️ Atividade física")

treina = st.radio("Pratica exercício?", ["Sim", "Não"])
tipo_treino = st.text_input("Qual exercício?")
dias = st.text_input("Quantos dias por semana?")
horario = st.text_input("Horário do treino")

# ------------------------
# ÁGUA
# ------------------------
st.header("💧 Água")

agua = st.radio("Quanto bebe por dia?", [
    "Menos de 1L", "1L", "2L", "Mais de 2L"
])

# ------------------------
# SONO
# ------------------------
st.header("😴 Sono")

sono = st.text_input("Quantas horas dorme?")
cansado = st.radio("Acorda cansado?", ["Sim", "Não"])
dificuldade = st.radio("Dificuldade para dormir?", ["Sim", "Não"])

# ------------------------
# PREFERÊNCIAS
# ------------------------
st.header("🍫 Preferências")

gosta = st.text_area("Alimentos que gosta")
nao_gosta = st.text_area("Alimentos que não gosta")
alergia = st.text_input("Possui alergia ou intolerância?")

# ------------------------
# ROTINA REAL
# ------------------------
st.header("🍕 Rotina real")

fora = st.radio("Come fora?", ["Sim", "Não"])
cozinhar = st.radio("Tem tempo para cozinhar?", ["Sim", "Não"])
tipo_dieta = st.radio("Prefere dieta:", ["Simples", "Variada", "Rápida"])

# ------------------------
# COMPROMETIMENTO
# ------------------------
st.header("🧠 Comprometimento")

compromisso = st.slider("Quanto está disposto (0-10)?", 0, 10)

# ------------------------
# EXPECTATIVA
# ------------------------
st.header("💬 Expectativa")

expectativa = st.text_area("O que você espera do plano?")

# ------------------------
# BOTÃO FINAL
# ------------------------
if st.button("Enviar Anamnese 💛"):

    sheet = conectar_planilha()

    sheet.append_row([
        nome,
        idade,
        altura,
        peso,
        peso_desejado,
        objetivo
    ])

    st.success("Recebido! 💛")
