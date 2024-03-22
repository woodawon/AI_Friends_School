import speech_recognition as sr  # SpeechRecognition 라이브러리 import하고 sr이라는 별칭으로 사용

r = sr.Recognizer()  # Recognizer 객체 생성
with sr.Microphone() as source:  # 마이크를 source로 사용
    print("녹음 시작")
    audio = r.listen(source)  # 마이크를 사용하여 녹음
    print("녹음 끝")


# try - except문 : 코드 실행 시 발생하는 에러 처리함.
# '예외' 란? -> 프로그램 실행 중 에러가 발생하는 상황
# '예외 처리' 란? -> 예외 발생 시 프로그램에서 어떤 처리를 하는 것.
try:
    text = r.recognize_google(audio, language="ko")  # 오디오 데이터를 텍스트로 변환
    print(text)  # 결과 출력

except sr.UnknownValueError:  # 음성 인식이 실패한 경우
    print("인식 실패")

except sr.RequestError as e:  # 요청이 실패한 경우
    print(f"요청 실패 : {e}")
