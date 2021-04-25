from fastapi import FastAPI
from pydantic import BaseModel
from predicting import process_file, make_files


class UpFile(BaseModel):
    file: bytes


class Predictions(BaseModel):
    answers: dict
    corrects: bytes
    incorrects: bytes

app = FastAPI()


@app.post('/predict', response_model=Predictions)
def make_prediction(file: UpFile):
    answers = process_file(file.file)
    corrects, incorrects = make_files(file.file, answers)
    return Predictions(answers=answers, corrects=corrects, incorrects=incorrects)
