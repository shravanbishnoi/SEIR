"""
In this script, I have done the following necessary steps to 
compute pairwise similarity between each document to every other.
I have read content from all docs and wrote in a single file separated 
with <NEW: docid> for efficient processing.
Steps:
> Built a dictionary of <DOCNO> entry to document-id(1-N) using function buildDocDict(collection_path).
> Extracted <TITLE> and <TEXT> part then case normalised the text and then tokenized
  every document such that any sequence of alphanumeric characters and an underscore form a
  token (a-z, 0-9, _), each token is an index term.
> Built a dictionary of token to token-id (numeric: 1-M) using tokenize(docIDs, file)
> Computed token idfs  using computeIDFs(docids, docContent, indexTerms)
> Built a tf x idf cosine normalized document vector using computeTF_IDF(docContent, tokenIDFs)
> Computed pairwise document similarity and sorted document pairs from most similar to least similar 
  values, output is a list of tuples (doc1, doc2, their similarity)

  YOU NEED TO PROVIDE COLLECTION PATH AS SYSTEM ARGUMENT

Author: Shravan
Submission date: 25-04-2024
"""
import sys, os, time, math

def main():
    start_Time = time.time()
    try:
        collection_path = sys.argv[1]
    except:
        print("Please provide the collection path as an cmd line argument.")
        exit()
    file_dir = os.path.dirname(__file__)
    file = f"{file_dir}/all.txt"
    if not(os.path.exists(file)):
        writeContent(collection_path, file)
    docIDs, docnos = buildDocDict(collection_path)          # {<DOCNO> : doc-id (1-N)}
    docContent, indexTerms = tokenize(docIDs, file)         # creating index-terms
    tokenIDFs = computeIDFs(docIDs, docContent, indexTerms)
    vectors = computeTF_IDF(docContent, tokenIDFs)          # computing tf x idf doc vectors
    similarities = computeCosineSimilarity(vectors, docnos) # computing similarities
    print("Document 1, Document 2, Their similarity: ")
    for i in range(50):
        print(similarities[i])
    print("Total time taken to process: ", time.time()-start_Time)


### ---------------------- #### -------------------------- ###

def buildDocDict(folder_path):
    """Returns a dictionary of <DOCNO> entry to doc-id numeric(1-N) and
    a list of <DOCNO>

    Parameter folder_path: folder containing all the doc files.
    Precondition: must be a valid folder path.
    """
    files = os.listdir(folder_path)
    docs = {}
    docno = []
    for count, file in enumerate(files):
        docs[file] = count + 1
        docno.append(file)
    return docs, docno


def _extract(content, tag):
    """Returns a string containing the text inside the given tag
    in the content of the doc.
    
    Parameter content: content is a HTML/HML content of a doc.
    Precondition: must be a string.

    Parameter tag: tag is a HTML/HML tag inside the content.
    Precondition: must be a valid tag.
    """
    try:
        start = content.find(f"<{tag}>") + len(f"<{tag}>")
        end = content.find(f"</{tag}>")
        data = content[start:end].strip()
        return data.lower()
    except:
        return f"{tag} not found!"


def _getContent(file):
    """Returns list contents of all the documents present in file.

    Parameter file: file containing all the documents' content in one file.
    Precondition: must be a valid file path.
    """
    with open(file, "r") as file:
        content = file.read()
        content = content.split(f"<NEW: ")
        i = 0
        while (i<len(content)):
            if (content[i].strip())!='':
                content[i] = content[i][content[i].find('>')+1:]
                content[i] = content[i].replace("\n", " ")
                content[i] = content[i].lower().strip()
                i += 1
            else:
                content.pop(i)
    return content


