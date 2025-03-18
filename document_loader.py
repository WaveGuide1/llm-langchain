from langchain_core.documents import Document

# Document loader
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
def text_file():
    file_path = "file.pdf"
    loader = PyPDFLoader(file_path)

    docs = loader.load()

    print(len(docs))

    print(f"{docs[0].page_content[:]}\n")
    print(docs[0].metadata)

    return f"{docs[0].page_content[:]}\n"
print(text_file())

# text_splitter = RecursiveCharacterTextSplitter(
#     chunk_size=1000, chunk_overlap=200, add_start_index=True
# )
# all_splits = text_splitter.split_documents(docs)

# print(all_splits)
