import time
import streamlit as st
from string import Template
from st_keyup import st_keyup
from bayes import calcular_probabilidade

if "selecionado" in st.query_params:
    palavra_clicada = st.query_params["selecionado"]
    st.session_state["meu_texto"] = palavra_clicada
    st.query_params.clear()
    st.rerun()

if "ultimo_prefixo" not in st.session_state:
    st.session_state.ultimo_prefixo = ""
if "ultimas_palavras" not in st.session_state:
    st.session_state.ultimas_palavras = []
if "meu_texto" not in st.session_state:
    st.session_state.meu_texto = ""

def carregar_css(caminho):
    with open(caminho, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def desenhar_card(palavra, prob, rank, cor_fundo, cor_texto, altura, margin_top, tamanho_fonte, delay_card, delay_texto, saindo=False):
    with open("templates/card.html", "r", encoding="utf-8") as f:
        template = Template(f.read())
        
    if saindo:
        animacao_card = "animCardSair 0.25s ease forwards"
        animacao_texto = "animTextoSair 0.15s ease forwards"
        opacidade_inicial = "1"
    else:
        animacao_card = f"animCardEntrar 0.45s cubic-bezier(0.25, 1, 0.5, 1) {delay_card}s forwards"
        animacao_texto = f"animTextoEntrar 0.25s ease {delay_texto}s forwards"
        opacidade_inicial = "0"

    html_preenchido = template.substitute(
        cor_fundo=cor_fundo,
        cor_texto=cor_texto,
        altura=altura,
        margin_top=margin_top,
        animacao_card=animacao_card,
        animacao_texto=animacao_texto,
        opacidade_inicial=opacidade_inicial,
        rank=rank,
        tamanho_fonte=tamanho_fonte,
        palavra=palavra,
        prob=f"{prob*100:.4f}%"
    )
    st.markdown(html_preenchido, unsafe_allow_html=True)

def renderizar_podio(palavras, saindo=False):
    col1, col2, col3 = st.columns([1, 1.2, 1])
    
    gradiente_prata = "linear-gradient(135deg, #1C2026 0%, #525B68 30%, #9AA5B5 50%, #525B68 70%, #161A1F 100%)"
    
    gradiente_ouro = "linear-gradient(135deg, #3A2E0B 0%, #A3801D 30%, #E6C260 50%, #A3801D 70%, #2A2107 100%)"
    
    gradiente_bronze = "linear-gradient(135deg, #2B1810 0%, #753E27 30%, #BA6E4C 50%, #753E27 70%, #21120B 100%)"
    
    with col1:
        if len(palavras) >= 2:
            desenhar_card(palavras[1][0], palavras[1][1]['p_palavra'], 2, gradiente_prata, "#EAEFF5", 100, 30, 20, 0.05, 0.35, saindo)
            
    with col2:
        if len(palavras) >= 1:
            desenhar_card(palavras[0][0], palavras[0][1]['p_palavra'], 1, gradiente_ouro, "#FFF5D1", 130, 0, 24, 0.15, 0.45, saindo)

    with col3:
        if len(palavras) >= 3:
            desenhar_card(palavras[2][0], palavras[2][1]['p_palavra'], 3, gradiente_bronze, "#FFDACC", 80, 50, 16, 0.00, 0.25, saindo)

st.title("Teste de Autocomplete Bayesiano")
carregar_css("style.css")

user_input = st_keyup(
    label="Comece a digitar uma palavra:", 
    placeholder="Ex: ci", 
    value=st.session_state.meu_texto,
    key="meu_texto", 
    debounce=300
)

prefixo_atual = user_input.strip().lower() if user_input else ""

podio_placeholder = st.empty()
lista_placeholder = st.empty()

if prefixo_atual != st.session_state.ultimo_prefixo:
    if st.session_state.ultimas_palavras:
        with podio_placeholder.container():
            st.write("### 🏆 Ranking de Predição")
            renderizar_podio(st.session_state.ultimas_palavras, saindo=True)
        
        time.sleep(0.25)
        podio_placeholder.empty()
        lista_placeholder.empty()

    palavras_validas = []
    if prefixo_atual:
        probabilidades = calcular_probabilidade(prefixo_atual)
        palavras_validas = [(p, i) for p, i in probabilidades if i['verossimilhanca']]
    
    st.session_state.ultimo_prefixo = prefixo_atual
    st.session_state.ultimas_palavras = palavras_validas

palavras_atuais = st.session_state.ultimas_palavras
prefixo = st.session_state.ultimo_prefixo

if prefixo:
    if not palavras_atuais:
        podio_placeholder.warning("Nenhuma palavra encontrada no dataset para este prefixo.")
    else:
        with podio_placeholder.container():
            st.write("### 🏆 Ranking de Predição")
            renderizar_podio(palavras_atuais, saindo=False)
            
        restante = palavras_atuais[3:]
        if restante:
            with lista_placeholder.container():
                st.markdown("---")
                st.subheader("Outras Sugestões")
                for p, info in restante:
                    st.write(f"- **{p}** (Probabilidade: {info['p_palavra']*100:.4f}%)")