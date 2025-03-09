import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline
import onnxruntime as ort
import random

# 1️⃣ Wczytanie modelu do klasyfikacji poprawności seedów BIP39
MODEL_NAME = "distilbert-base-uncased"

device = "cuda" if torch.cuda.is_available() else "cpu"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME).to(device)

def classify_seed(seed_phrase):
    """Klasyfikuje seed BIP39 jako poprawny lub błędny."""
    inputs = tokenizer(seed_phrase, return_tensors="pt").to(device)
    outputs = model(**inputs)
    logits = outputs.logits
    prediction = torch.argmax(logits, dim=1).item()
    return "Poprawny" if prediction == 1 else "Błędny"

# 2️⃣ Generacja brakujących słów BIP39 (GPT-2)
from transformers import AutoModelForCausalLM

GEN_MODEL = "gpt2"
gen_model = AutoModelForCausalLM.from_pretrained(GEN_MODEL).to(device)
gen_tokenizer = AutoTokenizer.from_pretrained(GEN_MODEL)

def generate_missing_words(seed_fragment):
    """Generuje brakujące słowa w seedzie."""
    inputs = gen_tokenizer(seed_fragment, return_tensors="pt").to(device)
    outputs = gen_model.generate(**inputs, max_length=40, num_return_sequences=1)
    return gen_tokenizer.decode(outputs[0], skip_special_tokens=True)

# 3️⃣ Autokorekta seedów BIP39 (Mistral 7B / LLaMA 2 7B)
correction_pipeline = pipeline("text2text-generation", model="mistralai/Mistral-7B-v0.1", device=0)

def correct_seed(seed_phrase):
    """Koryguje literówki i błędy w seedzie BIP39."""
    correction = correction_pipeline(f"Popraw błędy w: {seed_phrase}", max_length=40)
    return correction[0]['generated_text']

# 4️⃣ Testowanie wygenerowanych seedów w Electrum (opcjonalnie)
import subprocess

def test_seed_in_electrum(seed):
    """Sprawdza, czy seed generuje poprawny portfel w Electrum."""
    command = f"electrum -w /tmp/test_wallet restore '{seed}'"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return "Success" if "Restored" in result.stdout else "Failed"

# 5️⃣ Przykładowe użycie
sample_seed = "abandon ability able about absent ..."
print("✅ Klasyfikacja:", classify_seed(sample_seed))
print("🔄 Generacja brakujących słów:", generate_missing_words("abandon ability ..."))
print("🔧 Autokorekta:", correct_seed("abandn abillity abl abut absnt ..."))

# Testowanie seedów w Electrum
# print("⚡ Test w Electrum:", test_seed_in_electrum(sample_seed))

