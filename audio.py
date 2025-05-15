import pydub, os, glob, div, requests, io
from collections import defaultdict


temp_sent = defaultdict(list)
n = defaultdict(list)
n["mita"] = 0
n["player"] = 0


def get_audio_from_api(charaster, text):
    print(charaster)
    pith = 8 if charaster == "mita" else -8
    sentence = div.division(text=text)
    for message in sentence:
        print(message)

        params = {
            "text": message,
            "person": "Player" if charaster == "player" else "CrazyMita",
            "rate": "+8%",
            "pith": pith
        }
        headers = {'Content-type': 'application/json'}

        try:
            response = requests.post(
                    url="http://109.110.73.254:2020/api/v1/edge/get_edge",
                    json=params,
                    headers=headers 
            )
            response.raise_for_status()
            temp_sent[f"{charaster}_{n[charaster]}"].append(pydub.AudioSegment.from_file(io.BytesIO(response.content), format="mp3"))
            div.sub(text=message, charaster=charaster, audio_duration=len(pydub.AudioSegment.from_file(io.BytesIO(response.content))))
        except Exception as e:
            print(e)
            raise
        
def temp_sent_to_one_audio(charaster):
    print(charaster)
    temp_sent[f"{charaster}_{n[charaster]}"] = sum(temp_sent[f"{charaster}_{n[charaster]}"])
    temp_sent[f"{charaster}_{n[charaster]}"].export(os.path.abspath(f"audio/{n[charaster]}_{charaster}.mp3"))
    temp_sent[f"{charaster}_{n[charaster]}"] = []
    n[charaster] += 1


def get_duration(audio):
    return len(pydub.AudioSegment.from_mp3(audio)) // 1000


def all_duration_audio():
    duration = 0
    audio_files = glob.glob(os.path.abspath("audio/*"))
    print(len(glob.glob(os.path.abspath("audio/*"))))
    for i in range(len(glob.glob(os.path.abspath("audio/*")))):
        duration += get_duration(audio_files[i])
    print(duration)


def gluing_audio():
    mita_files = glob.glob(os.path.abspath("audio/*_mita.mp3"))
    mita_num_files = len(glob.glob(os.path.abspath("audio/*_mita.mp3")))

    player_files = glob.glob(os.path.abspath("audio/*_player.mp3"))
    player_num_files = len(glob.glob(os.path.abspath("audio/*_player.mp3")))
    all_audio_files = []
    print(max(mita_num_files, player_num_files))
    for i in range(max(mita_num_files, player_num_files)):
        all_audio_files.append(pydub.AudioSegment.from_mp3(mita_files[i]))
        all_audio_files.append(pydub.AudioSegment.silent(500))
        all_audio_files.append(pydub.AudioSegment.from_mp3(player_files[i]))
    all_audio_files = sum(all_audio_files)
    all_audio_files.export(os.path.abspath("temp/temp_audio.mp3"))
    
    
    
    #all_audio_files.export(f"{os.path.abspath("temp")}/out.mp3", format="mp3")
    


if __name__ == "__main__":
    pass
