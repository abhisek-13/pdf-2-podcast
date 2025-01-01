from src.text_preprocessing import document_loader,doc_to_chunks,final_summary_builder
import asyncio
if __name__ == "__main__":
  text = document_loader(filepath="artifact\\NIPS-2017-attention-is-all-you-need-Paper.pdf")
  split_docs = doc_to_chunks(text)
  
  content = asyncio.run(final_summary_builder(split_docs))
  print(content)