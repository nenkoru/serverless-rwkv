import time
import os

import runpod

from typing import List, Callable

import binding

MODEL_PATH = os.environ.get("MODEL_PATH", "model.bin")
TOKENIZER_VOCAB_PATH = os.environ.get("TOKENIZER_VOCAB_PATH", "vocab.json")
TOKENIZER_MERGES_PATH = os.environ.get("TOKENIZER_MERGES_PATH", "merges.txt")

print(f"Loading {MODEL_PATH}...", end='')
t1 = time.time()
model = binding.ModelWrapper(model_path=MODEL_PATH)
print(f" Loaded in {time.time() - t1}!")

print(f"Loading tokenizer...", end='')
t1 = time.time()
tokenizer = binding.TokenizerWrapper(
        vocab_path=TOKENIZER_VOCAB_PATH,
        merges_path=TOKENIZER_MERGES_PATH,
        )
print(f" Loaded in {time.time() - t1}!")


def generate_tokens(
    *, 
    model: binding.ModelWrapper,
    input_tokens: List[int],
    tokens_to_generate: int,
    ):
    
    model.init_state()
    model.load_context(input_tokens)
    last_token = input_tokens[-1]
    for _ in range(tokens_to_generate):
        model.forward(last_token)
        last_token = model.sample()
        yield last_token
 

def handler(event):
    print(event)
    return "Hello World"

runpod.serverless.start({
    "handler": handler
})

