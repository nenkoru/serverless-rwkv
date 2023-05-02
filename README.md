# Serverless-RWKV
Serverless-RWKV is a repository containing all the needs to deploy a very basic inference API to serverless GPU providers such as Runpod.io
Having this you can go further and deploy any different kinds of a code around RWKV and serverless inference in particular.
## Motivation
I understand how hard it could be to host a huge 3090 or 4090 to run LLMs, not considering the cost of a GPU itself. I really wish everything to be mobile as possible. I do have a powerful laptop that could handle RWKV, but with the pace that I would like to use the model it would drain the battery real fast. So after that I started to think what could be done to run a model somewhere in cloud, but as cheap as possible. Renting a machine is GPU is quite costly. Very costly. And I won't be using all the horsepower all the second that I am paying for. So afterwards a serverless computation goes into a play. Deploy effortlessly, run efficiently. Now I can pay exactly for what I use.

## Building image
Deploy to a selected provider of yours by navigating to it and finding a Dockerfile for it.
Typical build and push to Dockerhub for Dockerfile:
```bash
$ pwd
> ./runpod-rwkv/runpod/cpp-cuda
$ sudo docker build --build-arg MODEL_URL=https://huggingface.co/nenkoru/rwkv-cuda-cpp/resolve/main/v11/model-4-Raven-7
B-v11-Eng99%25-Other1%25-20230427-ctx8192.bin -t ractyfree/runpod-rwkv:cpp-cuda-v11-7b -f Dockerfile.cpp_cuda .
$ sudo docker push ractyfree/runpod-rwkv:cpp-cuda-v11-7b
```
This would use a converted 7B model that is located in my huggingface repository, as long as we are building with [rwkv-cpp-cuda](https://github.com/harrisonvanderbyl/rwkv-cpp-cuda).
And push it to the Dockerhub repository that you have to create beforehand.
Note: I strongly recommend to opt for cpp-cuda version, as long as it's much more optimized in terms of loading time and inference(Q8_0).

## Deploying to a provider(Runpod)
In runpod.io you have to create an 'API Template' and in 'Container image' field you have to put a name like this:`ractyfree/runpod-rwkv:cpp-cuda-v11-7b`
And then in 'My APIs' create a new api with selecting a newly created template to be used as well as GPU suitable for the size of a model that you are willing to deploy.

## Contribution
All the contributions are welcome. You would like to add a Google-like documentation into serverless_handler.py - go ahead and push a PR.
You have a doubt that there is an inefficiency in a way Dockerfile is built - you know what to do.
`This is the way.`

## Roadmap:
- Integration with beam.cloud, banana.dev, replicate, pipeline.ai
- Automatic rebuilds on push to Dockerhub with all the base models 1b5, 3b, 7b, 14b
