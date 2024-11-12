from fastapi import FastAPI, HTTPException
import pickle
import numpy as np
import uvicorn

from Routers import predict







# Initialize FastAPI app
app = FastAPI()

# Define a root endpoint
@app.get("/")
def read_root():
    return {"message": "Model for Cirrhosis patient predictions"}

app.include_router(predict.router)

# Run the server
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)




