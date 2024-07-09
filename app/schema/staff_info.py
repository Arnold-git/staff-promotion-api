from typing import Optional, Union
from pydantic import BaseModel
import numpy as np

class StaffInfo(BaseModel):
    EmployeeNo: Optional[str] = "YAK/S/00011"
    Division: Optional[str] = "'Information Technology and Solution Support'"
    Qualification: Optional[str] = "nan"
    Gender: Optional[str] = "Male"
    Channel_of_Recruitment: Optional[str] = 'Direct Internal process'
    Trainings_Attended: Optional[int] = 2
    Year_of_birth: Optional[int] = 1991
    Last_performance_score: Optional[float] = 0.0
    Year_of_recruitment: Optional[int] = 2018
    Targets_met: Optional[int] = 0
    Previous_Award: Optional[int] = 0
    Training_score_average: Optional[int] = 69
    State_Of_Origin: Optional[str] = "OGUN"
    Foreign_schooled: Optional[str] = "Yes"
    Marital_Status: Optional[str] = "Married"
    Past_Disciplinary_Action: Optional[str] = "No"
    Previous_IntraDepartmental_Movement: Optional[str] = "No"
    No_of_previous_employers: Optional[str] = "1"