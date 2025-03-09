import pytest
import os
import sys

# Add src directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

@pytest.fixture
def sample_patient_profile():
    """Fixture providing a sample patient profile"""
    return """
    Patient Profile:
    - Age: 35
    - Gender: Female
    - Height: 165cm
    - Weight: 70kg
    - Medical History: None
    - Current Symptoms: Fatigue, occasional headaches
    """

@pytest.fixture
def sample_diagnosis():
    """Fixture providing a sample diagnosis"""
    return """
    Diagnosis:
    - Primary: Vitamin D deficiency
    - Secondary: Iron deficiency anemia
    - Risk Factors: Sedentary lifestyle, limited sun exposure
    """

@pytest.fixture
def sample_supplements_recommendation():
    """Fixture providing a sample supplements recommendation"""
    return """
    Supplements Recommendation:
    - Vitamin D: 1000 IU daily
    - Iron: 18mg daily
    - Magnesium: 200mg daily
    """

@pytest.fixture
def sample_exercise_recommendation():
    """Fixture providing a sample exercise recommendation"""
    return """
    Exercise Recommendation:
    - Daily walking: 30 minutes
    - Light stretching: 15 minutes
    - Strength training: 2-3 times per week
    """

@pytest.fixture
def output_dir():
    """Fixture to ensure output directory exists"""
    os.makedirs("output_data", exist_ok=True)
    yield "output_data"
    # Clean up any test files after tests
    if os.path.exists("output_data/recommendation.md"):
        os.remove("output_data/recommendation.md") 