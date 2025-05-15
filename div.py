import re, pysubs2, subprocess, os, audio, main
from pysubs2 import SSAFile, SSAStyle

subtitle = []
latest_duration = 0
subs = SSAFile()
subs_mita = SSAFile()
subs_player = SSAFile()


def division(text):
    eng_to_rus(text)
    text = re.sub(r'\*.*?\*', '', text).strip()
    sentences = re.split(r'(?<=[.!?])\s+', text)
    i = 0
    if len(sentences[len(sentences) - 1]) < 10:
        sentences[len(sentences) - 2] = sentences[len(sentences) - 2] + " " + sentences[len(sentences) - 1]
        del sentences[len(sentences) - 1]
    while i < len(sentences) - 1:
        if len(sentences[i]) < 10:
            sentences[i] = sentences[i] + " " + sentences[i+1]
            del sentences[i+1]
        else: i+=1
    
    return sentences


def eng_to_rus(text):
    # Словарь для замены двойных букв (проверяется в первую очередь)
    double_letters = {
        'th': 'т',
        'sh': 'ш',
        'ch': 'ч',
        'zh': 'ж',
        'kh': 'х',
        'yu': 'ю',
        'ya': 'я',
        'yo': 'ё',
        'ye': 'е',
        'ts': 'ц',
        'ia': 'я',
        'iu': 'ю',
        'ie': 'е',
        'io': 'ё',
        'io': 'ё',
        'py': 'пай',
    }

    # Словарь для одиночных букв
    single_letters = {
        'a': 'а', 'b': 'б', 'c': 'к', 'd': 'д', 'e': 'е',
        'f': 'ф', 'g': 'г', 'h': 'х', 'i': 'и', 'j': 'дж',
        'k': 'к', 'l': 'л', 'm': 'м', 'n': 'н', 'o': 'о',
        'p': 'п', 'q': 'к', 'r': 'р', 's': 'с', 't': 'т',
        'u': 'а', 'v': 'в', 'w': 'в', 'x': 'кс', 'y': 'й',
        'z': 'з',
    }

    result = []
    i = 0
    n = len(text)
    
    while i < n:
        # Проверяем двойные буквы (если не вышли за границы строки)
        if i + 1 < n:
            two_chars = text[i:i+2].lower()
            if two_chars in double_letters:
                # Добавляем в результат (с учётом регистра)
                if text[i].isupper():
                    result.append(double_letters[two_chars].capitalize())
                else:
                    result.append(double_letters[two_chars])
                i += 2
                continue
        
        # Если не нашли двойную букву, проверяем одиночную
        char = text[i].lower()
        if char in single_letters:
            if text[i].isupper():
                result.append(single_letters[char].capitalize())
            else:
                result.append(single_letters[char])
        else:
            result.append(text[i])  # Оставляем символ как есть, если нет замены
        i += 1
    
    return ''.join(result)


def sub(text, charaster, audio_duration):
    global latest_duration, subs
    player = SSAStyle(
    fontname="Rounded M Plus",
    fontsize=10,
    primarycolor=pysubs2.Color(178, 2, 247),
    backcolor="#f2c80a"
    )
    mita = SSAStyle(
        fontname="Rounded M Plus",
        outline=1,
        fontsize=10,
        primarycolor=pysubs2.Color(247, 194, 2),
        backcolor="#b202f7"
    )

    subs.styles["player"] = player
    subs.styles["mita"] = mita


    if charaster == "player":
        subs.append(pysubs2.SSAEvent(start=latest_duration, end=latest_duration + audio_duration, text=text, style=charaster))
    if charaster == "mita":
        subs.append(pysubs2.SSAEvent(start=latest_duration, end=latest_duration + audio_duration, text=text, style=charaster))
    latest_duration += audio_duration


def add_sub():
    global subs
    subs.save(os.path.abspath("temp/sub.ass"))
    subprocess.run(["ffmpeg", "-i", "main_stream.mp4", "-vf", f"ass=sub.ass", "main_stream_subtitle.mp4"], cwd=f"{os.path.abspath("temp")}")
    main.stream_ready = True

if __name__ == "__main__":

    pass