import audio, video, glob, os, shutil, random, threading, time, aiChat, div, screensaver, telegram_bot

stream_ready = False
create_ready = True

def all_duration_audio():
    duration = 0
    audio_files = glob.glob(os.path.abspath("audio/*"))
    print(len(glob.glob(os.path.abspath("audio/*"))))
    for i in range(len(glob.glob(os.path.abspath("audio/*")))):
        duration += audio.get_duration(audio_files[i])
    print(duration)

def create_video_mita():
    mita_audio = glob.glob(os.path.abspath('audio/*_mita.mp3'))
    mita_video = glob.glob(os.path.abspath('video/mita*.mp4'))
    for i in range(len(mita_audio)):
        duration_audio = audio.get_duration(mita_audio[i])
        mita_video1 = random.choice(mita_video)
        duration_video = video.duration_video(mita_video1)
        if duration_video == duration_audio:
            shutil.copy2(mita_video1, os.path.abspath(f"temp/{i}_mita"))
        else:
            video.acceleration(mita_video1, f"{i}_mita", duration_audio / duration_video)

def create_video_player():
    player_audio = glob.glob(os.path.abspath('audio/*_player.mp3'))
    player_video = glob.glob(os.path.abspath('video/player*'))
    print(player_video)
    for i in range(len(player_audio)):
        duration_audio = audio.get_duration(player_audio[i])
        player_video1 =  random.choice(player_video)
        duration_video = video.duration_video(player_video1)
        if duration_video == duration_audio:
            shutil.copy2(player_video1, os.path.abspath(f"temp/{i}_player"))
        else:
    #         player_video2 = random.choice(player_video)
    #         input_txt_path = os.path.abspath("temp/input.txt")
    #         with open(input_txt_path, "w", encoding='utf-8') as f:
    #             f.write(f"file '{os.path.abspath(player_video1)}'\n")
    #             f.write(f"file '{os.path.abspath(player_video2)}'\n")
    #             print(f"{os.path.abspath("temp")}\\input.txt")
    #             print(os.path.exists(os.path.abspath("temp/input.txt")))
    #             if not os.path.exists(os.path.abspath("temp/input.txt")):
    #                 time.sleep(0.5)
    #             time.sleep(2)
    #             video.gluing()
    #             print("склейка")
    # #            os.remove(f"{os.path.abspath("temp")}/input.txt")
    #             player_video1 = "D:\\MitaStream\\temp\\temp_output.mp4"
                video.acceleration(player_video1, f"{i}_player", duration_audio / duration_video)
                # os.remove(player_video1)

def create_temp_video():
    temp_vid_mita = glob.glob(os.path.abspath("temp/*_mita.mp4"))
    temp_vid_player = glob.glob(os.path.abspath("temp/*_player.mp4"))
    with open(os.path.abspath("temp/input.txt"), "w") as f:
        for i in range(max(len(temp_vid_mita), len(temp_vid_player))):
            f.writelines(f"file \'{temp_vid_mita[i]}\'\n")
            f.writelines(f"file \'{temp_vid_player[i]}\'\n")
        f.writelines(f"file \'{os.path.abspath("video/end.mp4")}\'")

def delete_temp():
    for file in glob.glob(os.path.abspath("temp/*")):
        os.remove(file)
def delete_audio():
    for file in glob.glob(os.path.abspath("audio/*")):
        os.remove(file)

def saver():
    global stream_ready
    print(glob.glob(os.path.abspath("screensaver")))
    threading.Thread(target=create_stream).start()
    screensaver.scrnsvr_main()

def create_stream():
    global create_ready
    print(f"start create_stream, stream_ready = {create_ready}")
    while True:
        if create_ready:
            start_time = time.time()
            threads = []


            delete_temp()
            delete_audio()
            aiChat.get_duration_dialogue()
            aiChat.Chat()


            all_duration_audio()
            audio.gluing_audio()
            threads.append(threading.Thread(target=create_video_mita))
            threads.append(threading.Thread(target=create_video_player))
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()
            create_temp_video()
            video.gluing()
            video.gluing_audio_and_video()
            div.add_sub()
            create_ready = False
            end_time = time.time()
            print(f"Время выполнения: {(end_time - start_time):.2f}")

if __name__ == "__main__":
    threading.Thread(target=telegram_bot.start_bot).start()
    saver()