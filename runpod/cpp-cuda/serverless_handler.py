import runpod
import os

def handler(event):
    print(event)
    return "Hello World"


runpod.serverless.start({
    "handler": handler
})
