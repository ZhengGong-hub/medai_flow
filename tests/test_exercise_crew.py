import pytest
from medai_flow.crews.exercise_crew.exercise_crew import ExerciseCrew

def test_exercise_crew_initialization():
    """Test that ExerciseCrew can be initialized"""
    crew = ExerciseCrew()
    assert crew is not None

def test_exercise_crew_creation():
    """Test that ExerciseCrew can create a crew"""
    crew = ExerciseCrew().crew()
    assert crew is not None
    assert len(crew.agents) > 0
    assert len(crew.tasks) > 0

@pytest.mark.asyncio
async def test_exercise_crew_with_sample_data(sample_patient_profile, sample_diagnosis):
    """Test ExerciseCrew with sample patient data and diagnosis"""
    crew = ExerciseCrew()
    result = await crew.kickoff_async(inputs={
        "patient_profile": sample_patient_profile,
        "diagnosis": sample_diagnosis
    })
    
    assert result is not None
    assert result.raw is not None
    assert len(result.raw) > 0
    assert any(keyword in result.raw.lower() for keyword in ["exercise", "workout", "routine", "recommendation"])


@pytest.mark.asyncio
async def test_exercise_crew_with_empty_inputs():
    """Test ExerciseCrew with empty inputs"""
    crew = ExerciseCrew()
    with pytest.raises(Exception):
        await crew.kickoff_async(inputs={
            "patient_profile": "",
            "diagnosis": ""
        })

@pytest.mark.asyncio
async def test_exercise_crew_with_missing_inputs():
    """Test ExerciseCrew with missing inputs"""
    crew = ExerciseCrew()
    with pytest.raises(Exception):
        await crew.kickoff_async(inputs={})  # Missing required inputs 