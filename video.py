import cv2, random, screeninfo, main, audio, threading, os, glob
from pathlib import Path
import numpy as np

video_frame_mita = []
video_frame_player = []

height = 0
width = 0


def num_frame_conf():
    files = glob.glob(f"{Path.cwd()}\\frames_?_mita.npz")
    print(len(files))
    return len(files) - 1 

def num_frame_conf_player():
    files = glob.glob(f"{Path.cwd()}\\frames_?_player.npz")
    print(len(files))
    return len(files) - 1


def get_video_frame_mita(num):
    temp_ar = np.load(f"{Path.cwd()}\\frames_{num}_mita.npz", allow_pickle=True)
    return temp_ar['arr_0']

def get_video_frame_player(num):
    temp_ar = np.load(f"D:\\npy_dir\\frames_{num}_player.npz", allow_pickle=True)
    return temp_ar['arr_0']

def get_video_frame_start():
    try: 
        temp_ar = np.load(f"{Path.cwd()}\\frames_start.npz", allow_pickle=True)
        return temp_ar['arr_0']
    except Exception as e:
        print(e)


def get_monitor_size():
    for monitor in screeninfo.get_monitors():
        global height 
        global width 
        height = monitor.height
        width = monitor.width
        print(f"{height} {width}")


def add_random_frame(temp_ar):
    temp_ar.append(get_video_frame_mita(random.randint(0, num_frame_conf())))
    temp_ar.append(get_video_frame_player(random.randint(0, num_frame_conf())))
    return

