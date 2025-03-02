import streamlit as st
import asyncio
from pydantic import BaseModel
import os
from crewai.flow import Flow, listen, start
import tempfile
import sys
from pathlib import Path

src_path = str(Path(__file__).parent.parent.parent / "src")
if src_path not in sys.path:
    sys.path.append(src_path)

from medai_flow import __version__
from medai_flow.crews.supplements_crew.supplements_crew import SupplementsCrew
from medai_flow.crews.exercise_crew.exercise_crew import ExerciseCrew
from medai_flow.crews.writer_crew.writer_crew import WriterCrew
from medai_flow.crews.diagnose_crew.diagnose_crew import DiagnoseCrew
from medai_flow.crews.input_parser_crew.input_parser_crew import InputParserCrew



class StreamlitRecommendationState(BaseModel):
    patient_profile: str = ""
    recommendation: str = ""
    supplements_recommendation: str = ""
    exercise_recommendation: str = ""
    diagnosis: str = ""

class StreamlitRecommendationFlow(Flow[StreamlitRecommendationState]):
    def __init__(self, status_container):
        super().__init__()
        self.status_container = status_container

    @start()
    def input_patient_profile(self):
        self.status_container.write("📄 Processing patient profile...")
        
        if self.state.patient_profile.endswith('.pdf'):
            self.status_container.write("🔍 Parsing PDF file...")
            input_parser_crew = InputParserCrew().crew()
            input_parser_result = input_parser_crew.kickoff(
                inputs={"pdf_file_address": self.state.patient_profile}
            )
            if "Failed to extract" in input_parser_result.raw:
                raise Exception("Failed to extract text from file!")
            else:
                self.state.patient_profile = input_parser_result.raw
        
        self.status_container.write("✅ Patient profile processed successfully!")

    @listen(input_patient_profile)
    def diagnose_patient(self):
        self.status_container.write("🏥 Medical Expert is analyzing patient profile...")
        diagnose_crew = DiagnoseCrew().crew()
        diagnose_result = diagnose_crew.kickoff(
            inputs={
                "patient_profile": self.state.patient_profile
            }
        )
        self.state.diagnosis = diagnose_result.raw
        self.status_container.write("✅ Medical diagnosis completed!")

    @listen(diagnose_patient)
    async def generate_recommendation(self):
        self.status_container.write("💊 Generating supplements recommendation...")
        self.status_container.write("🏃‍♂️ Creating exercise plan...")
        
        supplements_crew = SupplementsCrew().crew()
        exercise_crew = ExerciseCrew().crew()

        supplements_result, exercise_result = await asyncio.gather(
            supplements_crew.kickoff_async(inputs={
                "patient_profile": self.state.patient_profile,
                "diagnosis": self.state.diagnosis
            }),
            exercise_crew.kickoff_async(inputs={
                "patient_profile": self.state.patient_profile,
                "diagnosis": self.state.diagnosis
            })
        )

        self.state.supplements_recommendation = supplements_result.raw
        self.state.exercise_recommendation = exercise_result.raw
        
        self.status_container.write("✅ Supplements recommendation completed!")
        self.status_container.write("✅ Exercise plan completed!")

    @listen(generate_recommendation)
    def output_recommendation(self):
        self.status_container.write("📝 Compiling final report...")
        writer_crew = WriterCrew().crew()
        result = writer_crew.kickoff(
            inputs={
                "supplements_recommendation": self.state.supplements_recommendation,
                "exercise_recommendation": self.state.exercise_recommendation,
                "patient_profile": self.state.patient_profile,
                "diagnosis": self.state.diagnosis,
                "output_file_format": ".md",
            }
        )
        self.state.recommendation = result.raw
        self.status_container.write("✅ Final report generated!")
        return result.raw

def main():
    st.set_page_config(
        page_title="NOVA Agentic Framework",
        page_icon="🏥",
        layout="wide"
    )

    # Create a header container with title and version
    header_col1, header_col2 = st.columns([4, 1])
    with header_col1:
        st.title("🏥 NOVA Agentic Framework")
    with header_col2:
        st.markdown(f"<p style='text-align: right; color: #666666; padding-top: 20px;'>v{__version__}</p>", unsafe_allow_html=True)

    st.write("Upload a patient profile or paste the text directly to get personalized health recommendations.")

    # Create two columns
    col1, col2 = st.columns(2)

    with col1:
        # Add example data option
        use_example = st.checkbox("Use example patient profile", value=False)
        
        # File upload option
        uploaded_file = st.file_uploader("Upload patient profile (PDF or MD)", type=['pdf', 'md'], disabled=use_example)
        
        # Text input option with example data
        default_text = ""
        if use_example:
            try:
                with open("/home/azureuser/medai_flow/input_data/gold_standard/patient_b_profile.md", "r") as f:
                    default_text = f.read()
            except Exception as e:
                st.error(f"Failed to load example profile: {str(e)}")
                
        text_input = st.text_area(
            "Or paste patient profile text here", 
            value=default_text,
            height=300,
            disabled=use_example
        )

    with col2:
        # Status container
        status_container = st.empty()
        
        if st.button("Generate Recommendations", type="primary"):
            if not uploaded_file and not text_input:
                st.error("Please either upload a file or paste text")
                return

            # Create status container for real-time updates
            status_box = status_container.container()
            status_box.write("🚀 Starting analysis...")

            try:
                # Initialize the flow with status container
                flow = StreamlitRecommendationFlow(status_box)
                
                # Set the patient profile based on input method
                if uploaded_file:
                    # Save uploaded file to temporary location
                    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
                        tmp_file.write(uploaded_file.getvalue())
                        flow.state.patient_profile = tmp_file.name
                else:
                    flow.state.patient_profile = text_input

                # Run the flow
                result = flow.kickoff()

                # Display the final recommendation
                st.markdown("### 📋 Final Recommendation")
                st.markdown(flow.state.recommendation)

                # Offer download option
                st.download_button(
                    label="Download Recommendation",
                    data=flow.state.recommendation,
                    file_name="health_recommendation.md",
                    mime="text/markdown"
                )

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                status_box.error("❌ Process failed")

            finally:
                # Clean up temporary file if it exists
                if uploaded_file and 'tmp_file' in locals():
                    os.unlink(tmp_file.name)

if __name__ == "__main__":
    main() 