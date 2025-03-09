import pytest
import os
from medai_flow.crews.writer_crew.writer_crew import WriterCrew

def test_writer_crew_initialization():
    """Test that WriterCrew can be initialized"""
    crew = WriterCrew()
    assert crew is not None

def test_writer_crew_creation():
    """Test that WriterCrew can create a crew"""
    crew = WriterCrew().crew()
    assert crew is not None
    assert len(crew.agents) > 0
    assert len(crew.tasks) > 0

def test_writer_crew_with_sample_data(sample_patient_profile, sample_diagnosis, sample_supplements_recommendation, sample_exercise_recommendation):
    """Test WriterCrew with sample data"""
    sample_data = {
        "patient_profile": sample_patient_profile,
        "diagnosis": sample_diagnosis,
        "supplements_recommendation": sample_supplements_recommendation,
        "exercise_recommendation": sample_exercise_recommendation,
        "output_file_format": ".md"
    }
    
    crew = WriterCrew().crew()
    result = crew.kickoff(inputs=sample_data)
    
    assert result is not None
    assert result.raw is not None
    assert len(result.raw) > 0
    # Check if the result contains some expected keywords
    # currently a very lose one
    assert any(keyword in result.raw.lower() for keyword in ["recommendation", "diagnosis", "supplements", "exercise", "profile", "conclusion"])

def test_writer_crew_with_empty_inputs():
    """Test WriterCrew with empty inputs"""
    crew = WriterCrew()
    with pytest.raises(Exception):
        crew.kickoff(inputs={
            "patient_profile": "",
            "diagnosis": "",
            "supplements_recommendation": "",
            "exercise_recommendation": "",
            "output_file_format": ".md"
        })

def test_writer_crew_with_empty_output_file_format(sample_patient_profile, sample_diagnosis, sample_supplements_recommendation, sample_exercise_recommendation):
    """Test WriterCrew with empty output file format"""
    crew = WriterCrew()
    with pytest.raises(Exception):
        crew.kickoff(inputs={
            "patient_profile": sample_patient_profile,
            "diagnosis": sample_diagnosis,
            "supplements_recommendation": sample_supplements_recommendation,
            "exercise_recommendation": sample_exercise_recommendation,
            "output_file_format": ""
        })


def test_writer_crew_with_missing_inputs():
    """Test WriterCrew with missing inputs"""
    crew = WriterCrew()
    with pytest.raises(Exception):
        crew.kickoff(inputs={})  # Missing required inputs

def test_writer_crew_output_file(sample_patient_profile, sample_diagnosis, sample_supplements_recommendation, sample_exercise_recommendation):
    """Test that WriterCrew creates an output file"""
    sample_data = {
        "patient_profile": sample_patient_profile,
        "diagnosis": sample_diagnosis,
        "supplements_recommendation": sample_supplements_recommendation,
        "exercise_recommendation": sample_exercise_recommendation,
        "output_file_format": ".md"
    }
    
    crew = WriterCrew()
    result = crew.kickoff(inputs=sample_data)
    
    # Check if output file exists
    output_file = "output_data/recommendation.md"
    assert os.path.exists(output_file)
    
    # Clean up
    if os.path.exists(output_file):
        os.remove(output_file) 