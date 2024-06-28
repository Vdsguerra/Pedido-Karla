import streamlit as st

# Frase a ser adivinhada
frase = 'KARLA, NAMORA COMIGO?'

# Função para exibir a imagem da fase atual
def img():
    st.image(fases.get(st.session_state.tentativas))

# Título do jogo
st.markdown(
    "<div style='text-align: center; color: white; font-size: 2em;'>Jogo da Forca do Amor</div>", 
    unsafe_allow_html=True
)

# Estilização da interface
st.markdown("""
    <style>
        [data-testid="stAppViewContainer"] > .main {
            background-color: #FF9A8B;
            background-image: linear-gradient(90deg, #FF9A8B 0%, #FF6A88 55%, #FF99AC 100%);
        }
        [data-testid="stHeader"] {
            display: none;
        }
        [data-testid="stSidebar"] {
            display: none;
        }
        [data-testid="stToolbar"] {
            display: none;
        }
    </style>
    """, unsafe_allow_html=True)

# Função para redefinir o jogo
def reset_game():
    st.session_state.tentativas = 7
    st.session_state.letras_adivinhadas = []
    st.session_state.frase_completa = ''.join(['_' if c.isalpha() else c for c in frase])
    st.session_state.frase_acertada = False
    st.experimental_rerun()  # Atualiza a tela após o reset

# Mapear tentativas para imagens
fases = {
    7: "1.png",
    6: "2.png",
    5: "3.png",
    4: "4.png",
    3: "5.png",
    2: "6.png",
    1: "7.png",
    0: "0.png"
}

# Inicializar os estados da sessão
if 'tentativas' not in st.session_state:
    reset_game()

# Função para tocar a música
def tocar_musica():
    st.audio('musica.mp3', autoplay=True)  # Certifique-se de que o arquivo 'musica.mp3' está no mesmo diretório

# Função para processar a letra inserida
def processa_letra():
    input_letra = st.session_state.input_letra.upper()
    if st.session_state.tentativas > 0 and not st.session_state.frase_acertada:
        if len(input_letra) == 1 and input_letra.isalpha():
            if input_letra in st.session_state.letras_adivinhadas:
                st.error(f"Você já adivinhou a letra {input_letra}")
            elif input_letra not in frase:
                st.error(f"{input_letra} não está na palavra.")
                st.session_state.tentativas -= 1
                st.session_state.letras_adivinhadas.append(input_letra)
            else:
                st.success(f"Parabéns, {input_letra} está na frase!")
                index = [i for i, letra in enumerate(frase) if letra == input_letra]
                frase_completa_lista = list(st.session_state.frase_completa)
                for i in index:
                    frase_completa_lista[i] = input_letra
                st.session_state.frase_completa = "".join(frase_completa_lista)
                st.session_state.letras_adivinhadas.append(input_letra)
            img()
            st.session_state.input_letra = ''

        if all(c in st.session_state.letras_adivinhadas or not c.isalpha() for c in frase):
            st.balloons()
            st.success('Parabéns! Você acertou a frase completa!')
            st.session_state.frase_acertada = True
            tocar_musica()

        elif len(input_letra) > 1:
            st.warning("Escreva apenas uma letra.")
        elif input_letra and not input_letra.isalpha():
            st.warning('Digito inválido.')

    if st.session_state.tentativas <= 0 and not st.session_state.frase_acertada:
        st.error('Você perdeu!')
        if st.button("Tentar novamente"):
            reset_game()  # Chama a função para resetar o jogo

    columns = st.columns(len(frase))

    for i, col in enumerate(columns):
        with col:
            if frase[i].isalpha():
                col.write(st.session_state.frase_completa[i])
            else:
                col.write(frase[i])

    st.write("Letras já utilizadas: " + ", ".join(st.session_state.letras_adivinhadas))

# Função principal do jogo
def jogar():
    if not st.session_state.frase_acertada and st.session_state.tentativas > 0:
        st.text_input("Digite uma letra 👇", key="input_letra", on_change=processa_letra).upper()

# Executa o jogo
jogar()
