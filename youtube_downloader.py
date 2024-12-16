import streamlit as st
import yt_dlp
import re

# Page configuration / Configuración de la página
st.set_page_config(
    page_title="Social Media Downloader / Descargador de Redes Sociales",
    page_icon="📺",
    layout="centered"
)

# Title and description / Título y descripción
st.title("Social Media Downloader 📺")
st.markdown("""
#### Download videos from YouTube and TikTok / Descarga videos de YouTube y TikTok
""")

# URL input / Entrada de URL
url = st.text_input("Enter the URL / Ingresa la URL:", placeholder="https://www.youtube.com/watch?v=...")

# Download options / Opciones de descarga
if url:
    if "youtube.com" in url or "youtu.be" in url:
        download_type = st.radio(
            "Select download type / Selecciona el tipo de descarga:",
            ["Video MP4", "Audio MP3"]
        )
    elif "tiktok.com" in url:
        download_type = "Video MP4"
    else:
        st.error("URL not supported. Please enter a YouTube or TikTok URL / URL no soportada. Por favor ingresa una URL de YouTube o TikTok")
        st.stop()

    # Download button / Botón de descarga
    if st.button("Download / Descargar"):
        try:
            with st.spinner("Processing... / Procesando..."):
                # YouTube download options / Opciones de descarga de YouTube
                if "youtube.com" in url or "youtu.be" in url:
                    if download_type == "Video MP4":
                        ydl_opts = {
                            'format': 'best[ext=mp4]',
                        }
                    else:  # Audio MP3
                        ydl_opts = {
                            'format': 'bestaudio/best',
                            'postprocessors': [{
                                'key': 'FFmpegExtractAudio',
                                'preferredcodec': 'mp3',
                                'preferredquality': '192',
                            }],
                        }
                # TikTok download options / Opciones de descarga de TikTok
                else:
                    ydl_opts = {
                        'format': 'best',
                    }

                # Download process / Proceso de descarga
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                    video_title = info['title']
                    video_url = info['url']

                    # Clean filename / Limpiar nombre del archivo
                    clean_title = re.sub(r'[\\/*?:"<>|]', "", video_title)

                    # Set file extension / Establecer extensión del archivo
                    extension = 'mp3' if download_type == "Audio MP3" else 'mp4'
                    filename = f"{clean_title}.{extension}"

                    # Download button / Botón de descarga
                    st.download_button(
                        label="Click to download / Clic para descargar",
                        data=ydl.urlopen(video_url).read(),
                        file_name=filename,
                        mime=f"{'audio' if extension == 'mp3' else 'video'}/{extension}"
                    )

                    st.success(f"Ready to download! / ¡Listo para descargar!")

        except Exception as e:
            st.error(f"An error occurred / Ocurrió un error: {str(e)}")

