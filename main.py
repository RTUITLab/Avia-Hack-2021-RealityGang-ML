from fastapi import FastAPI, File
from pydantic import BaseModel
from predicting import process_file



class UpFile(BaseModel):
    file: bytes


class Predictions(BaseModel):
    answers: dict

app = FastAPI()


@app.post('/predict', response_model=Predictions)
async def make_prediction(file: bytes=UpFile):
    answers = process_file(file.file)
    return Predictions(answers=answers)
