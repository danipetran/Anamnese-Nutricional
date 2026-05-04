import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# ------------------------
# CONEXÃO COM GOOGLE SHEETS
# ------------------------
def conectar_planilha():
    creds_dict = st.secrets["gcp_service_account"]

    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)

    return client.open_by_url(
        "https://docs.google.com/spreadsheets/d/1mDGFuicx51n6edgRvMGy09m94M0UYYY39ZfkTzHwCEc/edit?usp=sharing"
    ).sheet1


# ------------------------
# CONFIG
# ------------------------
st.set_page_config(page_title="Anamnese - Dani", page_icon="📋")

if "pagina" not in st.session_state:
    st.session_state.pagina = "formulario"


# ------------------------
# FORMULÁRIO
# ------------------------
if st.session_state.pagina == "formulario":

    st.title("📋 Anamnese Nutricional")
    st.markdown("Preencha com atenção para seu plano personalizado 💛")

    # Dados pessoais
    nome = st.text_input("Nome completo")
    idade = st.number_input("Idade", min_value=0)
    altura = st.number_input("Altura (cm)", min_value=0.0)
    peso_atual = st.number_input("Peso atual (kg)", min_value=0.0)
    peso_desejado = st.number_input("Peso desejado (kg)", min_value=0.0)
    profissao = st.text_input("Profissão")
    rotina_trabalho = st.text_area("Rotina de trabalho")

    # Objetivo
    objetivo = st.selectbox("Objetivo", [
        "Emagrecimento", "Ganho de massa", "Definição", "Saúde", "Outro"
    ])
    prazo = st.text_input("Prazo")

    # Saúde
    saude = st.multiselect("Condições", [
        "Gastrite","Ansiedade","Compulsão","Diabetes",
        "Hipotireoidismo","Intestino preso","Intestino solto","Nenhum","Outro"
    ])
    medicamentos = st.text_input("Medicamentos")
    ja_dieta = st.radio("Já fez dieta?", ["Sim","Não"])
    qual_dieta = st.text_area("Qual dieta?")

    # Rotina alimentar
    hora_acorda = st.text_input("Hora que acorda")
    hora_dorme = st.text_input("Hora que dorme")
    rotina_alimentar = st.text_area("Rotina alimentar")

    # Relação com comida
    come_por = st.radio("Come por", ["Fome","Emoção","Ambos"])
    compulsao = st.radio("Compulsão", ["Sim","Não","Às vezes"])
    desafio = st.selectbox("Maior desafio", [
        "Ansiedade","Falta de tempo","Doce","Disciplina","Outro"
    ])

    # Exercício
    faz_exercicio = st.radio("Faz exercício?", ["Sim","Não"])
    qual_exercicio = st.text_input("Qual exercício")
    dias_semana = st.text_input("Dias por semana")
    horario_treino = st.text_input("Horário treino")

    # Água e sono
    agua = st.selectbox("Água", ["<1L","1L","2L",">2L"])
    horas_sono = st.text_input("Horas de sono")
    acorda_cansado = st.radio("Acorda cansado?", ["Sim","Não"])
    dificuldade_dormir = st.radio("Dificuldade dormir?", ["Sim","Não"])

    # Preferências
    gosta = st.text_area("Alimentos que gosta")
    nao_gosta = st.text_area("Alimentos que não gosta")
    alergia = st.text_input("Alergia")

    # Rotina real
    come_fora = st.radio("Come fora?", ["Sim","Não"])
    tempo_cozinhar = st.radio("Tem tempo para cozinhar?", ["Sim","Não"])
    tipo_dieta = st.selectbox("Tipo de dieta", ["Simples","Variada","Rápida"])

    # Comprometimento
    comprometimento = st.slider("Comprometimento", 0, 10)

    # Expectativa
    expectativa = st.text_area("Expectativa")

    # ------------------------
    # BOTÃO
    # ------------------------
    if st.button("Enviar Anamnese 💛"):

        if not nome:
            st.warning("Por favor, preencha seu nome.")
            st.stop()

        with st.spinner("Enviando sua anamnese..."):

            sheet = conectar_planilha()

            dados = [
                nome, idade, altura, peso_atual, peso_desejado,
                profissao, rotina_trabalho, objetivo, prazo,
                ", ".join(saude), medicamentos, ja_dieta, qual_dieta,
                hora_acorda, hora_dorme, rotina_alimentar,
                come_por, compulsao, desafio,
                faz_exercicio, qual_exercicio, dias_semana, horario_treino,
                agua, horas_sono, acorda_cansado, dificuldade_dormir,
                gosta, nao_gosta, alergia,
                come_fora, tempo_cozinhar, tipo_dieta,
                comprometimento, expectativa
            ]

            sheet.append_row(dados)

            st.session_state.dados_enviados = dados
            st.session_state.pagina = "sucesso"

            st.rerun()


# ------------------------
# PÁGINA DE SUCESSO
# ------------------------
if st.session_state.pagina == "sucesso":

    st.title("💛 Anamnese enviada com sucesso!")
    st.subheader("Resumo das suas respostas:")

    labels = [
        "Nome", "Idade", "Altura", "Peso Atual", "Peso Desejado",
        "Profissão", "Rotina Trabalho", "Objetivo", "Prazo", "Saúde",
        "Medicamentos", "Já fez dieta", "Qual dieta",
        "Hora acorda", "Hora dorme", "Rotina alimentar",
        "Come por", "Compulsão", "Desafio",
        "Faz exercício", "Qual exercício", "Dias por semana", "Horário treino",
        "Água", "Horas de sono", "Acorda cansado", "Dificuldade dormir",
        "Alimentos gosta", "Alimentos não gosta", "Alergia",
        "Come fora", "Tempo cozinhar", "Tipo dieta",
        "Comprometimento", "Expectativa"
    ]

    dados = st.session_state.get("dados_enviados", [])

    for label, valor in zip(labels, dados):
        st.write(f"**{label}:** {valor}")

    st.markdown("---")

    if st.button("Nova Anamnese"):
        st.session_state.pagina = "formulario"
        st.rerun()