def tokenize(docids, file):
    """
    Read and tokenize content from the file.

    Parameter docids: dict containing <DOCNO>: docid(1-N).
    Precondition: must be a valid dict with docids.

    Parameter file: containing content of docs.
    Precondition: must be a valid file path.
    """
    content = _getContent(file)
    TOKENS = {}     # initialize dict for tokens:(1-M)
    docContent = {} # {docid: list of terms in doc}
    count = 1
    for doc in content:
        docno = _extract(doc, 'docno')
        docid = docids[docno]
        data = _extract(doc, 'title')        # extract title from doc
        data += " " + _extract(doc, 'text')  # extract text from doc
        docContent[docid] = {}
        for word in data.split():
            if (word.strip().isalnum()):
                if (word.strip() not in TOKENS):
                    TOKENS[word.strip()] = count
                    count += 1
                if (word.strip() not in docContent[docid]):
                    docContent[docid][word] = 1
                else:
                    docContent[docid][word] += 1
            else:
                token = ""
                for letter in word:
                    if (letter.isalnum() or letter=="_"):
                        token += letter
                    elif (token.strip()!=""):
                        if (token not in TOKENS):
                            TOKENS[token] = count
                            count += 1
                        if (token.strip() not in docContent[docid]):
                            docContent[docid][token] = 1
                        else:
                            docContent[docid][token] += 1
                        token = ""
    return docContent, TOKENS


def computeIDFs(docids, docContent, tokens):
    """Return a dictionary such that {token: idf}

    Parameter docids: dict containing <DOCNO>: docid(1-N).
    Precondition: must be a valid dict with docids.

    Parameter docContent: dict of dict containing {docid: {token: count}}.
    Precondition: must be a valid doc content dict.
    
    Parameter tokens: dict containing index-terms.
    Precondition: must be a valid dict of tokens(index-terms).
    """
    tokenCount = {}
    for token in tokens:
        for words in docContent.values():
            if (token not in tokenCount) and (token in words):
                tokenCount[token] = 1
            elif (token in tokenCount) and (token in words):
                tokenCount[token] += 1
    tokenIDFs = {}
    for token, DocsWithToken in tokenCount.items():
        collectionSize = len(docids)
        tokenIDFs[token] = math.log(collectionSize/DocsWithToken) # IDF
    return tokenIDFs


def computeTF_IDF(docContent, tokenIDFs):
    """Returns a dict of dict {docids: {token: score}}

    Parameter docContent: dict of dict containing {docid: {token: count}}.
    Precondition: must be a valid doc content dict.

    Parameter tokenIDFs: dict containing {token: idf}.
    Precondition: must be a valid dict of tokenIDFs.
    """
    tf_idf = {}
    for docid, terms in docContent.items():
        tf_idf[docid] = {}
        for term in terms:
            tf = terms[term]/len(terms)
            score = tf*(tokenIDFs[term])   # TF x IDF
            tf_idf[docid][term] = score
    # building cosine normalised document vector
    vectors = {}
    for docid, scores in tf_idf.items():
        squaredSum = sum(scr**2 for scr in scores.values())
        euclideanNorm = math.sqrt(squaredSum)
        # cosine normalised vector
        vectors[docid] = {token: score/euclideanNorm for token, score in scores.items()}
    return vectors


def computeCosineSimilarity(vectors, docnos):
    """
    Returns a list of tuples such that [(doc1, doc2, their similarity), ...]

    Parameter vectors: dict of dict {docids: {token: score}}
    Precondition: must be a valid dict.
    """
    matrix = []
    for doc1 in range(1, len(vectors)+1):
        for doc2 in range(doc1, len(vectors)+1):
            if doc1!=doc2:
                total = 0
                for term, score in vectors[doc1].items():
                    if (term in vectors[doc2]):
                        total += score*(vectors[doc2][term])
                matrix.append((docnos[doc1-1], docnos[doc2-1], total))
    return sorted(matrix, key=lambda x: x[2], reverse=True)


def writeContent(folder_path, file_path):
    """
    Reads all the files one by one from the given folder
    and write content of all into one file 'all.txt' 

    Parameter folder_path: folder containing all the doc files.
    Precondition: must be a valid folder path.

    Parameter file_path: path of the file to write the content.
    Precondition: must be a valid file path.
    """
    files = os.listdir(folder_path)
    for count, file in enumerate(files):
        with open(f"{folder_path}/{file}", "r") as file:
            content = file.read()   # reading content
            content = f"<NEW: {count}>\n" + content 
            with open(file_path, 'a') as file:
                file.write(content) # writing it to 'all.txt'


if __name__ == "__main__":
    main()