import random, subprocess, ffmpeg, glob, os

def gluing():
    try:
        subprocess.run([
            'ffmpeg',
            '-f', 'concat',
            '-safe', '0',
            '-i', f"{os.path.abspath("temp/input.txt")}",
            '-c', 'copy',
            f"{os.path.abspath("temp/temp_output.mp4")}"
        ], check=True, stderr=subprocess.PIPE, text=True)
    except subprocess.CalledProcessError as e:
        print("FFmpeg error:", e.stderr)
        raise

def gluing_audio_and_video():
        subprocess.run([
        "ffmpeg",
        "-i", f"{os.path.abspath("temp/temp_output.mp4")}",
        "-i", f"{os.path.abspath("temp/temp_audio.mp3")}",
        "-c:v", "copy",
        "-map","0:v:0", 
        "-map", "1:a:0",
        "-c", "copy", f"{os.path.abspath("temp/main_stream.mp4")}"
    ])



def duration_video(filename):
    probe = ffmpeg.probe(filename)
    return float(probe['format']['duration']) + 0.5


def acceleration(video, num, speed):
    subprocess.run([
        "ffmpeg",
        "-i", video,
        "-filter:v", f"setpts={speed}*PTS",
        "-an",
        f"{os.path.abspath(f'temp/{num}.mp4')}"
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def add_audio():
    pass

if __name__ == "__main__":
    pass