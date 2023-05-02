import time
import os

import runpod

from typing import List, Callable
from dataclasses import dataclass

import binding

MODEL_PATH = os.environ.get("MODEL_PATH", "model.bin")
TOKENIZER_VOCAB_PATH = os.environ.get("TOKENIZER_VOCAB_PATH", "vocab.json")
TOKENIZER_MERGES_PATH = os.environ.get("TOKENIZER_MERGES_PATH", "merges.txt")

print(f"Loading {MODEL_PATH}...", end='')
t1 = time.time()
MODEL = binding.ModelWrapper(model_path=MODEL_PATH)
print(f" Loaded in {time.time() - t1}!")

print(f"Loading tokenizer...", end='')
t1 = time.time()
TOKENIZER = binding.TokenizerWrapper(
        vocab_path=TOKENIZER_VOCAB_PATH,
        merges_path=TOKENIZER_MERGES_PATH,
        )
print(f" Loaded in {time.time() - t1}!")


@dataclass
class RequestBodyMessage:
    body: str
    tokens: int
    with_body: bool = False
    stop_sequence: str = None

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
    req_body = RequestBodyMessage(**event['input'])
    input_tokens = TOKENIZER.encode(req_body.body)
    generator_tokens = generate_tokens(
            model=MODEL, 
            input_tokens=input_tokens, 
            tokens_to_generate=req_body.tokens
            )
    return "".join(TOKENIZER.decode(token) for token in generator_tokens)

runpod.serverless.start({
    "handler": handler
})

