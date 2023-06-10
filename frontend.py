import streamlit as st
from threading import Thread
from queue import Queue
import pyaudio
import subprocess
import json
from vosk import Model,KaldiRecognizer


# Initialising pyaudio
# p = pyaudio.PyAudio()
# for i in range(p.get_device_count()):
#     print(p.get_device_info_by_index(i))

CHANNELS = 1 
FRAME_RATE = 16000
RECORD_SECONDS = 20
AUDIO_FORMAT = pyaudio.paInt16
SAMPLE_SIZE = 2
recording_flag = False

# Threading 
messages = Queue()
recordings  = Queue()


# Vosk model for transcription
model = Model(model_name='vosk-model-small-en-us-0.15')
rec = KaldiRecognizer(model,FRAME_RATE)
rec.SetWords(True)

# Layout 
st.set_page_config(
    page_title="Transcibot", page_icon=":studio_microphone:", layout="wide"
)
st.title("Transcibot")
st.header("Transcribe Below")
# st.subheader("")
first,last = st.columns(2)



# def start_recording():
#     global recording_flag
#     messages.put(True)
#     st.write("Starting...")
#     recording_flag = True
#     record = Thread(target=record_mic)
#     record.start()
#     transcribe = Thread(target=speech_recognition)
#     transcribe.start()


# def stop_recording():
#     global recording_flag
#     messages.get()
#     st.write("Stopped..")
#     recording_flag = False



# def record_mic(chunk=1024):
#     p = pyaudio.PyAudio()
#     stream = p.open(format=AUDIO_FORMAT,channels = CHANNELS , rate = FRAME_RATE , input = True,input_device_index=1 , frames_per_buffer = chunk)
#     frames = []
#     while recording_flag or not messages.empty():
#         data = stream.read(chunk)
#         frames.append(data)
#         print(frames)
#         if len(frames) >= (FRAME_RATE * RECORD_SECONDS) / chunk :
#             recordings.put(frames.copy())
#             frames=[]
#     stream.stop_stream()
#     stream.close()
#     p.terminate()        


# def speech_recognition():
#     while not messages.empty():
#         frames = recordings.get()
#         rec.AcceptWaveform(b''.join(frames))
#         result = rec.Result()
#         text = json.loads(result)['text']
#         # print(text)
#         cased = subprocess.check_output('python recasepunc/recasepunc.py predict recasepunc/checkpoint',shell=True,text=True,input=text)
#         st.write("#The output ")
#         st.write(cased)

# if first.button("Speak :studio_microphone:"):
#     start_recording()
    
# if last.button("Stop :mute:"):
#    stop_recording()



import streamlit as st
from threading import Thread
from queue import Queue
import pyaudio
import subprocess
import json
from vosk import Model, KaldiRecognizer

# ...

def start_recording():
    messages.put(True)
    st.write("Starting...")
    record = Thread(target=record_mic, args=(messages,))
    record.start()
    transcribe = Thread(target=speech_recognition, args=(recordings,))
    transcribe.start()

def stop_recording():
    messages.get()
    st.write("Stopped..")

def record_mic(messages_queue, chunk=1024):
    p = pyaudio.PyAudio()
    stream = p.open(
        format=AUDIO_FORMAT,
        channels=CHANNELS,
        rate=FRAME_RATE,
        input=True,
        input_device_index=1,
        frames_per_buffer=chunk
    )
    frames = []
    while not messages_queue.empty():
        data = stream.read(chunk)
        frames.append(data)
        if len(frames) >= (FRAME_RATE * RECORD_SECONDS) / chunk:
            recordings.put(frames.copy())
            frames = []
    stream.stop_stream()
    stream.close()
    p.terminate()

def speech_recognition(recordings_queue):
    while not messages.empty():
        frames = recordings_queue.get()
        rec.AcceptWaveform(b''.join(frames))
        result = rec.Result()
        text = json.loads(result)['text']
        cased = subprocess.check_output('python recasepunc/vosk-recasepunc-en-0.22/recasepunc.py predict recasepunc/vosk-recasepunc-en-0.22/checkpoint', shell=True, text=True, input=text)
        st.write("# The output ")
        st.write(cased)

# ...

if first.button("Speak :studio_microphone:"):
    start_recording()
    
if last.button("Stop :mute:"):
   stop_recording()

# ...
