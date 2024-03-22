from gtts import gTTS
from playsound import playsound
import speech_recognition as sr

r = sr.Recognizer()
with sr.Microphone() as source:
    audio = r.listen(source)

text = r.recognize_google(audio, language="ko")


try:
    text = r.recognize_google(audio, language="ko")
    print(text)

    speech = "text.mp3"  # 오디오를 저장할 파일 이름
    tts = gTTS(text, lang="ko")  # 텍스트를 오디오로 변환
    tts.save(speech)  # 파일로 저장
    playsound(speech)  # 오디오 파일 재생

except sr.UnknownValueError:  # 음성 인식이 실패한 경우
    print("인식 실패")

except sr.RequestError as e:  # 요청이 실패한 경우
    print(f"요청 실패 : {e}")
