import os
import io
import asyncio
import tempfile
from pydub import AudioSegment
from edge_tts import Communicate


# Define text-to-audio conversion
"""async def text_to_audio(text, voice_name, temp_file):
    communicate = Communicate(text, voice=voice_name, rate="+0%")
    await communicate.save(temp_file)
    return temp_file


# Generate podcast audio and merge into a single file
async def generate_podcast(names, lines, output_file="artifact\\pdf_podcast.mp3"):
    voices = ['en-AU-WilliamNeural', 'en-US-JennyNeural', 'en-US-GuyNeural']
    merged_audio = AudioSegment.silent(duration=0)  # Start with an empty audio segment
    temp_file = "artifact\\chunk.mp3"  # Temporary file for each segment

    for i in range(len(names)):
        input_text = lines[i]
        name = names[i]

        # Choose the voice based on the speaker's name
        if name == 'Sophia':
            voice = voices[1]
        elif name == 'Ben':
            voice = voices[0]
        elif name == 'Alex':
            voice = voices[2]
        else:
            voice = voices[1]

        # Generate individual audio
        await text_to_audio(input_text, voice, temp_file)

        # Load the generated audio and append it to the merged audio
        segment = AudioSegment.from_file(temp_file, format="mp3")
        merged_audio += segment

        # Clean up the temporary file
        if os.path.exists(temp_file):
            os.remove(temp_file)

    # Export the final merged audio
    merged_audio.export(output_file, format="mp3")
    print(merged_audio)
    print(f"Podcast audio saved to {output_file}")"""
    
 
# Define text-to-audio conversion
async def text_to_audio(text, voice_name):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
        communicate = Communicate(text, voice=voice_name, rate="+0%")
        await communicate.save(temp_audio.name)
        return temp_audio.name  # Return the path of the temporary file

# Generate podcast audio and store in memory
async def generate_podcast(names, lines):
    voices = ['en-AU-WilliamNeural', 'en-US-JennyNeural', 'en-US-GuyNeural']
    merged_audio = AudioSegment.silent(duration=0)  # Start with an empty audio segment

    temp_files = []  # To keep track of temporary files for cleanup

    try:
        for i in range(len(names)):
            input_text = lines[i]
            name = names[i]

            # Choose the voice based on the speaker's name
            if name == 'Sophia':
                voice = voices[1]
            elif name == 'Ben':
                voice = voices[0]
            elif name == 'Alex':
                voice = voices[2]
            else:
                voice = voices[1]

            # Generate individual audio and get the temp file path
            temp_file_path = await text_to_audio(input_text, voice)
            temp_files.append(temp_file_path)

            # Load the generated audio and append it to the merged audio
            segment = AudioSegment.from_file(temp_file_path, format="mp3")
            merged_audio += segment

        # Export the final merged audio to an in-memory buffer
        audio_buffer = io.BytesIO()
        merged_audio.export(audio_buffer, format="mp3")
        audio_buffer.seek(0)  # Reset the buffer to the beginning
        return audio_buffer  # Return the in-memory audio buffer
    finally:
        # Clean up temporary files
        for temp_file in temp_files:
            if os.path.exists(temp_file):
                os.remove(temp_file)


