wget $MODEL_URL -O model.pth
wget $TOKENIER_URL -O tokenizer.json

docker build -t runpod-rwkv:${MODEL_VERSION} .
