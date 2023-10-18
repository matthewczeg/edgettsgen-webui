import streamlit as st
import subprocess
import pygame

def get_voices():
    voices_output = subprocess.check_output("edge-tts --list-voices", shell=True).decode().split('\n')
    voices = [line.split(": ")[1] for line in voices_output if line.startswith("Name: ") and "en-" in line]
    return voices

def pygame_mixer_operation(operation):
    if operation == "stop":
        if pygame.mixer.get_init():
            pygame.mixer.music.stop()
            pygame.mixer.quit()
    elif operation == "play":
        pygame.mixer.init()
        pygame.mixer.music.load("sound.mp3")
        pygame.mixer.music.play()

def main():
    st.title("Edge-TTS VoiceGen")

    voices = get_voices()
    if not voices:
        st.error("No voices available. Please check your Edge TTS installation.")
        return

    edge_tts_model = st.selectbox('Select Edge TTS Model', voices)

    rate_options = list(range(-100, +210, 10))
    rate_option = st.selectbox('Select Rate Option', rate_options, index=rate_options.index(0))

    user_input = st.text_input("Enter your text here")
    if st.button('Generate and Play'):
        pygame_mixer_operation("stop")

        command = f'edge-tts --voice={edge_tts_model} --text="{user_input}"'
        if rate_option != 0:
            rate_option_str = f'+{rate_option}%' if rate_option > 0 else str(rate_option)
            command += f' --rate={rate_option_str}'
        command += ' --write-media sound.mp3'
        
        try:
            subprocess.run(command, shell=True)
        except Exception as e:
            st.error(f"Error running command: {e}")
            return

        pygame_mixer_operation("play")

if __name__ == "__main__":
    main()