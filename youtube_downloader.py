import streamlit as st
import subprocess
import sys
import tempfile
import os
import re

# Configuración de la página
st.set_page_config(
    page_title="Social Media Downloader",
    page_icon="📱",
    layout="centered"
)

# Estilos CSS personalizados
st.markdown("""
    <style>
        .stButton>button {
            width: 100%;
            color: white;
        }
        .stButton>button:hover {
            color: white;
        }
        .download-button {
            background-color: #28a745 !important;
        }
        .platform-info {
            padding: 1rem;
            border-radius: 0.5rem;
            margin: 1rem 0;
        }
        .youtube-info {
            background-color: #ff00001a;
        }
        .tiktok-info {
            background-color: #00f2ea1a;
        }
        .instagram-info {
            background-color: #c135841a;
        }
    </style>
""", unsafe_allow_html=True)

def install_dependencies():
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "yt-dlp"], 
                      check=True, capture_output=True)
    except Exception as e:
        st.error(f"Error instalando dependencias: {str(e)}")

def detect_platform(url):
    if 'youtube.com' in url or 'youtu.be' in url:
        return 'youtube'
    elif 'tiktok.com' in url:
        return 'tiktok'
    elif 'instagram.com' in url:
        return 'instagram'
    return None

def get_platform_icon(platform):
    icons = {
        'youtube': '📺',
        'tiktok': '📱',
        'instagram': '📸'
    }
    return icons.get(platform, '🔗')

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
    st.title("📱 Social Media Downloader")
    st.markdown("### Descarga contenido de tus redes sociales favoritas")

    # Mostrar plataformas soportadas
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("#### 📺 YouTube")
    with col2:
        st.markdown("#### 📱 TikTok")
    with col3:
        st.markdown("#### 📸 Instagram")

    url = st.text_input("Ingresa el enlace:", placeholder="https://...")

    if url:
        platform = detect_platform(url)
        if platform:
            info = get_video_info(url)
            if info:
                st.markdown(f"### {get_platform_icon(platform)} Información del contenido")
                with st.container():
                    st.markdown(f"""
                    <div class="platform-info {platform}-info">
                        <strong>Título:</strong> {info['title']}
                        {'<br><strong>Duración:</strong> ' + info['duration'] if platform == 'youtube' else ''}
                    </div>
                    """, unsafe_allow_html=True)

                # Opciones específicas por plataforma
                if platform == 'youtube':
                    download_option = st.radio(
                        "Selecciona el formato:",
                        ["Video completo", "Solo audio (MP3)"]
                    )
                else:
                    download_option = "Video completo"

                if st.button(f"⬇️ Descargar de {platform.title()}"):
                    download_video(url, download_option == "Solo audio (MP3)")
        else:
            st.error("Por favor, ingresa un enlace válido de YouTube, TikTok o Instagram")

    # Información adicional
    with st.expander("ℹ️ Información y ayuda"):
        st.markdown("""
        ### Plataformas soportadas:

        #### 📺 YouTube
        - Videos completos
        - Solo audio (MP3)
        - Shorts

        #### 📱 TikTok
        - Videos
        - Clips

        #### 📸 Instagram
        - Reels
        - Posts con video
        - Stories (públicas)

        ### Instrucciones:
        1. Pega el enlace del contenido que quieres descargar
        2. La aplicación detectará automáticamente la plataforma
        3. Selecciona las opciones disponibles (si aplica)
        4. Haz clic en "Descargar"
        5. Espera a que se procese y descarga tu archivo

        ### Notas:
        - El tiempo de procesamiento depende de tu conexión a internet
        - Para videos largos, la preparación puede tardar varios minutos
        - Asegúrate de que el contenido sea público
        """)

if __name__ == "__main__":
    install_dependencies()
    main()