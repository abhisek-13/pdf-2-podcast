from src.text_preprocessing import document_loader,doc_to_chunks,final_summary_builder
from src.script_writer import script_generator,name_and_content_list
from src.audio_generator import generate_podcast
import asyncio
import streamlit as st

import sys
venv_path = sys.prefix
print(venv_path)

async def pdf_2_podcast(uploaded_file):
  
  text = document_loader(filepath=uploaded_file)
  
  split_docs = doc_to_chunks(text)
  
  content = await final_summary_builder(split_docs)
  
  script = script_generator(content)
  
  name_content = name_and_content_list(script)

  final_audio = await generate_podcast(names=name_content[0],lines=name_content[1])
  
  return script,final_audio

def main():
  st.title("PDF to Podcast Generator")
  st.write("Upload a PDF document to generate a podcast script and audio.")

  uploaded_file = st.file_uploader("", type=["pdf"])
    
  if st.button("Generate Podcast"):
      
      with st.spinner("Processing..."):
        script,audio = asyncio.run(pdf_2_podcast(uploaded_file)) 
        
      # Add audio player
      st.write("### Listen to the Podcast")
      st.audio(audio.getvalue(), format="audio/mp3")
       
      st.write("### Here is the Script of the Podcast:")
      st.write(script)
      
      




  
if __name__ == "__main__":
  main()
