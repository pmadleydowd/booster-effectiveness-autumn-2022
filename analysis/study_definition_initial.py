# Import codelists from codelists.py
import codelists

# import json module
import json

#study_parameters
with open("./lib/design/study-dates.json") as f:
  study_dates = json.load(f)

from cohortextractor import (
  StudyDefinition,
  patients,
  codelist_from_csv,
  codelist,
  filter_codes_by_category,
  combine_codelists,
  params
)

############################################################
## inclusion variables
from variables_vax import generate_vax_variables 
vax_variables = generate_vax_variables(index_date="1900-01-01")
############################################################
# vax variables
from variables_inclusion import generate_inclusion_variables 
inclusion_variables = generate_inclusion_variables(index_date=study_dates["studystart"])
############################################################

# Specify study definition
study = StudyDefinition(
  
  # Configure the expectations framework
  default_expectations={
    "date": {"earliest": "2020-01-01", "latest": "today"},
    "rate": "uniform",
    "incidence": 0.2,
    "int": {"distribution": "normal", "mean": 1000, "stddev": 100},
    "float": {"distribution": "normal", "mean": 25, "stddev": 5},
  },
  
  # This line defines the study population
  population=patients.satisfying(
    """
    registered
    AND
    age >= 50
    AND
    NOT has_died
    # AND 
    # covid_vax_disease_2_date
    """,
    
    **inclusion_variables,    

  ),
  
  age=patients.age_as_of( 
    study_dates["boosterautumn2022"]["ages50to64"],
    ),
  
  #################################################################
  ## Covid vaccine dates
  #################################################################
  **vax_variables,        
  
)