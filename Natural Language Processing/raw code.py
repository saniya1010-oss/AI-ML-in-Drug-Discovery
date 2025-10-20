!pip install biopython spacy nltk pandas networkx matplotlib
!pip install --upgrade biopython

from Bio import Entrez
import spacy, re, pandas as pd
import nltk
from nltk.tokenize import word_tokenize
import networkx as nx, matplotlib.pyplot as plt
from nltk.corpus import stopwords
stop = set(stopwords.words('english'))
import spacy

nlp = spacy.load(r"<path to the model if saved locally>")

nltk.download('punkt')
nltk.download('stopwords')

Entrez.email = 'youremail@gmail.com'
Entrez.api_key = 'YOUR_API_KEY' #optional

def fetch_pubmed_abstracts(query, max_records=10):
    '''Searches Pubmed for a given query, retrieves the pubmed IDs of
    a few matching papers, Fetch thier abstracts and titles,
    Returns:
    in a list of dictionaries'''
    h = Entrez.esearch(db='pubmed', term=query, retmax=max_records)
    ids = Entrez.read(h)['IdList']; h.close()
    if not ids:
        return []
    h = Entrez.efetch(db='pubmed', id=','.join(ids), retmode='xml'); recs = Entrez.read(h)
    h.close()
    out = []
    for art in recs.get('PubmedArticle', []):
        pmid = str(art['MedlineCitation']['PMID'])
        article = art['MedlineCitation']['Article']
        title = article.get('ArticleTitle','')
        abstract = ''
        if article.get('Abstract'):
            parts = article['Abstract'].get('AbstractText')
            if isinstance(parts, list):
                texts = []
                for p in parts:
                    if isinstance(p, str):
                        texts.append(p)
                    elif isinstance(p, dict):
                        texts.append(p.get('_',''))
                abstract = ' '.join(texts)
            elif isinstance(parts, dict):
                abstract = parts
            elif isinstance(parts, dict):
                abstract = parts.get(' ', '')
        out.append({'pmid': pmid, 'title': str(title), 'abstract': abstract})
    return out

docs = fetch_pubmed_abstracts('query', max_records=10) #specify any query
for d in docs:
    print(d['pmid'], '-', d['title'][:120])


def clean_text(txt):
    t = re.sub(r'\s+,',' ', txt or '').strip()
    t = re.sub(r'\[[0-9]+\]', '', t)
    return t

def remove_stopwords(txt):
    tokens = [w for w in word_tokenize(txt) if re.match(r'\w', w)]
    return ' '.join([w for w in tokens if w.lower() not in stop])

#nlp = spacy.load('en_core_web_sm')

def extract_entities(text):
    doc = nlp(text)
    return [(ent.text, ent.label_) for ent in doc.ents]

print(extract_entities(clean_text(docs[0]['abstract'])))


TRIGGERS = ['inhibit', 'inhibits', 'inhibitting', 'activate', 'activates', 'bind', 'binds', 'block', 'suppress', 'associated', 'cause', 'causes', 'increase', 'decrease']

def extract_relations(text):
    doc = nlp(text)
    relations = []
    for sent in doc.sents:
        ents = sent.ents
        if len(ents)<2:
            continue
        sent_l = sent.text.lower()
        for t in TRIGGERS:
            if t in sent_l:
                for i in range(len(ents)):
                    for j in range(i+1, len(ents)):
                        relations.append({'sentence': sent.text.strip(),
                                         'e1': ents[i].text,
                                         'e2': ents[j].text,
                                         'trigger': t})
                        break
    return relations

query = 'YOUR_QUERY'
docs = fetch_pubmed_abstracts(query, max_records=10)

triplets = []
for d in docs:
    txt = clean_text(d['abstract'])
    rels = extract_relations(txt)
    for r in rels:
        r.update({'pmid': d['pmid'], 'title': d['title']})
        triplets.append(r)

df = pd.DataFrame(triplets)
print('Triplets found', len(df))
display(df.head())
df.to_csv('pubmed_triplets.csv', index = False)

if not df.empty:
    G = nx.DiGraph()
    for _, row in df.iterrows():
        G.add_edge(row['e1'], row['e2'], label = row['trigger'])
    plt.figure(figsize=(10,10))
    pos = nx.spring_layout(G, seed = 2)
    nx.draw(G, pos, with_labels=True, node_size=100, font_size=9)
    nx.draw_networkx_edge_labels(G,pos,edge_labels=nx.get_edge_attributes(G, 'label')) #font_color='red'))
    plt.title('Knowledge Graph')
    plt.show()

else:
    print('No relations detected')

