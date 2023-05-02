# Serverless-RWKV
Serverless-RWKV is a repository containing all the needs to deploy a very basic inference API to serverless GPU providers such as Runpod.io
Having this you can go further and deploy any different kinds of a code around RWKV and serverless inference in particular.

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

## Deploying to a provider(Runpod)
In runpod.io you have to create an 'API Template' and in 'Container image' field you have to put a name like this:`ractyfree/runpod-rwkv:cpp-cuda-v11-7b`
And then in 'My APIs' create a new api with selecting a newly created template to be used as well as GPU suitable for the size of a model that you are willing to deploy.
