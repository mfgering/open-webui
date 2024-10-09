

RAG
  Node == chunk

  Connector: A data connector (often called a Reader) ingests data from different data sources and data  formats into Documents and Nodes.

  Retriever: generates queries to find relevant documents or nodes in the knowledge graph for answering user questions.

  Router: decides which node should be used to answer the question based on relevance, context, etc.

  Node Postprocessor: processes the retrieved nodes to generate answers and other outputs that are useful for users.

Insert a document into index via nodes, i.e. create nodes (chunks) 

query_engine = index.as_query_engine()
response = query_engine.query(
    "Write an email to the user given their background information."
)
print(response)

----

Adding a document 
  rag.main.process_doc takes in a file path and processes it to create chunks (nodes) which are then stored in the vector database.
    rag main.store_data_in_vector_db 
      creates splitter, nodes, calls:
      rag main.store_docs_in_vector_db 

----
create langchain_core.documents.bas.Document element for doc
create collection name for doc
do not call store_doc_in_vector_db() (it assumes )

parse/chunk the doc
store_docs_in_vector_db():

-------------

rag.utils.get_rag_context(): tracks citations.

-----------

import chromadb

# Initialize the Chroma client
client = chromadb.Client()

# Create or get a collection (database)
collection = client.create_collection("my_collection")

# Example data for the nodes
documents = [
    {"id": "node1", "text": "This is the first document."},
    {"id": "node2", "text": "This is the second document."},
    {"id": "node3", "text": "This is the third document."}
]

# Add the nodes (documents) to the collection
for doc in documents:
    collection.add(
        documents=[doc["text"]],
        ids=[doc["id"]]
    )

# Verify the documents have been added
print(collection.get(ids=["node1", "node2", "node3"]))

-----------

OI collects documents from query into a single context, uses rag template to generate response based on user's background information and document content.

---------

rag process:
  use doc tags for workspace/model as knowledge
  each doc in workspace is a file/tag
    get_rag_context() for query
      for each file, 
        query_collection(file)
          each file has many collection names (faq1txt, eg)
          query_doc(each collection name)
            return k results
          merge_and_sort_query_results() of all 
        # have sorted list of results for the file/collection
        # append results to relevent_contexts along with file/tag info
          e.g. faqs tag element with k results
        # append all extracted names to extracted_collections array
      for context in relevant_contexts:
        collect all the doc text content into single value
        create citation for each context:
          source, document, metadata
  have contexts, citations arrays
  insert text from contexts into rag template
  update messages with new body to include rag text; ollama vs openai differences
  add citations via data_items.append({"citations": citations})
  call LLM to get response
  
