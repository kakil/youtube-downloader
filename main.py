import os
import streamlit as st
from pytube import YouTube
from pytube.exceptions import PytubeError
import tempfile
import shutil


st.title("YouTube Video Downloader")

# Test URL:  https://www.youtube.com/watch?v=PYe2uv-evOo

youtube_url = st.text_input("Enter the YouTube video URL: ")

if youtube_url:
    # Save YouTube URL in session state
    st.session_state['youtube_url'] = youtube_url

if st.button("Download Video"):
    if 'youtube_url' in st.session_state:
        try:
            # Attempting to get the best available stream that is
            # a progressive video (contains both audio and video)
            yt = YouTube(st.session_state['youtube_url'])
            video_title = yt.title
            stream = yt.streams.filter(progressive=True).first()

            with tempfile.TemporaryDirectory() as temp_dir:
                download_path = stream.download(output_path=temp_dir)
                st.success(f"Download '{video_title}' successfully!")
                st.video(download_path)
                print(download_path)

                # Copy to a persistent temporary file
                persistent_temp_file = tempfile.NamedTemporaryFile(delete=False)
                shutil.copy(download_path, persistent_temp_file.name)

            st.session_state['download_path'] = persistent_temp_file.name

        except PytubeError as e:
            print(f"Failed to download due to a Pytube error: {e}")
        except Exception as e:
            print(f"An error occurredL {e}")

    if 'download_path' in st.session_state:
        with open(st.session_state['download_path'], "rb") as file:
            file_data = file.read()
            btn = st.download_button(
                label="Download Video to Disk",
                data=file_data,
                file_name=os.path.basename(st.session_state['download_path']),
                mime="video/mp4"
            )

    if 'youtube_url' not in st.session_state:
        st.error("Please enter a valid YouTube URL")
