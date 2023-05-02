import runpod


runpod.api_key = "<API_KEY>"
endpoint = runpod.Endpoint("f04pvrewtkujxb")
t1 = time.time()
run_request = endpoint.run({
    "body": "Bob: How to create a systemd unit file and enable it?\n\nAlice:", 
    "tokens": 500, 
    "with_body": True, 
    "stop_sequence": "Bob:"
    })

# Check the status of the endpoint run request
print(run_request.status())

# Get the output of the endpoint run request, blocking until the endpoint run is complete.
print(run_request.output())
print(time.time() - t1)
