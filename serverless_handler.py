import runpod
import os

from rwkv.model import RWKV
from rwkv.utils import PIPELINE, PIPELINE_ARGS

STRATEGY = os.environ.get("STRATEGY", "cuda fp16")

model = RWKV(model="model.pth", strategy=STRATEGY)
pipeline = PIPELINE(model, "tokenizer.json")

def evaluate(
    prompt,
    token_count=200,
    temperature=1.0,
    top_p=0.7,
    presencePenalty = 0.1,
    countPenalty = 0.1,
    token_stop = [0],
    token_ban = [],
    ctx_limit=4096,
):
    args = PIPELINE_ARGS(
            temperature = max(0.2, float(temperature)), 
            top_p = float(top_p),
            alpha_frequency = countPenalty,
            alpha_presence = presencePenalty,
            token_ban=token_ban,
            token_stop=token_stop,
            )

    all_tokens = []
    occurrence = {}
    state = None
    for i in range(int(token_count)):
        out, state = model.forward(
                pipeline.encode(prompt)[-ctx_limit:] if i == 0 else [token],
                state
                )

        for n in occurrence:
            out[n] -= (args.alpha_presence + occurrence[n] * args.alpha_frequency)

        token = pipeline.sample_logits(
                out, 
                temperature=args.temperature, 
                top_p=args.top_p
                )

        if token in args.token_stop:
            break

        all_tokens += [token]

        if token not in occurrence:
            occurrence[token] = 1
        else:
            occurrence[token] += 1
        
    return pipeline.decode(all_tokens)

def handler(event):
    print(event)
    return "Hello World"


runpod.serverless.start({
    "handler": handler
})
