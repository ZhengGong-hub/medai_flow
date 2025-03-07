from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.knowledge.source.pdf_knowledge_source import PDFKnowledgeSource
from src.medai_flow.validation.input_validation import validate_patient_profile, validate_diagnosis
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators


@CrewBase
class ExerciseCrew:
    """Exercise Crew"""

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    # Create a PDF knowledge source
    pdf_source = PDFKnowledgeSource(
        file_paths=[
            "Aging Hallmarks: The Benefits of Physical Exercise.pdf", 
            "Resistance Exercise Training as a Primary Countermeasure to Age-Related Chronic Disease.pdf"
            ]
    )
    
    # If you would lik to add tools to your crew, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def exercise_expert(self) -> Agent:
        return Agent(
            config=self.agents_config["exercise_expert"],
            verbose=True,
            knowledge_sources=[self.pdf_source]
        )

    @task
    def exercise_task(self) -> Task:
        return Task(
            config=self.tasks_config["exercise_task"],
        )


    @crew
    def crew(self) -> Crew:
        """Creates the Research Crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )

    def kickoff(self, inputs: dict):
        """Kickoff the crew"""
        validate_patient_profile(inputs)
        validate_diagnosis(inputs)
        return self.crew().kickoff(inputs=inputs)
    
    def kickoff_async(self, inputs: dict):
        """Kickoff the crew"""
        validate_patient_profile(inputs)
        validate_diagnosis(inputs)
        return self.crew().kickoff_async(inputs=inputs)