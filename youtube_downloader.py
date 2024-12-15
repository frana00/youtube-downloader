import streamlit as st
import subprocess
import sys
import tempfile
import os

# Configuración de la página
st.set_page_config(
    page_title="YouTube Downloader",
    page_icon="📺",
    layout="centered"
)

# Estilos CSS personalizados
st.markdown("""
    <style>
        .stButton>button {
            width: 100%;
            background-color: #FF0000;
            color: white;
        }
        .stButton>button:hover {
            background-color: #CC0000;
            color: white;
        }
        .download-button {
            background-color: #28a745 !important;
        }
    </style>
""", unsafe_allow_html=True)

def install_dependencies():
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "yt-dlp"], 
                      check=True, capture_output=True)
    except Exception as e:
        st.error(f"Error instalando dependencias: {str(e)}")

def get_video_info(url):
    try:
        comando = [
            'yt-dlp',
            '--get-title',
            '--get-duration',
            url
        ]
        resultado = subprocess.run(comando, capture_output=True, text=True)
        info = resultado.stdout.strip().split('\n')
        return {
            'title': info[0] if len(info) > 0 else 'No disponible',
            'duration': info[1] if len(info) > 1 else 'No disponible'
        }
    except:
        return None

def download_video(url, download_audio_only=False):
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            output_template = os.path.join(temp_dir, '%(title)s.%(ext)s')

            if download_audio_only:
                comando = [
                    'yt-dlp',
                    '-x',
                    '--audio-format', 'mp3',
                    '-o', output_template,
                    '--no-warnings',
                    url
                ]
                extension = 'mp3'
            else:
                comando = [
                    'yt-dlp',
                    '-o', output_template,
                    '--no-warnings',
                    url
                ]
                extension = 'mp4'

            # Mostrar barra de progreso
            progress_bar = st.progress(0)
            status_text = st.empty()

            process = subprocess.Popen(
                comando,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )

            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    if '[download]' in output and '%' in output:
                        try:
                            percent = float(output.split('%')[0].split()[-1])
                            progress_bar.progress(percent / 100)
                            status_text.text(f"Descargando: {percent:.1f}%")
                        except:
                            continue

            if process.returncode == 0:
                archivo = [f for f in os.listdir(temp_dir)][0]
                archivo_path = os.path.join(temp_dir, archivo)

                with open(archivo_path, 'rb') as file:
                    archivo_bytes = file.read()

                status_text.text("¡Archivo listo para descargar! 🎉")
                st.balloons()

                st.download_button(
                    label="📥 Guardar archivo",
                    data=archivo_bytes,
                    file_name=archivo,
                    mime=f"{'audio' if download_audio_only else 'video'}/{extension}",
                    key='download_button'
                )
                return True
            else:
                st.error(f"Error en la descarga: {process.stderr.read()}")
                return False

    except Exception as e:
        st.error(f"Error: {str(e)}")
        return False

def main():
    st.title("📺 YouTube Downloader")
    st.markdown("### Descarga tus videos favoritos de YouTube")

    url = st.text_input("Ingresa el enlace de YouTube:", placeholder="https://youtube.com/...")

    if url:
        info = get_video_info(url)
        if info:
            st.markdown("### Información del video")
            st.write(f"**Título:** {info['title']}")
            st.write(f"**Duración:** {info['duration']}")

            download_option = st.radio(
                "Selecciona el formato:",
                ["Video completo", "Solo audio (MP3)"]
            )

            if st.button("⬇️ Descargar"):
                download_video(url, download_option == "Solo audio (MP3)")

    # Información adicional
    with st.expander("ℹ️ Información y ayuda"):
        st.markdown("""
        ### Instrucciones:
        1. Pega el enlace del video de YouTube
        2. Selecciona si quieres descargar el video completo o solo el audio
        3. Haz clic en "Descargar"
        4. Cuando el archivo esté listo, aparecerá un botón "Guardar archivo"
        5. Haz clic en "Guardar archivo" para descargarlo a tu dispositivo

        ### Notas:
        - El tiempo de procesamiento dependerá de tu conexión a internet
        - Para videos largos, la preparación puede tardar varios minutos

        ### Formatos disponibles:
        - **Video completo**: Incluye video y audio en la mejor calidad disponible
        - **Solo audio**: Formato MP3
        """)

if __name__ == "__main__":
    install_dependencies()
    main()