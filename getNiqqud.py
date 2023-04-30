import requests
from bs4 import BeautifulSoup
import re
from transformers import AutoTokenizer, AutoModel
import torch
from scipy.spatial.distance import cosine

# Function to remove non-alpha characters except spaces
def remove_non_alpha(text):
    return re.sub('[^a-zA-Z\s]', '', text)

# Function to get SBERT embeddings for given sentences
def get_sbert_embeddings(model, tokenizer, sentences):
    inputs = tokenizer(sentences, return_tensors='pt', padding=True, truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    embeddings = outputs.pooler_output
    return embeddings

# Function to compute semantic similarity between two sentences
def semantic_similarity(sentence1, sentence2, model, tokenizer):
    embeddings = get_sbert_embeddings(model, tokenizer, [sentence1, sentence2])
    similarity_score = 1 - cosine(embeddings[0], embeddings[1])
    return similarity_score

# Function to get translations from the given URL
def get_translation(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    translations = {}

    translation_blocks = soup.find_all("div", class_="Translation_content_heToen")

    for trans_item in translation_blocks:
        niqqud = trans_item.find("span", class_="Translation_spTop_heToen").text.strip()
        words = trans_item.find("div", class_="normal_translation_div").text
        translations[niqqud] = [remove_non_alpha(x).strip() for x in words.replace(",", ";").split(";")]

    return translations

# Function to get the closest matching niqqud for a given word and its English translation
def getNiqqud(word, english):
    url = "https://www.morfix.co.il/en/" + word
    translations = get_translation(url)

    model_name = "sentence-transformers/paraphrase-distilroberta-base-v1"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)

    scores = {}

    for niqqud, meanings in translations.items():
        max_score = 0
        for meaning in meanings:
            similarity = semantic_similarity(english, meaning, model, tokenizer)
            max_score = max(max_score, similarity)
        scores[niqqud] = max_score

    return max(scores, key=scores.get) if translations else None

print(getNiqqud("רואה", "Sees"))
