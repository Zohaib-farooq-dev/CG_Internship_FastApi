from fastapi import FastAPI
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

















