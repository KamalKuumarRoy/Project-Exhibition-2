from contextlib import asynccontextmanager
from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from constants import SERVER_URL, PORT, ENV

from fastapi import APIRouter
import base64
from io import BytesIO
from apps.calculator.utils import analyze_image
from schema import ImageData
from PIL import Image

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app= FastAPI(lifespan=lifespan) 

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def health():
    return {'message': 'Server is running'}

@app.post('/calculate')
async def run(data: ImageData):
    image_data = base64.b64decode(data.image.split(",")[1])  # Assumes data:image/png;base64,<data>
    image_bytes = BytesIO(image_data)
    image = Image.open(image_bytes)
    responses = analyze_image(image, dict_of_vars=data.dict_of_vars)
    data = []
    for response in responses:
        data.append(response)
    print('response in route: ', response)
    return {"message": "Image processed", "data": data, "status": "success"}

if __name__=='__main__':
    uvicorn.run("main:app", host=SERVER_URL, port=int(PORT), reload=(ENV == "dev"))    