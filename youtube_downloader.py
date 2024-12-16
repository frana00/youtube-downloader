import streamlit as st
import yt_dlp
import re

# Page configuration
st.set_page_config(
    page_title="Social Media Downloader",
    page_icon="📺",
    layout="centered"
)

# Title and description with HTML
st.markdown("""
    <h1 style='text-align: center;'>📺 Social Media Downloader</h1>
    <h3 style='text-align: center;'>YouTube & TikTok Downloader</h3>
""", unsafe_allow_html=True)

st.markdown("""
    🇺🇸 Download videos from YouTube and TikTok  
    🇪🇸 Descarga videos de YouTube y TikTok
""")

# URL input
url = st.text_input(
    "🔗 URL:",
    placeholder="https://youtube.com/... or https://tiktok.com/..."
)

# Download options
if url:
    if "youtube.com" in url or "youtu.be" in url:
        download_type = st.radio(
            "🎯 Download Type | Tipo de Descarga",
            ["Video MP4 🎥", "Audio MP3 🎵"]
        )
    elif "tiktok.com" in url:
        download_type = "Video MP4 🎥"
    else:
        st.error("❌ URL not supported | URL no soportada")
        st.stop()

    # Download button
    if st.button("⬇️ Download | Descargar"):
        try:
            with st.spinner("⏳ Processing... | Procesando..."):
                # YouTube download options
                if "youtube.com" in url or "youtu.be" in url:
                    if "Video MP4" in download_type:
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
                # TikTok download options
                else:
                    ydl_opts = {
                        'format': 'best',
                    }

                # Download process
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                    video_title = info['title']
                    video_url = info['url']

                    # Clean filename
                    clean_title = re.sub(r'[\\/*?:"<>|]', "", video_title)

                    # Set file extension
                    extension = 'mp3' if "Audio MP3" in download_type else 'mp4'
                    filename = f"{clean_title}.{extension}"

                    # Download button
                    st.download_button(
                        label="📥 Click to download | Clic para descargar",
                        data=ydl.urlopen(video_url).read(),
                        file_name=filename,
                        mime=f"{'audio' if extension == 'mp3' else 'video'}/{extension}"
                    )

                    st.success("✅ Ready to download! | ¡Listo para descargar!")

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

# Add footer
st.markdown("""
---
<div style='text-align: center;'>
    Made with ❤️ by Frana | <a href="https://github.com/frana00/youtube-downloader"><img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" height="20"/></a>
</div>
""", unsafe_allow_html=True)