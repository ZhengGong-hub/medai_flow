from typing import Type

from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from math import pi, sqrt

class BRICalculatorInput(BaseModel):
    """Input schema for BRICalculator."""

    waist_circumference: float = Field(..., description="circumference of the waist in meters")
    height: float = Field(..., description="Height in meters")


class BRICalculator(BaseTool):
    name: str = "Body Roundness Index Calculator (BRI)"
    description: str = (
        """Calculate the Body Roundness Index of a person (BRI),

        source: https://www.usz.ch/en/bri-calculator/

        Args:
            waist_circumference (float): Circumference of the waist in meters
            height (float): Height in meters

        Returns:
            float: Body Roundness Index value
        
        Example:
            >>> bri_calculator(waist_circumference=0.7, height=1.7)
        """
    )
    args_schema: Type[BaseModel] = BRICalculatorInput

    def _run(self, waist_circumference: float, height: float) -> float:
        # Implementation goes here
        # body round index 
        # Body Roundness Index = 364.2 − 365.5 × Eccentricity

        bri = 364.2 - 365.5 * sqrt(1 - (waist_circumference / (pi * height)) ** 2)

        return bri


