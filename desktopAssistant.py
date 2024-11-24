import base64
from threading import Lock, Thread
import numpy as np
import pyautogui
import cv2
import openai
from cv2 import imencode
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema.messages import SystemMessage
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI
from pyaudio import PyAudio, paInt16
from speech_recognition import Microphone, Recognizer, UnknownValueError

load_dotenv()

class DesktopCapture:
    def __init__(self):
        self.running = False
        self.lock = Lock()
        self.frame = None

    def start(self):
        if self.running:
            return self
        self.running = True
        self.thread = Thread(target=self.capture_desktop)
        self.thread.start()
        return self

    def capture_desktop(self):
        while self.running:
            screenshot = pyautogui.screenshot()
            frame = np.array(screenshot)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            with self.lock:
                self.frame = frame

    def read(self, encode=False):
        with self.lock:
            frame = self.frame.copy() if self.frame is not None else None
        if frame is None:
            return None
        if encode:
            _, buffer = imencode(".jpeg", frame)
            return base64.b64encode(buffer)
        return frame

    def stop(self):
        self.running = False
        if self.thread.is_alive():
            self.thread.join()

class Assistant:
    def __init__(self, model):
        self.chain = self._create_inference_chain(model)

    def answer(self, prompt, image):
        if not prompt or image is None:
            return
        print("Prompt:", prompt)
        response = self.chain.invoke(
            {"prompt": prompt, "image_base64": image.decode()},
            config={"configurable": {"session_id": "unused"}},
        ).strip()
        print("Response:", response)
        if response:
            self._tts(response)

    def _tts(self, response):
        player = PyAudio().open(format=paInt16, channels=1, rate=24000, output=True)
        with openai.audio.speech.with_streaming_response.create(
            model="tts-1",
            voice="alloy",
            response_format="pcm",
            input=response,
        ) as stream:
            for chunk in stream.iter_bytes(chunk_size=1024):
                player.write(chunk)

    def _create_inference_chain(self, model):
        SYSTEM_PROMPT = """
        You are an assistant that observes the user's desktop activity and listens to their voice to answer questions.
        Your responses should be concise, friendly, and helpful. Avoid unnecessary verbosity or emojis.
        """
        prompt_template = ChatPromptTemplate.from_messages(
            [
                SystemMessage(content=SYSTEM_PROMPT),
                MessagesPlaceholder(variable_name="chat_history"),
                (
                    "human",
                    [
                        {"type": "text", "text": "{prompt}"},
                        {
                            "type": "image_url",
                            "image_url": "data:image/jpeg;base64,{image_base64}",
                        },
                    ],
                ),
            ]
        )
        chain = prompt_template | model | StrOutputParser()
        chat_message_history = ChatMessageHistory()
        return RunnableWithMessageHistory(
            chain,
            lambda _: chat_message_history,
            input_messages_key="prompt",
            history_messages_key="chat_history",
        )

desktop_capture = DesktopCapture().start()

# Replace ChatOpenAI with GPT-4o Model
model = ChatOpenAI(model="gpt-4o")
assistant = Assistant(model)

def audio_callback(recognizer, audio):
    try:
        prompt = recognizer.recognize_whisper(audio, model="base", language="english")
        desktop_frame = desktop_capture.read(encode=True)
        assistant.answer(prompt, desktop_frame)
    except UnknownValueError:
        print("Could not understand the audio.")

recognizer = Recognizer()
microphone = Microphone()

with microphone as source:
    recognizer.adjust_for_ambient_noise(source)

stop_listening = recognizer.listen_in_background(microphone, audio_callback)

try:
    while True:
        desktop_frame = desktop_capture.read()
        if desktop_frame is not None:
            cv2.imshow("Desktop Capture", desktop_frame)
        if cv2.waitKey(1) in [27, ord("q")]:  # Press ESC or Q to quit
            break
finally:
    desktop_capture.stop()
    cv2.destroyAllWindows()
    stop_listening(wait_for_stop=False)
