import json
from sklearn.model_selection import train_test_split
from datasets import Dataset
from transformers import T5Tokenizer, T5ForConditionalGeneration
from transformers import DataCollatorForSeq2Seq, Seq2SeqTrainingArguments, Seq2SeqTrainer

# Load data
with open("data.json", "r") as f:
    data = json.load(f)

# Generate pairs
pairs = [(hebrew, translit) for hebrew, translit in data.items()]

# Split the data
train_pairs, val_pairs = train_test_split(pairs, test_size=0.1)

# Load tokenizer and model
tokenizer = T5Tokenizer.from_pretrained("t5-small")
model = T5ForConditionalGeneration.from_pretrained("t5-small")

# Tokenize the data and convert to Dataset
def tokenize(pair):
    src, tgt = pair
    src_tokenized = tokenizer(src, return_tensors="pt", padding="max_length", truncation=True, max_length=128)
    tgt_tokenized = tokenizer(tgt, return_tensors="pt", padding="max_length", truncation=True, max_length=128)
    return {k: v.squeeze(0) for k, v in src_tokenized.items()}, {k: v.squeeze(0) for k, v in tgt_tokenized.items()}

train_data = [tokenize(pair) for pair in train_pairs]
val_data = [tokenize(pair) for pair in val_pairs]

train_dataset = Dataset.from_dict({
    "input_ids": [item[0]["input_ids"] for item in train_data],
    "attention_mask": [item[0]["attention_mask"] for item in train_data],
    "labels": [item[1]["input_ids"] for item in train_data],
})
val_dataset = Dataset.from_dict({
    "input_ids": [item[0]["input_ids"] for item in val_data],
    "attention_mask": [item[0]["attention_mask"] for item in val_data],
    "labels": [item[1]["input_ids"] for item in val_data],
})

# Training arguments
training_args = Seq2SeqTrainingArguments(
    output_dir="output",
    num_train_epochs=5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    logging_dir="logs",
    logging_strategy="steps",
    logging_steps=50,
    evaluation_strategy="steps",
    eval_steps=100,
    save_strategy="steps",
    save_steps=100,
    save_total_limit=2,
)

# Define data collator
data_collator = DataCollatorForSeq2Seq(tokenizer, model=model)

# Create trainer
trainer = Seq2SeqTrainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    data_collator=data_collator,
    tokenizer=tokenizer,
)

# Train the model
trainer.train()

# Save the model
model.save_pretrained("trained_model")