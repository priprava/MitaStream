main_dict = {
    "video": [],
    "audio": [],
}

def main():
    import audio, video, threading


    video.video_main()
    threading.Thread(target=audio.audio_main).start()
    video.play_video_frame()

if __name__ == "__main__":
    main()
