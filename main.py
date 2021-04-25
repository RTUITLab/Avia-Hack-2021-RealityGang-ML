from fastapi import FastAPI
from pydantic import BaseModel
from predicting import process_file, make_files


class File(BaseModel):
    '''
    file: bytes. Input file in base64 format.
    '''
    file: bytes


class Predictions(BaseModel):
    '''
    answers: dict. Dictionary {"track_id": label}, where label is 0 or 1.
    
    corrects: bytes. Output file in base64 format. Contains correct tracks from input file.
    
    incorrects: bytes. Output file in base64 format. Contains correct tracks from output file.
    '''
    answers: dict
    corrects: bytes
    incorrects: bytes


app = FastAPI()


@app.post('/predict', response_model=Predictions)
def make_prediction(file: File):
    '''
    Make prediction for input file.
    Args:

        file: File schema. Input file.
    Returns:

        Object of Prediction schema.
    '''

    answers = process_file(file.file)
    corrects, incorrects = make_files(file.file, answers)
    return Predictions(answers=answers, corrects=corrects, incorrects=incorrects)