def random_frame():
    print("random_frame")
    global video_frame_player
    global video_frame_mita
    temp_ar = []
    print("get_video_frame_start")
    temp_ar.append(get_video_frame_start())
    threads = []
    for i in range(len(main.main_dict["audio"]) // 2):
        t = threading.Thread(target=add_random_frame, args=(temp_ar,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
    # else:
    #     for i in range(len(video_frame_mita)):
    #         temp_ar.append(video_frame_mita[random.randint(0, len(video_frame_mita))])
    #         temp_ar.append(video_frame_player[random.randint(0, len(video_frame_player))])
    for i in range(len(temp_ar)):
        main.main_dict["video"].append(temp_ar[i])


def get_video_duration_from_frames(frames_list, fps):
    return len(frames_list) // fps

def resize_video_frame():
    print("___________________")
    for i in range(len(main.main_dict["audio"])):
        len_audio = len(main.main_dict["audio"][i]) // 1000
        print(len(main.main_dict["video"]))
        print(len(main.main_dict["audio"]))
        len_video = get_video_duration_from_frames(main.main_dict["video"][i], 30)
        if int(len_video) < int(len_audio):
            if i // 2:
                "Mita"
                temp = get_video_frame_mita(random.randint(0, num_frame_conf()))
                len_temp = get_video_duration_from_frames(temp, 30)
                if len_video + len_temp == len_audio:
                    main.main_dict["video"][i] += temp
                elif len_video + len_temp < len_audio and len_temp / (len_audio - (len_video + len_temp)) > 0 :
                    remaining = len_audio - len_video
                    speed = len_temp / remaining if remaining > 0 else 1.0
                    print(len_temp)
                    print(f"{len_audio} - {(len_video + len_temp)}")
                    print(len_audio - (len_video + len_temp))
                    print(speed)
                    if speed < 0.1:
                        step = int(1 / 0.1)
                        new_frames = temp[::step]
                    num_new_frames = int(len(temp) / speed)
                    indices = np.linspace(0, len(temp) - 1, num_new_frames).astype(int)
                    new_frames = temp[indices]
                    main.main_dict["video"][i] = np.concatenate((main.main_dict["video"][i], new_frames), axis=0)
                elif len_video + len_temp > len_audio:
                    remaining = len_audio - len_video
                    speed = len_temp / remaining if remaining > 0 else 1.0
                    num_new_frames = int(len(temp) / speed)
                    print(len_temp)
                    print(f"{len_audio} - {(len_video + len_temp)}")
                    print(len_audio - (len_video + len_temp))
                    print(speed)
                    if speed < 0.1:
                        step = int(1 / 0.1)
                        new_frames = temp[::step]
                    indices = np.linspace(0, len(temp) - 1, num_new_frames).astype(int)
                    new_frames = temp[indices]
                    main.main_dict["video"][i] = np.concatenate((main.main_dict["video"][i], new_frames), axis=0)
            else:
                "player"
                temp = get_video_frame_player(random.randint(0, num_frame_conf_player()))
                len_temp = get_video_duration_from_frames(temp, 30)
                if len_video + len_temp == len_audio:
                    main.main_dict["video"][i] += temp
                elif len_video + len_temp < len_audio:
                    remaining = len_audio - len_video
                    speed = len_temp / remaining if remaining > 0 else 1.0
                    print(len_temp)
                    print(f"{len_audio} - {(len_video + len_temp)}")
                    print(len_audio - (len_video + len_temp))
                    print(speed)
                    if speed < 0.1:
                        step = int(1 / 0.1)
                        new_frames = temp[::step]
                    num_new_frames = int(len(temp) / speed)
                    indices = np.linspace(0, len(temp) - 1, num_new_frames).astype(int)
                    new_frames = temp[indices]
                    main.main_dict["video"][i] = np.concatenate((main.main_dict["video"][i], new_frames), axis=0)
                elif len_video + len_temp > len_audio:
                    remaining = len_audio - len_video
                    speed = len_temp / remaining if remaining > 0 else 1.0
                    num_new_frames = int(len(temp) / speed)
                    print(len_temp)
                    print(f"{len_audio} - {(len_video + len_temp)}")
                    print(len_audio - (len_video + len_temp))
                    print(speed)
                    if speed < 0.1:
                        step = int(1 / 0.1)
                        new_frames = temp[::step]
                    indices = np.linspace(0, len(temp) - 1, num_new_frames).astype(int)
                    new_frames = temp[indices]
                    main.main_dict["video"][i] = np.concatenate((main.main_dict["video"][i], new_frames), axis=0)
            print(len_temp)
            print(len(main.main_dict["video"][i]))

    


def play_video_frame():
    global height 
    global width 
    print(len(main.main_dict["video"]))
    for i in range(len(main.main_dict["video"])):
        for x in range(len(main.main_dict["video"][i])):
            cv2.namedWindow("MitaStream", cv2.WINDOW_NORMAL)
            cv2.setWindowProperty("MitaStream", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            cv2.waitKey(30)
            frame = cv2.resize(main.main_dict["video"][i][x], (width, height), interpolation=cv2.INTER_AREA)
            cv2.imshow("MitaStream", frame)


def video_main():
    # add_video_frame_mita()
    # add_video_frame_player()
    get_monitor_size()
    audio.add_audio_frame()
    random_frame()
    resize_video_frame()
    #play_video_frame()

if __name__ == "__main__":
    video_main()























# def get_video_frame(num):
#     temp_array = []
#     if num == 0:
#         cap = cv2.VideoCapture(f"{Path.cwd()}\\{num}.mp4")
#     elif num == 1:
#         cap = cv2.VideoCapture(f"{Path.cwd()}\\{num}.mp4")
#     elif num == 2:
#         cap = cv2.VideoCapture(f"{Path.cwd()}\\{num}.mp4")
#     else:
#         cap = cv2.VideoCapture(f"{Path.cwd()}\\{random.randint(3, 5)}.mp4")
#     print(num)
#     while True:
#         ret, frame = cap.read()

#         if not ret:
#             break
#         key = cv2.waitKey(30)
#         temp_array.append(frame)
#     cap.release()
#     print(len(temp_array))
#     return temp_array
        
# def add_video_frame_mita():
#     with ThreadPoolExecutor(max_workers=4) as ex:
#         futures = [ex.submit(get_video_frame_mita, i) for i in range(num_frame_conf())]
#         for futur in as_completed(futures):
#             video_frame_mita.append(futur.result())

# def add_video_frame_player():
#     with ThreadPoolExecutor(max_workers=4) as ex:
#         futures = [ex.submit(get_video_frame_player, i) for i in range(num_frame_conf_player())]
#         for futur in as_completed(futures):
#             video_frame_player.append(futur.result())
