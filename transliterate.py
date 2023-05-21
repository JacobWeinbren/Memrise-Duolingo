import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration

# Load the trained model and tokenizer
tokenizer = T5Tokenizer.from_pretrained("trained_model")
model = T5ForConditionalGeneration.from_pretrained("trained_model")

def transliterate(hebrew_word, num_beams=5, max_length=128):
    input_ids = tokenizer.encode(hebrew_word, return_tensors="pt")
    output_ids = model.generate(input_ids, num_beams=num_beams, max_length=max_length)
    transliteration = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    return transliteration

hebrew_word = "עברית"
transliteration = transliterate(hebrew_word)
print(transliteration)  # Expected output: 'ivrit'