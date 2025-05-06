import pydub, os, main
from pydub.playback import play

audio_frame = []


def num_frame_conf():
    n = 0
    while True:
        try:
            f = open(f"{os.getcwd()}\\{n}_mita.mp3")
            n += 1
            f.close()
        except:
            break
    return n



def add_audio_frame():
    global audio_frame
    print("создание frame")
    audio_frame.append(pydub.AudioSegment.silent(5000))
    for i in range(num_frame_conf()):
        x = pydub.AudioSegment.from_mp3(f"{os.getcwd()}\\{i}_mita.mp3") + (pydub.AudioSegment.silent())
        audio_frame.append(x)
        x = pydub.AudioSegment.from_mp3(f"{os.getcwd()}\\{i}_player.mp3") + pydub.AudioSegment.silent()
        audio_frame.append(x)
    for i in range(len(audio_frame)):
        main.main_dict['audio'].append(audio_frame[i])

def audio_main():
    print("Старт аудио")
    add_audio_frame()
    for i in range(len(main.main_dict['audio'])):
        print(len((main.main_dict['audio'])))
        play(main.main_dict['audio'][i])

if __name__ == "__main__":
    audio_main()
