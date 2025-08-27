from fastapi import FastAPI, Path, HTTPException, Query
import json


app = FastAPI()



def load_data():
    with open('patients.json','r') as f:
        data = json.load(f)
    return data 


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












