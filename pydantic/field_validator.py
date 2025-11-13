from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator, model_validator
from typing import List, Dict, Optional, Annotated

class Patient(BaseModel):
    
    name : str
    email : EmailStr
    age : int
    weight: float
    married: bool
    allergies :List[str]
    contact_details: Dict[str,str]
    
    @model_validator(mode = 'after')
    def validate_emergency_contact(cls,model): #ek single value ki jagha pura model le rahe hai jsmai saare fields hai apne
        if model.age>60 and 'emergency' not in model.contact_details:
            raise ValueError('Patients older than 60 must have an emergency ciontact')
    
    @field_validator('email') #creating a field validator along with a decorator
    @classmethod
    def email_validator(cls, value):
        valid_domains = ['hdfc.com', 'icici.com']
        domain_name = value.split('@')[-1]
        if domain_name not in valid_domains:
            raise ValueError('Not a valid domain')
        return value
    
    @field_validator('name')
    @classmethod
    def transform_name(cls, value):
        return value.upper() #name in capital
    
    @field_validator('age', mode = 'after')
    @classmethod
    def validate_age(cls,value): #mode mai after lagane se hoga yeh ki yeh jo age ki value hai vo str of 30 ki jagha int of 30 milegi, ie type coversion k baad ki.
        if 0 < value< 100:
            return value
        else:
            raise ValueError('Age should be between 0 and 100')
    
    
def update_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print("Inserted")
    
patient_info = {'name':'Anushka', 'age':22,'email':'ranjananushka90@gmail.com',  'weight':53.7,'married': True,'allergies':['pollen','dust'],'contact':{'phone':'930272340'}} 
patient1 = Patient(**patient_info)

