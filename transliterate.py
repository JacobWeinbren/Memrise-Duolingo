import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
import pickle

# Load the trained models
encoder_model = load_model('encoder_model.h5')
decoder_model = load_model('decoder_model.h5')

# Load dictionaries and sequence lengths
with open('char_indices.pkl', 'rb') as f:
    input_token_index, target_token_index = pickle.load(f)
with open('sequence_lengths.pkl', 'rb') as f:
    max_encoder_seq_length, max_decoder_seq_length = pickle.load(f)

# Get the number of tokens (unique characters) in each dictionary
num_encoder_tokens = len(input_token_index)
num_decoder_tokens = len(target_token_index)

# Reverse lookup token index to decode sequences back to something readable
reverse_input_char_index = {i: char for char, i in input_token_index.items()}
reverse_target_char_index = {i: char for char, i in target_token_index.items()}


def decode_sequence(input_seq):
    """Decode the input sequence to find the predicted sentence."""

    # Encode the input as state vectors
    states_value = encoder_model.predict(input_seq)

    # Generate empty target sequence of length 1
    target_seq = np.zeros((1, 1, num_decoder_tokens))

    # Populate the first character of target sequence with the start character
    target_seq[0, 0, target_token_index['\t']] = 1.

    # Loop to decode the sequence
    decoded_sentence = ''
    while True:
        output_tokens, h, c = decoder_model.predict(
            [target_seq] + states_value)
        sampled_token_index = np.argmax(output_tokens[0, -1, :])
        sampled_char = reverse_target_char_index[sampled_token_index]
        decoded_sentence += sampled_char

        if sampled_char == '\n' or len(decoded_sentence) > max_decoder_seq_length:
            break

        target_seq = np.zeros((1, 1, num_decoder_tokens))
        target_seq[0, 0, sampled_token_index] = 1.
        states_value = [h, c]
    return decoded_sentence


def transliterate(word):
    """Convert a Hebrew word to its English transliteration."""

    # Convert the word to the proper input format
    encoder_input_data = np.zeros(
        (1, max_encoder_seq_length, num_encoder_tokens), dtype='float32')
    for t, char in enumerate(word):
        encoder_input_data[0, t, input_token_index[char]] = 1.
    encoder_input_data[0, t + 1:, input_token_index[' ']] = 1.

    # Decode the word
    decoded_sentence = decode_sequence(encoder_input_data[0:1])
    return decoded_sentence.strip()


hebrew_word = input("Enter a Hebrew word: ")
print("Transliteration: ", transliterate(hebrew_word))
