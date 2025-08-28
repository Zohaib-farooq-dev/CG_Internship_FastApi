from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field,computed_field
from typing import Annotated,Literal,Optional
import json


app = FastAPI()

class Patient(BaseModel):
    id: Annotated[str,Field(...,description='Id of the patient',example='P001')]
    name:Annotated[str,Field(...,description='Name of the patient')]
    city:Annotated[str,Field(...,description='City where the patient is living')]
    age:Annotated[int,Field(...,gt=0,lt=120,description='Age of the patient')]
    gender:Annotated[Literal['male','female','other'],Field(...,description='Gender of teh patient')]
    height:Annotated[float,Field(...,description='Heightof teh patient in meters')]
    weight:Annotated[float,Field(...,description='Weight of  the patient in Kgs')]

    @computed_field
    @property
    def bmi(self)->float:
        bmi = round(self.weight/(self.height**2),2)
        return bmi
    
    @computed_field
    @property
    def verdict(self)->str:
        if self.bmi<18.5:
            return 'Underweight'
        elif self.bmi<28:
            return 'Normal'
        else:
            return 'Obese'

class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0)]
    gender: Annotated[Optional[Literal['male', 'female']], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]


def load_data():
    with open('patients.json','r') as f:
        data = json.load(f)
    return data 

def save_data(data):
    with open('patients.json','w') as f:
        json.dump(data,f)
    


@app.get("/")
def hello():
    return {"message":"Patient Mnagement System API"}

@app.get("/about")
def about():
    return {"message":"Fully functional API for mangaging your patients"}

@app.get("/view")
def view():
    data = load_data()
    return data 


@app.get("/patient/{patient_id}")
def view_patient(patient_id:str = Path(...,description='ID of the patient in DB',example='P001')):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail='Patient not Found!')

@app.get('/sort')
def sorted_patients(sort_by:str = Query('weight', description='Sort on the basis of wirght ,hight and bmi'), order:str= Query('asc',description="Sosrt values in ascending or descending order")):
    valid_fields =['height','weight','bmi']
    if sort_by not in valid_fields:
        raise HTTPException(status_code='400',detail=f'Invalid fields select from {valid_fields}')
    if order not in ['asc','desc']:
        raise HTTPException(status_code='400',detail='Invalid order select asc or desc')
    
    data = load_data()
    sort_order = True if order =='desc' else False
    sort = sorted(data.values(),key= lambda x:x.get(sort_by,0),reverse=sort_order)
    return sort

@app.post('/create')
def create_patient(patient:Patient):

    data = load_data()

    if patient.id in data:
        raise HTTPException(status_code=400,detail='Patient already exists in database')
    
    data[patient.id] = patient.model_dump(exclude=['id'])
    save_data(data)
    return JSONResponse(status_code=201, content='Patient created succesfully')

@app.put('/edit/{patient_id}')
def update_patient(patient_id : str, patient:PatientUpdate):
    
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient Not Found!')
    
    existing_patient = data[patient_id]
    updated_patient = patient.model_dump(exclude_unset=True)
    for key,values in updated_patient.items():
        existing_patient[key] = values
    
    existing_patient['id']= patient_id
    updated = Patient(**existing_patient)
    existing_patient = updated.model_dump(exclude='id')
    data[patient_id]= existing_patient

    save_data(data)
    return JSONResponse(status_code=200,content={'mesage':'Patient Updated'})


@app.delete('/delete/{patient_id}')
def patient_delete(patient_id:str):

    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404,detail='Patient doesnt exist')
    
    del data[patient_id]
    save_data(data)
    return JSONResponse(status_code=200,content={'message':'Patient deleted'})









