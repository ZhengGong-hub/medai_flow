from typing import Type

from crewai.tools import BaseTool
from pydantic import BaseModel, Field


class BMICalculatorInput(BaseModel):
    """Input schema for BMICalculator."""

    weight: float = Field(..., description="Weight in kilograms")
    height: float = Field(..., description="Height in meters")


class BMICalculator(BaseTool):
    name: str = "BMI Calculator"
    description: str = (
        """Calculate the BMI of a person,

        Args:
            weight (float): Weight in kilograms
            height (float): Height in meters

        Returns:
            float: BMI value
        
        Example:
            >>> bmi_calculator(weight=70, height=1.7)
            >>> 24.22
        """
    )
    args_schema: Type[BaseModel] = BMICalculatorInput

    def _run(self, weight: float, height: float) -> float:
        # Implementation goes here
        return weight / (height ** 2)
