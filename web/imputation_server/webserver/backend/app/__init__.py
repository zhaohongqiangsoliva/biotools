from app import rpc_middleware

...

app.middleware('http')(rpc_middleware)

...
