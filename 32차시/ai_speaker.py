from gtts import gTTS  # gtts library -> gTTS class import.
from playsound import playsound  # playsound module -> playsound function import
import speech_recognition as sr  # SpeechRecognition library import(as sr)
import requests  # requests pacakge import => 인터넷 통신을 위해..
from datetime import (
    datetime,
)  # datetime module -> datetime class import => 시간 정보를 활용하기 위해..

API_KEY = "bb154dc0-0149-11ee-8747-417f4bfcff2ca7b17904-a171-49a5-9707-2d4d229b0adb"
# api_key : machine learning for kids 에서 학습시킨 인공지능 모델을 사용하기 위해 만듦.

r = sr.Recognizer()  # Recognizer 객체 생성
end = False  # 프로그램 종료 확인용 변수
cnt = 1  # 답변할 때 마다 1씩 증가시킬 변수

while not end:
    with sr.Microphone() as source:
        print("녹음 시작")
        audio = r.listen(source)
        print("녹음 끝")
    try:
        #!!! - MLFK 인공지능에 데이터 보내 질문을 인식함.
        text = r.recognize_google(audio, language="ko")  # audio data -> text
        print(text)  # 결과 출력

        url = (
            "https://machinelearningforkids.co.uk/api/scratch/" + API_KEY + "/classify"
        )
        response = requests.get(
            url, params={"data": text}
        )  # 인공지능에 데이터 입력 => requests.get(url, params={ key : value })

        if response.ok:  # 서버에서 잘 처리되어서 정상적인 응답을 보내줬다는 OK 싸인을 의미한다.
            responseData = (
                response.json()
            )  # API에서 JSON 형식의 데이터를 reponse로 주기 위해 => 데이터들 딕셔너리 형태로 담겨있음
            topMatch = responseData[0]  # 인공지능 인식 결과
        else:
            response.raise_for_status()  # 200 OK 코드가 아닌 경우 에러 발동

        label = topMatch["class_name"]  # ["name"]
        confidence = topMatch["confidence"]  # ["name"]

        #!!!

        print(
            f"[인공지능 인식 결과] : {label} {confidence}%"
        )  # 인식 결과 ? 클래스로 인식되었고, ?의 정확도를 가졌다고 출력

        if confidence < 60:  # 정확도 < 60이라면?
            answer = "잘 모름"
        elif label == "hello":  # class name => hello라면?
            answer = "안녕하세요 반갑습니다"
        elif label == "time":  # class name => time이라면?
            answer = f"지금은{datetime.now().strftime('%H시 %M분')}입니다"
        elif label == "meal":  # class name => meal이라면?
            answer = "맛있어요"
        elif label == "exit":  # class name => exit이라면?
            answer = "네 종료할게요"
            end = True
        speech = f"answer{cnt}.mp3"  # audio file name
        tts = gTTS(answer, lang="ko")  # text-> audio
        tts.save(speech)  # 파일로 저장
        playsound(speech)  # 오디오 파일 재생
        cnt += 1  # 답변한 횟수 의미함

    except sr.UnknownValueError:
        print("인식 실패")

    except sr.RequestError as e:
        print(f"요청 실패 : {e}")
