# PDF2Podcast

PDF2Podcast is a Streamlit-based application that transforms any PDF document into an audio podcast along with a generated script. The project takes users through an automated pipeline of document processing, summarization, and audio generation.

## Features

- Upload a PDF document.
- Automatically extract text and split it into meaningful chunks.
- Generate a summary for each chunk and a final overall summary.
- Create a structured script based on the summary.
- Convert the script into an audio podcast using NLP techniques.
- Download the podcast audio and the generated script.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/pdf2podcast.git
   cd pdf2podcast
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   streamlit run app.py
   ```

## How to Use

1. **Upload PDF**: Click on the file uploader in the application to upload your PDF document.

2. **Processing Steps**:
   - The document is loaded and text is extracted.
   - The extracted text is split into chunks.
   - Summaries are generated for each chunk and concatenated into a final summary.
   - A structured script is generated from the summary.
   - The script is split into sections for audio synthesis.
   - Audio is generated for each section and merged into a single podcast.

3. **Download Outputs**:
   - Once processing is complete, you can download the podcast audio file and the generated script as a text file.

## Process Overview

1. **Document Load**: The user uploads a PDF document.
2. **Text Extraction**: Extracts textual content from the uploaded PDF.
3. **Splitting into Chunks**: Divides the extracted text into smaller, manageable chunks for processing.
4. **Generate Summary of Each Chunk**: Summarizes each text chunk to extract key points.
5. **Concatenate All Summaries and Generate Final Summary**: Combines individual summaries into a cohesive overall summary.
6. **Generate Script**: Converts the final summary into a well-structured script.
7. **Use NLP and Split the Script**: Utilizes NLP techniques to segment the script for audio synthesis.
8. **Generate Each Voice**: Creates audio for each segment of the script.
9. **Merge All the Voices into a Single File**: Combines individual audio segments into a complete podcast.

## Example

1. Upload a PDF file, such as `example.pdf`.
2. The application processes the document and provides:
   - A downloadable podcast audio file, e.g., `example_podcast.mp3`.
   - A downloadable script file, e.g., `example_script.txt`.

## Dependencies

- Python 3.8+
- Streamlit
- PyPDF2 (or other PDF parsing library)
- Transformers (for summarization and NLP tasks)
- edge_tts or any other text-to-speech library
- FFmpeg (for audio merging)

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request to suggest improvements or report bugs.

## Contact

For any inquiries or support, contact abhisekmaharana9861@gmail.com.
