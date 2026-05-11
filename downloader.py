import yt_dlp
from colorama import init, Fore, Style

init()

def mp4_ytb():
    url = input(Fore.RED + "| YouTube URL (converter mp4): ")

    options = {
        "format": "best[ext=mp4][vcodec=h264]/best",
        "merge_output_format": "mp4",
        "ffmpeg_location": "/data/data/com.termux/files/usr/bin",
        "outtmpl": "/storage/emulated/0/Download/%(title)s.%(ext)s"
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([url])

    print(Fore.GREEN + "| Download finished" + Style.RESET_ALL)


def mp3_ytb():
    url = input(Fore.RED + "| Youtube URL(converter mp3): ")

    options = {
        "format": "bestaudio/best",
        "outtmpl": "/storage/emulated/0/Download/%(title)s.%(ext)s",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
        "ffmpeg_location": "/data/data/com.termux/files/usr/bin",
        "quiet": False
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([url])

    print(Fore.GREEN + "| MP3 conversion finished" + Style.RESET_ALL)


if __name__ == "__main__":
    mp3_ytb()