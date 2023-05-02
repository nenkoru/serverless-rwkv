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

    reverse_sequence_window = len(req_body.stop_sequence) * -1 if req_body.stop_sequence else 0
    output_str = req_body.body if req_body.with_body else ""

    for token in generator_tokens:
        decoded_token = TOKENIZER.decode(token)
        
        output_str += decoded_token
        if req_body.stop_sequence && output_str[reverse_sequence_window:] == req_body.stop_sequence:
            break

    return output_str

runpod.serverless.start({
    "handler": handler
})

