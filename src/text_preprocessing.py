import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain import hub
from langchain_core.prompts import ChatPromptTemplate
import operator
from typing import Annotated, List, Literal, TypedDict
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain.chains.combine_documents.reduce import (
    acollapse_docs,
    split_list_of_docs,)
from langchain_core.documents import Document
from langgraph.constants import Send
from langgraph.graph import END, START, StateGraph
import tempfile

# API key
os.environ['NVIDIA_API_KEY']="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"
os.environ['LANGCHAIN_API_KEY'] = "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"

#importing the model
llm = ChatNVIDIA(model="meta/llama3-70b-instruct")

# Document loader and text extraction
def document_loader(filepath):
  with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
    temp_file.write(filepath.read())  # Write the contents of the uploaded file
    temp_path = temp_file.name  
    
  loader = PyPDFLoader(temp_path)
  text = loader.load()
  
  return text

# Splitting the text into chunks
def doc_to_chunks(text):
  text_splitter = CharacterTextSplitter.from_tiktoken_encoder(chunk_size=5000, chunk_overlap=0)
  split_docs = text_splitter.split_documents(text)
  
  return split_docs

# Generate summary of each chunk and concatinate all summeries to generate a final summary
def reduced_prompt():
  
  reduce_template = """
  The following is a set of summaries:
  {docs}
  Take these and give a detailed summary
  of the main themes in around 5000 words.
  """

  reduce_prompt = ChatPromptTemplate([("human", reduce_template)])
  return reduce_prompt

token_max = 5000 # maximum number of tokens


def length_function(documents: List[Document]) -> int:
    """Get number of tokens for input contents."""
    return sum(llm.get_num_tokens(doc.page_content) for doc in documents)


# This will be the overall state of the main graph.
# It will contain the input document contents, corresponding
# summaries, and a final summary.
class OverallState(TypedDict):
    # Notice here we use the operator.add
    # This is because we want combine all the summaries we generate
    # from individual nodes back into one list - this is essentially
    # the "reduce" part
    contents: List[str]
    summaries: Annotated[list, operator.add]
    collapsed_summaries: List[Document]
    final_summary: str


# This will be the state of the node that we will "map" all
# documents to in order to generate summaries
class SummaryState(TypedDict):
    content: str


# Here we generate a summary, given a document
async def generate_summary(state: SummaryState):
    map_prompt = hub.pull("rlm/map-prompt")
    prompt = map_prompt.invoke(state["content"])
    response = await llm.ainvoke(prompt)
    return {"summaries": [response.content]}


# Here we define the logic to map out over the documents
# We will use this an edge in the graph
def map_summaries(state: OverallState):
    # We will return a list of `Send` objects
    # Each `Send` object consists of the name of a node in the graph
    # as well as the state to send to that node
    return [
        Send("generate_summary", {"content": content}) for content in state["contents"]
    ]


def collect_summaries(state: OverallState):
    return {
        "collapsed_summaries": [Document(summary) for summary in state["summaries"]]
    }


async def _reduce(input: dict) -> str:
    reduce_prompt = reduced_prompt()
    prompt = reduce_prompt.invoke(input)
    response = await llm.ainvoke(prompt)
    return response.content


# Add node to collapse summaries
async def collapse_summaries(state: OverallState):
    doc_lists = split_list_of_docs(
        state["collapsed_summaries"], length_function, token_max
    )
    results = []
    for doc_list in doc_lists:
        results.append(await acollapse_docs(doc_list, _reduce))

    return {"collapsed_summaries": results}


# This represents a conditional edge in the graph that determines
# if we should collapse the summaries or not
def should_collapse(
    state: OverallState,
) -> Literal["collapse_summaries", "generate_final_summary"]:
    num_tokens = length_function(state["collapsed_summaries"])
    if num_tokens > token_max:
        return "collapse_summaries"
    else:
        return "generate_final_summary"


# Here we will generate the final summary
async def generate_final_summary(state: OverallState):
    response = await _reduce(state["collapsed_summaries"])
    return {"final_summary": response}

async def final_summary_builder(split_docs):
  # Construct the graph
  # Nodes:
  graph = StateGraph(OverallState)
  graph.add_node("generate_summary", generate_summary)  # same as before
  graph.add_node("collect_summaries", collect_summaries)
  graph.add_node("collapse_summaries", collapse_summaries)
  graph.add_node("generate_final_summary", generate_final_summary)

  # Edges:
  graph.add_conditional_edges(START, map_summaries, ["generate_summary"])
  graph.add_edge("generate_summary", "collect_summaries")
  graph.add_conditional_edges("collect_summaries", should_collapse)
  graph.add_conditional_edges("collapse_summaries", should_collapse)
  graph.add_edge("generate_final_summary", END)

  app = graph.compile()
  
  async for step in app.astream(
    {"contents": [doc.page_content for doc in split_docs]},
    {"recursion_limit": 10},):
    print(list(step.keys()))
    
  content = step['generate_final_summary']['final_summary']
  
  return content
