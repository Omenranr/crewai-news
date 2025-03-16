#!/usr/bin/env python
from crew import NewsletterGenCrew
from TTS.api import TTS
from pydub import AudioSegment
from uuid import uuid4
from datetime import datetime

def generate_chunks(intput_text: str):
    chunks = intput_text.split('\n')
    input_list = [sentence for sentence in chunks if sentence != ""]
    combined_list = [input_list[i] + input_list[i + 1] for i in range(0, len(input_list) - 1, 2)]
    if len(input_list) % 2 != 0:
        combined_list.append(input_list[-1])
    return combined_list

def generate_audio_podcast(podcast_script: str, topic: str, presentator: str, speaker: str, language: str, velocity_X: float) -> str:
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=False)
    chunks = generate_chunks(podcast_script)
    generated_audio_paths = []
    # Generate speech for each chunk:
    for chunk in chunks:
        # generate speech by cloning a voice using default settings
        file_path = f"news/output_{topic}_{presentator}_{speaker}_{language}_{str(uuid4())}.wav"
        generated_audio_paths.append(file_path)
        tts.tts_to_file(text=chunk,
                        speaker=speaker,
                        file_path=file_path,
                        language=language)
    # init combined
    combined = AudioSegment.from_file(generated_audio_paths[0], format="wav")
    # Combine chunks:
    for i in range(1, len(generated_audio_paths)):
        sound = AudioSegment.from_file(generated_audio_paths[i], format="wav")
        combined += sound

    if velocity_X != 1.0:
        combined = combined.speedup(velocity_X, 150, 25)
        final_path = f'news/final_podcast_{topic}_{presentator}_{speaker}_{language}_{str(uuid4())}.mp3'

    combined.export(final_path, format = 'mp3')
    return final_path


def run():
    # Replace with your inputs, it will automatically interpolate any tasks and agents information
    inputs = {
        'topic': input('Enter the topic for yout newsletter: '),
        'presentator': input("Enter the presentator's name: "),
        'language': input("Choose a language (en, fr): ")
    }
    speed = input("Choose a speed rate for the podcast ex: (1, 1.5, 2): ")
    speakers = ['Claribel Dervla', 'Daisy Studious', 'Gracie Wise', 'Tammie Ema', 'Alison Dietlinde', 'Ana Florence', 'Annmarie Nele', 'Asya Anara', 'Brenda Stern', 'Gitta Nikolina', 'Henriette Usha', 'Sofia Hellen', 'Tammy Grit', 'Tanja Adelina', 'Vjollca Johnnie', 'Andrew Chipper', 'Badr Odhiambo', 'Dionisio Schuyler', 'Royston Min', 'Viktor Eka', 'Abrahan Mack', 'Adde Michal', 'Baldur Sanjin', 'Craig Gutsy', 'Damien Black', 'Gilberto Mathias', 'Ilkin Urbano', 'Kazuhiko Atallah', 'Ludvig Milivoj', 'Suad Qasim', 'Torcull Diarmuid', 'Viktor Menelaos', 'Zacharie Aimilios', 'Nova Hogarth', 'Maja Ruoho', 'Uta Obando', 'Lidiya Szekeres', 'Chandra MacFarland', 'Szofi Granger', 'Camilla Holmström', 'Lilya Stainthorpe', 'Zofija Kendrick', 'Narelle Moon', 'Barbora MacLean', 'Alexandra Hisakawa', 'Alma María', 'Rosemary Okafor', 'Ige Behringer', 'Filip Traverse', 'Damjan Chapman', 'Wulf Carlevaro', 'Aaron Dreschner', 'Kumar Dahl', 'Eugenio Mataracı', 'Ferran Simen', 'Xavier Hayasaka', 'Luis Moray', 'Marcos Rudaski']
    speaker = input(f"Choose a speaker from: {speakers}")
    print(f"Starting up the crew...")
    output = NewsletterGenCrew().crew().kickoff(inputs=inputs)
    print(f"Generating Audio Podcast about {inputs['topic']}...")
    audio_file_path = generate_audio_podcast(output.raw, inputs["topic"], inputs["presentator"], speaker, inputs["language"], float(speed))
    print(f"Finished generating audio podcast available at: {audio_file_path}")

run()