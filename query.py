#This one is old, and gives wrong links


import math

def load_vocab():
    vocab = {}
    with open('tf-idf/vocab.txt', 'r') as f:
        vocab_terms = f.readlines()
    with open('tf-idf/idf-values.txt', 'r') as f:
        idf_values = f.readlines()
    
    for (term,idf_value) in zip(vocab_terms, idf_values):
        vocab[term.strip()] = int(idf_value.strip())
    
    return vocab

def load_documents():
    documents = []
    with open('tf-idf/documents.txt', 'r') as f:
        documents = f.readlines()
    documents = [document.strip().split() for document in documents]

    #print('Number of documents: ', len(documents))
    #print('Sample document: ', documents[0])
    return documents

def load_inverted_index():
    inverted_index = {}
    with open('tf-idf/inverted-index.txt', 'r') as f:
        inverted_index_terms = f.readlines()

    for row_num in range(0,len(inverted_index_terms),2):
        term = inverted_index_terms[row_num].strip()
        documents = inverted_index_terms[row_num+1].strip().split()
        inverted_index[term] = documents
    
    print('Size of inverted index: ', len(inverted_index))
    return inverted_index

def load_Q_links():
    with open('Qdata/leetcode.txt','r') as f:
        links=f.readlines()
    return links

vocab_idf_values = load_vocab()
documents = load_documents()
inverted_index = load_inverted_index()
Q_links=load_Q_links()


def get_tf_dictionary(term):
    tf_values = {}
    if term in inverted_index:
        for document in inverted_index[term]:
            if document not in tf_values:
                tf_values[document] = 1
            else:
                tf_values[document] += 1
                
    for document in tf_values:
        tf_values[document] /= len(documents[int(document)])
    
    return tf_values

def get_idf_value(term):
    return math.log(len(documents)/vocab_idf_values[term])

# New 2D list excluding elements after "ABCDEFGH"
new_list = []

for sublist in documents:
    new_sublist = []
    for item in sublist:
        if item == 'ABCDEFGH?!':
            break
        new_sublist.append(item)
    new_list.append(new_sublist)

documents=new_list

#print(documents[1])

def calculate_sorted_order_of_documents(query_terms):
    potential_documents = {}
    for term in query_terms:
        if term not in vocab_idf_values:
            continue
        if vocab_idf_values[term] == 0:
            continue
        tf_values_by_document = get_tf_dictionary(term)
        idf_value = get_idf_value(term)
        print(term,tf_values_by_document,idf_value)
        for document in tf_values_by_document:
            if document not in potential_documents:
                potential_documents[document] = tf_values_by_document[document] * idf_value
            potential_documents[document] += tf_values_by_document[document] * idf_value

    print(potential_documents)
    # divite by the length of the query terms
    for document in potential_documents:
        potential_documents[document] /= len(query_terms)

    potential_documents = dict(sorted(potential_documents.items(), key=lambda item: item[1], reverse=True))

    for document_index in potential_documents:
        print('Document: ', documents[int(document_index)], ' Score: ', potential_documents[document_index],'\n','Link: ', Q_links[int(document_index)],'\n')


query_string = input('Enter your query: ')
query_terms = [term.lower() for term in query_string.strip().split()]

print(query_terms)
calculate_sorted_order_of_documents(query_terms)