import time
import streamlit as st
from string import Template
from st_keyup import st_keyup
from bayes import calcular_probabilidade

if "ultimo_prefixo" not in st.session_state:
    st.session_state.ultimo_prefixo = ""
if "ultimas_palavras" not in st.session_state:
    st.session_state.ultimas_palavras = []

def carregar_css(caminho):
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass 

def desenhar_card(palavra, prob, rank, cor_fundo, cor_texto, altura, margin_top, tamanho_fonte, delay_card, delay_texto, prefixo, saindo=False):
    with open("templates/card.html", "r", encoding="utf-8") as f:
        template = Template(f.read())
        
    key_id = f"{prefixo}_{rank}_{palavra}".replace("+", "plus").replace(" ", "_")

    if saindo:
        animacao_card = f"animCardSair_{key_id} 0.25s ease forwards"
        animacao_texto = f"animTextoSair_{key_id} 0.15s ease forwards"
        opacidade_inicial = "1"
    else:
        animacao_card = f"animCardEntrar_{key_id} 0.45s cubic-bezier(0.25, 1, 0.5, 1) {delay_card}s forwards"
        animacao_texto = f"animTextoEntrar_{key_id} 0.25s ease {delay_texto}s forwards"
        opacidade_inicial = "0"

    html_preenchido = template.substitute(
        cor_fundo=cor_fundo, cor_texto=cor_texto, altura=altura, margin_top=margin_top,
        animacao_card=animacao_card, animacao_texto=animacao_texto, opacidade_inicial=opacidade_inicial,
        rank=rank, tamanho_fonte=tamanho_fonte, palavra=palavra, prob=f"{prob*100:.4f}%", key_id=key_id
    )
    st.markdown(html_preenchido, unsafe_allow_html=True)


def renderizar_podio(palavras, prefixo, saindo=False):
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col1:
        if len(palavras) >= 2:
            desenhar_card(palavras[1][0], palavras[1][1]['p_palavra'], 2, "#E0E0E0", "#000000", 100, 30, 20, 0.05, 0.35, prefixo, saindo)
    with col2:
        if len(palavras) >= 1:
            desenhar_card(palavras[0][0], palavras[0][1]['p_palavra'], 1, "#FFD700", "#000000", 130, 0, 24, 0.15, 0.45, prefixo, saindo)
    with col3:
        if len(palavras) >= 3:
            desenhar_card(palavras[2][0], palavras[2][1]['p_palavra'], 3, "#CD7F32", "#000000", 80, 50, 16, 0.00, 0.25, prefixo, saindo)


st.title("Teste de Autocomplete Bayesiano")
carregar_css("style.css")

user_input = st_keyup(label="Comece a digitar uma palavra:", placeholder="Ex: ci", key="meu_texto", debounce=300)
prefixo_atual = user_input.strip().lower() if user_input else ""

podio_placeholder = st.empty()
lista_placeholder = st.empty()

if prefixo_atual != st.session_state.ultimo_prefixo:
    
    if st.session_state.ultimas_palavras:
        with podio_placeholder.container():
            st.write("### 🏆 Ranking de Predição")
            renderizar_podio(st.session_state.ultimas_palavras, st.session_state.ultimo_prefixo, saindo=True)
        
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
            renderizar_podio(palavras_atuais, prefixo, saindo=False)
            
        restante = palavras_atuais[3:]
        if restante:
            with lista_placeholder.container():
                st.markdown("---")
                st.subheader("Outras Sugestões")
                for p, info in restante:
                    st.write(f"- **{p}** (Probabilidade: {info['p_palavra']*100:.4f}%)")