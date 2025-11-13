#computed fields vo fields hote hai jinki value hum dusre fields se nikalte hai

from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator, model_validator, computed_field
from typing import List, Dict, Optional, Annotated

class Patient(BaseModel):
    
    name : str
    email : EmailStr
    age : int
    weight: float
    married: bool
    allergies :List[str]
    contact_details: Dict[str,str]
    
    @computed_field
    @property
    def calculate_bmi(self) -> float:
        bmi = round(self.weight/self.height**2)
        return bmi
    
def update_patient_data(patient:Patient):
    print(patient.name)
    print(patient.calculate_bmi)
patient_info = {'name':'Anushka', 'age':22,'email':'ranjananushka90@gmail.com',  'weight':53.7,'height': 1.72, 'married': True,'allergies':['pollen','dust'],'contact':{'phone':'930272340'}} 

patient1 = Patient(**patient_info)

update_patient_data(patient1)
    