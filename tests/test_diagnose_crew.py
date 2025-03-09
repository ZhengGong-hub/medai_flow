import pytest
from medai_flow.crews.diagnose_crew.diagnose_crew import DiagnoseCrew

def test_diagnose_crew_initialization():
    """Test that DiagnoseCrew can be initialized"""
    crew = DiagnoseCrew()
    assert crew is not None

def test_diagnose_crew_creation():
    """Test that DiagnoseCrew can create a crew"""
    crew = DiagnoseCrew().crew()
    assert crew is not None
    assert len(crew.agents) > 0
    assert len(crew.tasks) > 0

def test_diagnose_crew_with_sample_profile(sample_patient_profile):
    """Test DiagnoseCrew with a sample patient profile"""
    crew = DiagnoseCrew()
    result = crew.kickoff(inputs={"patient_profile": sample_patient_profile})
    
    assert result is not None
    assert result.raw is not None
    assert len(result.raw) > 0
    # Check if the result contains some expected keywords
    assert any(keyword in result.raw.lower() for keyword in ["bmi", "overweight", "weight"])

def test_diagnose_crew_with_empty_profile():
    """Test DiagnoseCrew with an empty profile"""
    crew = DiagnoseCrew()
    with pytest.raises(Exception):
        crew.kickoff(inputs={"patient_profile": ""})

def test_diagnose_crew_with_invalid_input():
    """Test DiagnoseCrew with invalid input"""
    crew = DiagnoseCrew()
    with pytest.raises(Exception):
        crew.kickoff(inputs={})  # Missing patient_profile 