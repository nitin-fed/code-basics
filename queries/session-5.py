# =============================================================================
# Code Basics - Session 5 (Nov 15, 2026) Project -5
#
# Topic: Advanced RAG and ReRanking
#   - Multi-format document loading (PDF, CSV)
#   - Chunking and embedding
#   - Re-ranking
# =============================================================================



import os
import time
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from groq import Groq
import pandas as pd

from langchain_huggingface import HuggingFaceEmbeddings # Dense Embedding
from langchain_qdrant import FastEmbedSparse # Parse Embedding
from langchain_qdrant import QdrantVectorStore, RetrievalMode # Vector DB
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains.retrieval import create_retrieval_chain

from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document 

from langchain_classic.retrievers import ContextualCompressionRetriever
from langchain_classic.retrievers.document_compressors import CrossEncoderReranker
from langchain_community.cross_encoders import HuggingFaceCrossEncoder

load_dotenv()


GROQ_API_KEY= os.getenv('GROQ_API_KEY')
EMBEDDING_MODEL=os.getenv('EMBEDDING_MODEL')
GROQ_MODEL = 'openai/gpt-oss-20b'
groq_client = Groq()
COLLECTION_NAME = 'project-5'

FINANCE_DOC_URL="documents/session-5/borrower_quarterly_financials.csv"
FINANCE_PDF_URL=["documents/session-5/master_credit_facility_agreement.pdf", "documents/session-5/borrower_financial_reporting.pdf" ]

llm = ChatGroq(
    model=GROQ_MODEL,
    temperature=1,
    max_tokens=None,
    reasoning_format="parsed",
    timeout=None,
    max_retries=2,
)


# txt = "This is sample text, contains my name, according to document it is Nitin, and my last name is sharma, ther other name is Kevin which is not my name, he is a film star"

# msg = llm.invoke(
#     "Answer the question below using ONLY the text. "
#     "If the answer is not in the text, say 'I have no answer.'\n\n"
#     f"Text: {txt}\n\n"
#     "Question: whats the name of film star?"
# )

# print(msg.content)

#******** Loadign CSV file
try: 
    df = pd.read_csv(FINANCE_DOC_URL)
except pd.errors.EmptyDataError:
    print("The CSV is empty")
except pd.errors.ParserError as e:
    print(f"Couldn't parse the CSV: {e}")          # malformed rows, wrong delimiter
except Exception as e:
    print(f"Unexpected error: {type(e).__name__}: {e}")
 
finance_docs =[]
for id, row in df.iterrows():
    content = "\n".join(f"{col}: {val}" for col, val in row.items())
    document = Document(
        page_content=content,
        metadata={"Source": "Quarterly Report", "category": "Financial", "id": id }
    )
    finance_docs.append(document)

print(f"Created {len(finance_docs)} document for Financial report.")

pdf_docs = []
for path in FINANCE_PDF_URL:
    pdf_docs.extend(PyPDFLoader(path).load())


# ***** Chunking the PDF pages
splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,      # characters per chunk
    chunk_overlap=150,    # shared characters between neighbouring chunks
)
pdf_chunks = splitter.split_documents(pdf_docs)
pdf_chunks_with_metadata = []

for i, chunk in enumerate(pdf_chunks):
    producer = chunk.metadata.get("producer", "")[:8]   # first 8 characters
    chunk.metadata["creator"] = producer
    chunk.metadata["chunk_id"] = i
    pdf_chunks_with_metadata.append(chunk)

all_docs = finance_docs + pdf_chunks_with_metadata



############## Dense Embedding
start_time = time.perf_counter()
dense_embedding = HuggingFaceEmbeddings(
    model_name=EMBEDDING_MODEL,
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": True },
    show_progress=True,
    multi_process=False #does not work on cpu works only on 1000+ document on GPU
)
dense_embedding_time = time.perf_counter() - start_time
print(f"dense_embedding took {dense_embedding_time:.2f} seconds to initialize.")

############## Sparse Embedding
sparse_embedding = FastEmbedSparse(
    mode_name="Qdrant/bm25",
    batch_size=32
)

