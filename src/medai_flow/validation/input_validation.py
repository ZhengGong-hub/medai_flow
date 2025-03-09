"""Input validation functions for medai_flow."""

def validate_patient_profile(inputs: dict) -> None:
    """Validate patient profile input.
    
    Args:
        inputs: Dictionary containing input data
        
    Raises:
        ValueError: If patient_profile is missing, empty, or invalid
    """
    if not inputs or "patient_profile" not in inputs:
        raise ValueError("patient_profile is required")
    
    patient_profile = inputs["patient_profile"]
    if not patient_profile or not isinstance(patient_profile, str):
        raise ValueError("patient_profile must be a non-empty string")
    
    if patient_profile.strip() == "":
        raise ValueError("patient_profile cannot be empty or only whitespace")

def validate_diagnosis(inputs: dict) -> None:
    """Validate diagnosis input.
    
    Args:
        inputs: Dictionary containing input data
        
    Raises:
        ValueError: If diagnosis is missing, empty, or invalid
    """
    if not inputs or "diagnosis" not in inputs:
        raise ValueError("diagnosis is required")
    
    diagnosis = inputs["diagnosis"]
    if not diagnosis or not isinstance(diagnosis, str):
        raise ValueError("diagnosis must be a non-empty string")
    
    if diagnosis.strip() == "":
        raise ValueError("diagnosis cannot be empty or only whitespace")

def validate_supplements_recommendation(inputs: dict) -> None:
    """Validate supplements recommendation input.
    
    Args:
        inputs: Dictionary containing input data
        
    Raises:
        ValueError: If supplements_recommendation is missing, empty, or invalid
    """
    if not inputs or "supplements_recommendation" not in inputs:
        raise ValueError("supplements_recommendation is required")
    
    supplements = inputs["supplements_recommendation"]
    if not supplements or not isinstance(supplements, str):
        raise ValueError("supplements_recommendation must be a non-empty string")
    
    if supplements.strip() == "":
        raise ValueError("supplements_recommendation cannot be empty or only whitespace")

def validate_exercise_recommendation(inputs: dict) -> None:
    """Validate exercise recommendation input.
    
    Args:
        inputs: Dictionary containing input data
        
    Raises:
        ValueError: If exercise_recommendation is missing, empty, or invalid
    """
    if not inputs or "exercise_recommendation" not in inputs:
        raise ValueError("exercise_recommendation is required")
    
    exercise = inputs["exercise_recommendation"]
    if not exercise or not isinstance(exercise, str):
        raise ValueError("exercise_recommendation must be a non-empty string")
    
    if exercise.strip() == "":
        raise ValueError("exercise_recommendation cannot be empty or only whitespace") 

def validate_output_file_format(inputs: dict) -> None:
    """Validate output file format input.
    
    Args:
        inputs: Dictionary containing input data
        
    Raises:
        ValueError: If output_file_format is missing, empty, or invalid
    """
    if not inputs or "output_file_format" not in inputs:
        raise ValueError("output_file_format is required")
    
    output_file_format = inputs["output_file_format"]
    if not output_file_format or not isinstance(output_file_format, str):
        raise ValueError("output_file_format must be a non-empty string")
    
    if output_file_format.strip() == "":
        raise ValueError("output_file_format cannot be empty or only whitespace")