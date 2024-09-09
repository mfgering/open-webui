

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
  