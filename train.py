import json
import numpy as np
import pickle
from tensorflow.keras.layers import Dense, Input, LSTM
from tensorflow.keras.models import Model


def preprocess_data(data):
    input_words = []
    target_words = []
    input_characters = set()
    target_characters = set()

    # Build list of words and set of characters
    for word, transliteration in data.items():
        input_words.append(word)
        target_word = '\t' + transliteration + '\n'
        target_words.append(target_word)

        # Update character sets
        input_characters |= set(word)
        target_characters |= set(target_word)

    return input_words, target_words, sorted(list(input_characters)), sorted(list(target_characters))


def build_one_hot_arrays(input_words, target_words, input_token_index, target_token_index, max_encoder_seq_length, max_decoder_seq_length, num_encoder_tokens, num_decoder_tokens):
    # Initialize 3D arrays for input data
    encoder_input_data = np.zeros(
        (len(input_words), max_encoder_seq_length, num_encoder_tokens), dtype='float32')
    decoder_input_data = np.zeros(
        (len(input_words), max_decoder_seq_length, num_decoder_tokens), dtype='float32')
    decoder_target_data = np.zeros(
        (len(input_words), max_decoder_seq_length, num_decoder_tokens), dtype='float32')

    # Fill in data
    for i, (input_word, target_word) in enumerate(zip(input_words, target_words)):
        for t, char in enumerate(input_word):
            encoder_input_data[i, t, input_token_index[char]] = 1.
        encoder_input_data[i, t + 1:, input_token_index[' ']] = 1.
        for t, char in enumerate(target_word):
            decoder_input_data[i, t, target_token_index[char]] = 1.
            if t > 0:
                decoder_target_data[i, t - 1, target_token_index[char]] = 1.
        decoder_input_data[i, t + 1:, target_token_index[' ']] = 1.
        decoder_target_data[i, t:, target_token_index[' ']] = 1.

    return encoder_input_data, decoder_input_data, decoder_target_data


# Load data
with open('data.json', 'r') as f:
    data = json.load(f)

input_words, target_words, input_characters, target_characters = preprocess_data(
    data)

num_encoder_tokens = len(input_characters)
num_decoder_tokens = len(target_characters)

max_encoder_seq_length = max([len(txt) for txt in input_words])
max_decoder_seq_length = max([len(txt) for txt in target_words])

input_token_index = {char: i for i, char in enumerate(input_characters)}
target_token_index = {char: i for i, char in enumerate(target_characters)}

encoder_input_data, decoder_input_data, decoder_target_data = build_one_hot_arrays(
    input_words, target_words, input_token_index, target_token_index, max_encoder_seq_length, max_decoder_seq_length, num_encoder_tokens, num_decoder_tokens)

# Save the character dictionaries and sequence lengths for later use
with open('char_indices.pkl', 'wb') as f:
    pickle.dump((input_token_index, target_token_index), f)
with open('sequence_lengths.pkl', 'wb') as f:
    pickle.dump((max_encoder_seq_length, max_decoder_seq_length), f)

# Define the model
encoder_inputs = Input(shape=(None, num_encoder_tokens))
encoder = LSTM(256, return_state=True)
encoder_outputs, state_h, state_c = encoder(encoder_inputs)

decoder_inputs = Input(shape=(None, num_decoder_tokens))
decoder_lstm = LSTM(256, return_sequences=True, return_state=True)
decoder_outputs, _, _ = decoder_lstm(
    decoder_inputs, initial_state=[state_h, state_c])
decoder_dense = Dense(num_decoder_tokens, activation='softmax')
decoder_outputs = decoder_dense(decoder_outputs)

model = Model([encoder_inputs, decoder_inputs], decoder_outputs)

# Compile and train the model
model.compile(optimizer='rmsprop', loss='categorical_crossentropy')
model.fit([encoder_input_data, decoder_input_data],
          decoder_target_data, batch_size=64, epochs=50, validation_split=0.2)

# Save the encoder and decoder models for later use
encoder_model = Model(encoder_inputs, [state_h, state_c])
encoder_model.save('encoder_model.h5')

# These inputs will receive the states of the previous time step
decoder_state_inputs = [Input(shape=(256,)), Input(shape=(256,))]
decoder_outputs, state_h, state_c = decoder_lstm(
    decoder_inputs, initial_state=decoder_state_inputs)
decoder_outputs = decoder_dense(decoder_outputs)

decoder_model = Model([decoder_inputs] + decoder_state_inputs,
                      [decoder_outputs, state_h, state_c])
decoder_model.save('decoder_model.h5')
