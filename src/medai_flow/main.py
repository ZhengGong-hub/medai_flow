#!/usr/bin/env python
from pydantic import BaseModel
import asyncio
import os
from crewai.flow import Flow, listen, start
import sys
from medai_flow.crews.supplements_crew.supplements_crew import SupplementsCrew
from medai_flow.crews.exercise_crew.exercise_crew import ExerciseCrew
from medai_flow.crews.writer_crew.writer_crew import WriterCrew
from medai_flow.crews.diagnose_crew.diagnose_crew import DiagnoseCrew
from medai_flow.crews.input_parser_crew.input_parser_crew import InputParserCrew


class RecommendationState(BaseModel):
    patient_profile: str = ""
    recommendation: str = ""
    supplements_recommendation: str = ""
    exercise_recommendation: str = ""
    diagnosis: str = ""

class RecommendationFlow(Flow[RecommendationState]):
    

    @start()
    def input_patient_profile(self):
        file_path = "input_data/gold_standard/patient_b_profile.md"

        if os.path.exists(file_path):
            # check whether it is pdf or md 
            if file_path.endswith(".pdf"):
                print("Parsing PDF file")
                input_parser_crew = InputParserCrew().crew()
                input_parser_result = input_parser_crew.kickoff(
                    inputs={"pdf_file_address": file_path}
                )       
                if "Failed to extract" in input_parser_result.raw:
                    raise Exception("Failed to extract text from file!")
                else:
                    self.state.patient_profile = input_parser_result.raw
            elif file_path.endswith(".md"):
                with open(file_path, "r") as f:
                    self.state.patient_profile = f.read()
            else:
                raise Exception("File is not a PDF or MD file!")
        else:
            raise Exception("File does not exist!")
            


    @listen(input_patient_profile)
    def diagnose_patient(self):
        print("Diagnosing patient")
        # get patient profile from directory
        diagnose_crew = DiagnoseCrew()
        diagnose_result = diagnose_crew.kickoff(
            inputs={
                "patient_profile": self.state.patient_profile
            }
        )
        self.state.diagnosis = diagnose_result.raw

    @listen(diagnose_patient)
    async def generate_recommendation(self):
        print("Generating recommendation")
        supplements_crew = SupplementsCrew()
        exercise_crew = ExerciseCrew()

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
                "diagnosis": self.state.diagnosis,
                "output_file_format": ".md",
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

def test():

    with open("input_data/gold_standard/patient_b_profile.md", "r") as f:
        patient_profile = f.read()
    inputs = {
        "patient_profile": patient_profile,
    }
    try:
        diagnose_crew = DiagnoseCrew().crew()
        n_iterations = int(sys.argv[1]) if len(sys.argv) > 1 else 2 # set default to 2
        model_name = sys.argv[2] if len(sys.argv) > 2 else "gpt-4o" # set default to gpt-4o
        diagnose_crew.test(n_iterations=n_iterations, openai_model_name=model_name, inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while testing the diagnose crew: {e}")

if __name__ == "__main__":
    kickoff()
