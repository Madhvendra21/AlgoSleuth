#read index.txt and prepare documents, vocab, idf

import chardet
import re

def find_encoding(fname):
    r_file = open(fname, 'rb').read()
    result = chardet.detect(r_file)
    charenc = result['encoding']
    return charenc

filename = 'Qdata/indexLC.txt'
my_encoding = find_encoding(filename)

with open(filename, 'r', encoding=my_encoding) as f:
    lines=f.readlines()

def token_seperator(string_of_tokens):
    list_of_tokens=string_of_tokens.split()

    pattern = re.compile(r'^[\w-]+$')  # Regular expression pattern to match alphanumeric characters and hyphen

    return [word for word in list_of_tokens[1:] if pattern.match(word)]

def read_documents(file_paths):
    document_contents = []  # List to store the contents of the text documents

    for file_path in file_paths:
        my_encoding=find_encoding(file_path)
        with open(file_path, 'r', encoding=my_encoding) as file:
            content = ""  # Variable to store the content of the current document
            for line in file:
                if 'Example' in line:
                    break  # Stop reading when the line with "Example" is encountered
                content += line.rstrip('\n')  # Append the line to the document content

            document_contents.append(content.strip())  # Append the document content to the list

    return document_contents

file_paths=[]
for i in range (1,2227):
    each_file_path="Qdata/"+str(i)+"/"+str(i)+".txt"
    file_paths.append(each_file_path)
document_contents=read_documents(file_paths)

#print(document_contents)

vocab={}
documents=[]
i=0
for index, line in enumerate(lines):
    words=token_seperator(line)
    words_in_body=token_seperator(document_contents[index])
    i+=1
    words.append("ABCDEFGH?!")
    #Since all problems are getting this particular string, relatively, it would be alright
    words.extend(words_in_body)
    documents.append(words)
    words=set(words)
    for each_word in words:
        if each_word not in vocab:
            vocab[each_word]=1
        else:
            vocab[each_word]+=1

vocab = dict(sorted(vocab.items(), key=lambda item: item[1], reverse=True))

with open('tf-idf/vocab.txt', 'w',encoding="utf-8") as f:
    for key in vocab.keys():
        f.write("%s\n" % key)

with open('tf-idf/idf-values.txt', 'w',encoding="utf-8") as f:
    for key in vocab.keys():
        f.write("%s\n" % vocab[key])

with open('tf-idf/documents.txt', 'w',encoding="utf-8") as f:
    for document in documents:
        f.write("%s\n" % ' '.join(document))

inverted_index = {}
for index, document in enumerate(documents):
    for token in document:
        if token not in inverted_index:
            inverted_index[token] = [index]
        else:
            inverted_index[token].append(index)

with open('tf-idf/inverted-index.txt', 'w',encoding="utf-8") as f:
    for key in inverted_index.keys():
        f.write("%s\n" % key)
        f.write("%s\n" % ' '.join([str(doc_id) for doc_id in inverted_index[key]]))
