#!/usr/bin/env python
from pydantic import BaseModel
import asyncio

from crewai.flow import Flow, listen, start

from medai_flow.crews.supplements_crew.supplements_crew import SupplementsCrew
from medai_flow.crews.exercise_crew.exercise_crew import ExerciseCrew
from medai_flow.crews.writer_crew.writer_crew import WriterCrew
from medai_flow.crews.diagnose_crew.diagnose_crew import DiagnoseCrew

class RecommendationState(BaseModel):
    patient_profile: str = ""
    recommendation: str = ""
    supplements_recommendation: str = ""
    exercise_recommendation: str = ""
    diagnosis: str = ""

class RecommendationFlow(Flow[RecommendationState]):

    @start()
    def input_patient_profile(self):
        print("Generating sentence count")

        # get patient profile from directory
        with open("input_data/patient_b_profile.md", "r") as f:
            self.state.patient_profile = f.read()
    
    @listen(input_patient_profile)
    def diagnose_patient(self):
        print("Diagnosing patient")
        # get patient profile from directory
        diagnose_crew = DiagnoseCrew().crew()
        diagnose_result = diagnose_crew.kickoff(
            inputs={
                "patient_profile": self.state.patient_profile
            }
        )
        self.state.diagnosis = diagnose_result.raw

    @listen(diagnose_patient)
    async def generate_recommendation(self):
        print("Generating supplements recommendation")
        supplements_crew = SupplementsCrew().crew()
        exercise_crew = ExerciseCrew().crew()   

        # Launch both crews concurrently using asyncio.gather:
        supplements_result, exercise_result = await asyncio.gather(
            supplements_crew.kickoff_async(inputs={"patient_profile": self.state.patient_profile, "diagnosis": self.state.diagnosis}),
            exercise_crew.kickoff_async(inputs={"patient_profile": self.state.patient_profile, "diagnosis": self.state.diagnosis})
        )

        print("Supplements recommendation generated", supplements_result.raw)
        print("Exercise recommendation generated", exercise_result.raw)
        self.state.supplements_recommendation = supplements_result.raw
        self.state.exercise_recommendation = exercise_result.raw

    @listen(generate_recommendation)
    def output_recommendation(self):
        print("Output recommendation")
        writer_crew = WriterCrew().crew()
        writer_crew.kickoff(
            inputs={
                "supplements_recommendation": self.state.supplements_recommendation, 
                "exercise_recommendation": self.state.exercise_recommendation,
                "patient_profile": self.state.patient_profile,
                "diagnosis": self.state.diagnosis
            }
        )



def kickoff():
    recommendation_flow = RecommendationFlow()
    recommendation_flow.kickoff()


def plot():
    recommendation_flow = RecommendationFlow()
    recommendation_flow.plot(
        "output_data/recommendation_flow"
    )


if __name__ == "__main__":
    kickoff()
