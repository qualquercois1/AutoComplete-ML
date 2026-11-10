import streamlit as st
from string import Template
from st_keyup import st_keyup
from bayes import calcular_probabilidade

def carregar_css(caminho):
    with open(caminho, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def desenhar_card(palavra, prob, rank, cor_fundo, cor_texto, altura, margin_top, tamanho_fonte, delay_card, delay_texto):
    with open("templates/card.html", "r", encoding="utf-8") as f:
        template = Template(f.read())
        
    html_preenchido = template.substitute(
        cor_fundo=cor_fundo,
        cor_texto=cor_texto,
        altura=altura,
        margin_top=margin_top,
        delay_card=delay_card,
        delay_texto=delay_texto,
        rank=rank,
        tamanho_fonte=tamanho_fonte,
        palavra=palavra,
        prob=f"{prob*100:.4f}%"
    )
    
    st.markdown(html_preenchido, unsafe_allow_html=True)

st.title("Teste de Autocomplete Bayesiano")

carregar_css("style.css")

user_input = st_keyup(
    label="Comece a digitar uma palavra:",
    placeholder="Ex: ci",
    key="meu_texto",
    debounce=300
)

if user_input and user_input.strip():
    prefixo = user_input.strip().lower() 
    probabilidades = calcular_probabilidade(prefixo)
    
    palavras_validas = [(p, i) for p, i in probabilidades if i['verossimilhanca']]
    
    if not palavras_validas:
        st.warning("Nenhuma palavra encontrada no dataset para este prefixo.")
    else:
        st.write("### 🏆 Ranking de Predição")
        
        col1, col2, col3 = st.columns([1, 1.2, 1])
        
        with col1:
            if len(palavras_validas) >= 2:
                p, info = palavras_validas[1]
                desenhar_card(p, info['p_palavra'], 2, "#E0E0E0", "#000000", 100, 30, 20, 0.2, 0.50)
        
        with col2:
            if len(palavras_validas) >= 1:
                p, info = palavras_validas[0]
                desenhar_card(p, info['p_palavra'], 1, "#FFD700", "#000000", 130, 0, 24, 0.4, 0.70)

        with col3:
            if len(palavras_validas) >= 3:
                p, info = palavras_validas[2]
                desenhar_card(p, info['p_palavra'], 3, "#CD7F32", "#000000", 80, 50, 16, 0.0, 0.30)
                
        restante = palavras_validas[3:]
        if restante:
            st.markdown("---")
            st.subheader("Outras Sugestões")
            for p, info in restante:
                st.write(f"- **{p}** (Probabilidade: {info['p_palavra']*100:.4f}%)")