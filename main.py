from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
import json
from pydantic import BaseModel, Field, computed_field
from typing import Annotated,Literal, Optional

app = FastAPI()

#using pydantic to validate the request body and adding meta data
class Patient(BaseModel):
    
    id:Annotated[str,Field(...,description='ID of the patient')]
    name: Annotated[str, Field(...,description='Name of the Patient')]
    city: Annotated[str, Field(...,description='City of the Patient')]
    age: Annotated[int, Field(...,description='Age of the Patient',gt=0,lt=120)]
    gender: Annotated[Literal['male','female','others'], Field(...,description='Gender of the Patient')]
    height: Annotated[float, Field(...,description='Height of the Patient', gt=0)]
    weitght: Annotated[float, Field(...,description='Weight of the Patient',gt=0)]
    
    #calculating bmi
    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/(self.height**2),2)
        return bmi
    
    #displaying verdict based on calculated bmi
    @computed_field
    @property
    def verdict(self)-> str:
        if self.bmi<18.5:
            return 'Underweight'
        elif self.bmi < 25:
            return 'Normal'
        elif self.bmi < 30:
            return 'Nmormal'
        else:
            return 'Obsese'
# To perform update operation we have to create a new pydantic model because in previous one all the fields are set to cumpulsory. If the fields are mandatory then we won't be able to edit/change anything.

class PatientUpdate(BaseModel):
      
    name: Annotated[Optional[str],Field(default=None)]
    city: Annotated[Optional[str],Field(default=None)]
    age: Annotated[Optional[int],Field(default=None)]
    gender: Annotated[Optional[Literal['male','female']],Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field (default=None, gt=0)]   

def load_data():
    with open('patients.json','r') as f:
        data = json.load(f)
        
        return data
def save_data(data):
    with open('patient.json', 'w') as f:
        json.dump(data, f)
        
        
#we have to define a route with the help of a decorator for our app, koi bhi man lo angel.in/ krega toh vo iss api ko hit krega
@app.get("/")
#create a method for this endpoint
def hello():
    return {'message': 'Patient Management System API!'}

@app.get('/about')
def about():
    return{'message': 'A fully functional API to manage your patient records'}

#endpoint1
@app.get('/view')
def view():
    data = load_data()
    return data

@app.get('/patient/{patient_id}') #path param
def view_patient(patient_id: str = Path(...,description = 'ID of the paitent in the DB, Example=P001')):
    #load all the patients
    data = load_data()
    
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail='Patient Not Found')

@app.get('/sort')
def sort_patients(sort_by: str = Query(..., description='sort on the basis of height,weight or bmi'),order: str= Query('asc',description = 'sort in asc or dsc')):
    
    valid_fields = ['height','weight','bmi']
    
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail='Invalid field, select from valid fields')
    if order not in ['asc','desc']:
        raise HTTPException(status_code=400, detail='Invalid field, select between asc and desc')
    data = load_data()
    sort_order = True if order =='desc' else False
    sorted_data = sorted(data.values(), key = lambda x:x.get('sort_by',0), reverse= sort_order)
    
    return sorted_data

#makinf create endpoint
@app.post('/create')
def create_patient(patient: Patient): #whatever data we are receving from client we are passing it directly to the basemodel
    #load existing data
    data =load_data()
    
    #check if patient is already there in db, if yes then raise error
    if patient.id in data:
        raise HTTPException(status_code=400, detail='Patient already exists')
    
    #if new then add new patient to the db
    data[patient.id]= patient.model_dump(exclude=['id'])
    
    #save in json file
    save_data(data)
    return JSONResponse(status_code=201, content={'message':'patient created successfully'})

@app.put('/edit/{patient_id}')
def update_patient(patient_id: str, patient_update: PatientUpdate):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404,detail = 'Patient not found')
    #patient ka existing info ek dict mai hai(all fields)
    existing_patient_info = data[patient_id]
    #patient ka updated info ek dict mai hai(updated fileds)
    updated_patient_info = patient_update.model_dump(exclude_unset = True)
    
    #loop chala rahe hai updated wale pe but changes kar rahe hai existing wale pe
    for key, value in updated_patient_info.items():
        existing_patient_info[key] = value
        
    #existing_patient_info -> pydantic object-> updated bmi + verdict
    existing_patient_info['id'] = patient_id
    patient_pydantic_obj = Patient(**existing_patient_info)
    # -> pydantic obj -> dict
    existing_patient_info= patient_pydantic_obj.model_dump(exclude='id')
    
    #add this dictionary to data
    data[patient_id] = existing_patient_info    
    #save data
    save_data(data)
    
    return JSONResponse(status_code=200, content={'message':'patient updated'})

@app.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):
    #load data
    data = load_data()
    
    if patient_id not in data:
        raise HTTPException(status_code=404,detail='Patient not found')
    del data[patient_id]
    
    save_data(data)
    
    return JSONResponse(status_code=200,content={'message':'patient deleted'})
    