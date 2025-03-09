import pytest
from medai_flow.crews.supplements_crew.supplements_crew import SupplementsCrew

def test_supplements_crew_initialization():
    """Test that SupplementsCrew can be initialized"""
    crew = SupplementsCrew()
    assert crew is not None

def test_supplements_crew_creation():
    """Test that SupplementsCrew can create a crew"""
    crew = SupplementsCrew().crew()
    assert crew is not None
    assert len(crew.agents) > 0
    assert len(crew.tasks) > 0

@pytest.mark.asyncio
async def test_supplements_crew_with_sample_data(sample_patient_profile, sample_diagnosis):
    """Test SupplementsCrew with sample patient data and diagnosis"""
    
    crew = SupplementsCrew()    
    result = await crew.kickoff_async(inputs={
        "patient_profile": sample_patient_profile,
        "diagnosis": sample_diagnosis
    })
    
    assert result is not None
    assert result.raw is not None
    assert len(result.raw) > 0
    # Check if the result contains some expected keywords
    assert any(keyword in result.raw.lower() for keyword in ["supplement", "vitamin", "recommendation", "dosage"])

@pytest.mark.asyncio
async def test_supplements_crew_with_empty_inputs():
    """Test SupplementsCrew with empty inputs"""
    crew = SupplementsCrew()
    with pytest.raises(Exception):
        await crew.kickoff_async(inputs={
            "patient_profile": "",
            "diagnosis": ""
        })

@pytest.mark.asyncio
async def test_supplements_crew_with_missing_inputs():
    """Test SupplementsCrew with missing inputs"""
    crew = SupplementsCrew()
    with pytest.raises(Exception):
        await crew.kickoff_async(inputs={})  # Missing required inputs 