from pydantic import BaseModel
from typing import List,Dict, Optional,EmailStr, Field, Annotated

#this is our pydantic model with a well defined schema
class Patient(BaseModel):
    name:Annotated[str,Field(max_length= 50, title = 'Name of the Patient', description='Given name of the patient in less than 50 characters')]
    age: int
    email: EmailStr
    weight: float = Field(gt=0)
    married: bool
    allergies: Optional[List[str]] = None
    contact: Dict[str,str]

def insert_patient_data(patient:Patient):
    print(patient.name)
    print(patient.age)
    print("Inserted")
#make an object for the above model
#firstly creating a dictionary
patient_info = {'name':'Anushka', 'age':22,'email':'ranjananushka90@gmail.com',  'weight':53.7,'married': True,'allergies':['pollen','dust'],'contact':{'phone':'930272340'}} 
#unpacking the dictionary and making our object
patient1 = Patient(**patient_info)

insert_patient_data(patient1)