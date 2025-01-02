import re
from src.text_preprocessing import llm


def script_generator(content):
  prompt = f"""Using the provided {content}, create a podcast script in the following format:

  - Structure: The script should consist of an engaging introduction by Sophia, followed by a back-and-forth conversation between the three characters (Sophia, Alex, and Ben). Each character should have clearly labeled lines (e.g., "Sophia:"), and their dialogue should flow naturally like a casual discussion.
  - Tone: Keep it conversational, easy to understand, and relatable, incorporating humor and real-life analogies where appropriate.
  - Content Goals: Simplify and explain key concepts in detailed form, provide practical examples, and address potential questions from the audience.
  - Character Roles:
    - Sophia: Insightful, empathetic, and the primary host of the discussion.
    - Alex: Analytical, thoughtful, and skilled at breaking down complex ideas.
    - Ben: Curious, light-hearted, and provides humorous or relatable commentary.

  End the script with a motivational takeaway led by Sophia and a group sign-off message."""

  result = llm.invoke(prompt)
  script = result.content
  
  return script

def remove_unwanted_symbols(texts):
  unwanted_symbols = "*&$%"
  pattern = f"[{re.escape(unwanted_symbols)}]"
  
  # Clean each string in the list
  cleaned_strings = [re.sub(pattern, "", string) for string in texts]
  return cleaned_strings

def name_and_content_list(script):

  pattern = [r"\[(\w+)\]:\s*(.+?)\n",r"\*\*(.+?)\*\*:\s(.+)",r"(\w+):\s*(.*)",r"\[(\w+)\]\s(.+)",r"\((.*?)\)\s+(.*)",r"\((\w+)\): (.+?)(?=\n\n|\Z)"]
  names = []
  contents = []
  flag = 0
  while len(names) == 0 and len(contents) == 0:
    matches = re.findall(pattern[flag], script)

    # Separate names and content into two lists
    names = [match[0] for match in matches]
    contents = [match[1] for match in matches]
    texts = remove_unwanted_symbols(contents)
    flag += 1
  
  return (names,texts)