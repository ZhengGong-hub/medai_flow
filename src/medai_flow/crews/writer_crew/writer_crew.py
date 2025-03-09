from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from src.medai_flow.validation.input_validation import validate_patient_profile, validate_diagnosis, validate_output_file_format
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators


@CrewBase
class WriterCrew:
    """Writer Crew"""

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    # If you would lik to add tools to your crew, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def writer_expert(self) -> Agent:
        return Agent(
            config=self.agents_config["writer_expert"],
            verbose=True,
        )

    @task
    def writer_task(self) -> Task:
        return Task(
            config=self.tasks_config["writer_task"],
            output_file="output_data/recommendation{output_file_format}"
        )


    @crew
    def crew(self) -> Crew:
        """Creates the Research Crew"""

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
        validate_output_file_format(inputs)
        return self.crew().kickoff(inputs=inputs)
