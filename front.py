import streamlit as st
from st_keyup import st_keyup
from bayes import calcular_probabilidade

st.title("Teste de Autocomplete Bayesiano")

user_input = st_keyup(
    label="Comece a digitar uma palavra:",
    placeholder="Ex: ci",
    key="meu_texto",
    debounce=300
)

def desenhar_card(palavra, prob, rank, cor_fundo, cor_texto, altura, margin_top, tamanho_fonte):
    html = f"""
    <div style="
        background-color: {cor_fundo}; 
        color: {cor_texto};
        padding: 10px; 
        border-radius: 8px; 
        text-align: center; 
        height: {altura}px; 
        display: flex; 
        flex-direction: column; 
        justify-content: center;
        margin-top: {margin_top}px; /* Isso cria o efeito de 'degrau' do pódio */
        box-shadow: 2px 2px 10px rgba(0,0,0,0.2);
    ">
        <div style="font-size: 14px; opacity: 0.8;">{rank}º Lugar</div>
        <div style="font-size: {tamanho_fonte}px; font-weight: bold; margin: 5px 0;">{palavra}</div>
        <div style="font-size: 12px;">Probabilidade: {prob*100:.4f}%</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

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
                desenhar_card(p, info['p_palavra'], 2, "#E0E0E0", "#000000", 100, 30, 20)
        
        with col2:
            if len(palavras_validas) >= 1:
                p, info = palavras_validas[0]
                desenhar_card(p, info['p_palavra'], 1, "#FFD700", "#000000", 130, 0, 24)

        with col3:
            if len(palavras_validas) >= 3:
                p, info = palavras_validas[2]
                desenhar_card(p, info['p_palavra'], 3, "#CD7F32", "#000000", 80, 50, 16)
                
        restante = palavras_validas[3:]
        
        if restante:
            st.markdown("---")
            st.subheader("Outras Sugestões")
            for p, info in restante:
                st.write(f"- **{p}** (Probabilidade: {info['p_palavra']*100:.4f}%)")