# Save to Qdrant Vector stores BOTH dense and sparse vectors
# ************** IMP uncomment this Create New if data updated
vectorstore = QdrantVectorStore.from_documents(
    documents=all_docs,
    embedding=dense_embedding,
    sparse_embedding=sparse_embedding,
    url="http://localhost:6333",
    collection_name=COLLECTION_NAME,
    retrieval_mode=RetrievalMode.HYBRID, #Reciprocal Rank Fusion - combines both embedding
    force_recreate=True # Delete older records, otherwise false value will keep adding records to DB. 
) 

# Save to Qdrant Vector stores BOTH dense and sparse vectors
# vectorstore = QdrantVectorStore.from_existing_collection(
#     # documents=all_docs,
#     embedding=dense_embedding,
#     sparse_embedding=sparse_embedding,
#     url="http://localhost:6333",
#     collection_name=COLLECTION_NAME,
#     retrieval_mode=RetrievalMode.HYBRID, 
#     # force_recreate=True # Delete older records, otherwise false value will keep adding records to DB. 
# ) 

hybrid_retriever = vectorstore.as_retriever(
    search_kwargs={"k": 5}
)
 
#PROMPT Template
system_prompt = """You are a helpful customer support assistant.
Answer the customer's question using ONLY the information provided in the context below.
If the answer is not in the context, say "I don't have that information."
Keep answers concise and friendly.
Context:
{context}"""

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}"),
])

question = "Which law governs the credit agreement and where must disputes be heard?"
# question =  "What was the EBITDA margin in Q1-2024"
# question = "What was Halcyon Precision Manufacturing's revenue in Q4-2024?"
# question = "Show me name of record id fin-031"
question_answer_chain = create_stuff_documents_chain(llm, prompt)
hybrid_rag_chain = create_retrieval_chain(hybrid_retriever, question_answer_chain)

result = hybrid_rag_chain.invoke({"input": question})

print("=" * 60)
print(f"Question: {question}")
print(f"\nAnswer: {result['answer']}")
print("=" * 60)

# ***************************** Re-Ranking ************

# Load cross-encoder model (downloads ~270MB on first run)
cross_encoder = HuggingFaceCrossEncoder(
    model_name="cross-encoder/ms-marco-MiniLM-L-6-v2"
)

# Wrap it as a LangChain document compressor
reranker = CrossEncoderReranker(
    model=cross_encoder,
    top_n=3     # keep only top-3 after reranking
)
broad_retriever = vectorstore.as_retriever(
    search_kwargs={"k": 10}    # fetch 10, rerank down to 3
)

reranking_retriever = ContextualCompressionRetriever(
    base_compressor=reranker,
    base_retriever=broad_retriever
)

print("Retrieval pipeline:")
print("  1. Hybrid search → Top-10 candidates")
print("  2. Cross-encoder reranker → Top-3 best documents")

reranking_rag_chain = create_retrieval_chain(
    reranking_retriever,
    create_stuff_documents_chain(llm, prompt)
)

print("✅ Hybrid RAG + Reranking chain ready")

# query = "How do I check my data balance?"
candidates = broad_retriever.invoke(question) 

print(f"Retrieved {len(candidates)} candidates. Now scoring each with cross-encoder...\n")

pairs = [[question, doc.page_content] for doc in candidates]
scores = cross_encoder.score(pairs)
scored = sorted(zip(scores, candidates), reverse=True)

# for rank, (score, doc) in enumerate(scored, 1):
#     cat = doc.metadata.get("category", "")
#     print(f"Rank {rank}  score={score:.4f}  category={cat}")
#     print(f"  {doc.page_content[:100]}...")
#     print()


resp = reranking_rag_chain.invoke({"input": question})
print(f"Docs sent to LLM after reranking: {len(resp['context'])}")
for doc in resp["context"]:
    print(f"  category={doc.metadata.get('category', '')}  {doc.page_content[:100]!r}")
print("=" * 50)
print(f"Question: {question}")
print(f"Answer: {resp["answer"]}")
print("=" * 50)
  