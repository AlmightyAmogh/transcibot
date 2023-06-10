# import pyaudio


# p = pyaudio.PyAudio()
# for i in range(p.get_device_count()):
#     print(p.get_device_info_by_index(i))


# # //index = 1 --> mic   index 3 -- headphone   index 4 -- speakers


import pyaudio

def get_active_microphone():
    p = pyaudio.PyAudio()
    device_info = p.get_default_input_device_info()
    return device_info['name']

def list_audio_devices():
    p = pyaudio.PyAudio()
    device_count = p.get_device_count()
    print("Available audio devices:")
    for i in range(device_count):
        device_info = p.get_device_info_by_index(i)
        device_name = device_info['name']
        print(f"Device {i+1}: {device_name}")

# List available audio devices
list_audio_devices()

# Get active microphone
active_microphone = get_active_microphone()
print("Active microphone:", active_microphone)