from src.text_preprocessing import document_loader,doc_to_chunks,final_summary_builder
from src.script_writer import script_generator,name_and_content_list
from src.audio_generator import generate_podcast
import asyncio
if __name__ == "__main__":
  text = document_loader(filepath="artifact\\NIPS-2017-attention-is-all-you-need-Paper.pdf")
  
  split_docs = doc_to_chunks(text)
  
  content = asyncio.run(final_summary_builder(split_docs))
  
  script = script_generator(content)
  print(script)
  name_content = name_and_content_list(script)
  print(name_content[0])
  print()
  print(name_content[1])
  asyncio.run(generate_podcast(names=name_content[0],lines=name_content[1]))