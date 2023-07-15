from pathlib import Path
import streamlit as st
import yt_dlp
from httpx import HTTPStatusError
from speechmatics.batch_client import BatchClient
from speechmatics.models import ConnectionSettings

YT_DOWNLOAD_DIR = "downloads"

settings = ConnectionSettings(
    url="https://asr.api.speechmatics.com/v2",
    auth_token=st.secrets["SM_API_KEY"]
)


def download_yt_url(url, get_filename=False):
    yt_id = url.split('/')[-1]
    if yt_id.startswith("watch?v="):
        yt_id = yt_id.replace("watch?v=", "")
    filename = f"{YT_DOWNLOAD_DIR}/{yt_id}.m4a"
    Path(filename).parent.mkdir(exist_ok=True, parents=True)

    if get_filename or Path(filename + ".done").exists():
        return filename

    ydl_opts = {
        "format": "m4a/bestaudio",
        "outtmpl": filename,
        "sleep_interval": 1,
        "max_sleep_interval": 5,
        "writesubtitles": False,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    Path(filename + ".done").touch()

    return filename


def get_job_config(lang: str, op: str):
    return {
        "type": "transcription",
        "transcription_config": {
            "language": lang,
            "operating_point": op,
            "diarization": "speaker",
        },
    }

def run_sm_asr(url: str, lang: str = "en", op: str = "standard"):
    return "this is a $2 transcript $3"
    file_path = download_yt_url(url)
    with BatchClient(settings) as client:
        try:
            job_config = get_job_config(lang, op)
            job_id = client.submit_job(
                audio=file_path,
                transcription_config=job_config,
            )
            print(f"file: {file_path}")
            print(f"job_config: {job_config}")
            print(f"job {job_id} submitted")

            transcript = client.wait_for_completion(job_id, transcription_format="txt")
            print(f"job {job_id} done")
            return transcript
        except HTTPStatusError as e:
            print(e)
