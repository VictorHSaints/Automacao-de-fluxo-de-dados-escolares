import streamlit as st
from src.config import settings

# Configuração da página Streamlit
st.set_page_config(
    page_title=settings.APP_TITLE,
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    """Ponto de entrada da aplicação Streamlit."""
    
    st.title(settings.APP_TITLE)
    st.markdown("---")
    
    # Menu lateral
    st.sidebar.header("Filtros e Configurações")
    turma_selecionada = st.sidebar.selectbox("Selecione a Turma", ["Turma A", "Turma B"]) # Placeholder
    
    # Abas da aplicação
    tab_visao_geral, tab_visao_aluno = st.tabs(["Visão Geral", "Visão por Aluno"])
    
    with tab_visao_geral:
        st.subheader("Desempenho da Turma")
        # TODO: Chamar funções de src.analytics para popular KPIs e Gráficos
        st.info("Gráficos de evolução e médias gerais serão renderizados aqui.")
        
    with tab_visao_aluno:
        st.subheader("Boletim Analítico do Aluno")
        # TODO: Permitir seleção de aluno e mostrar radar de disciplinas
        st.info("Comparativo do aluno com a turma e foco para o vestibular será renderizado aqui.")
        if st.button("Gerar PDF do Aluno"):
            # TODO: Chamar src.export.pdf_generator
            st.success("PDF gerado com sucesso!")

if __name__ == "__main__":
    main()
