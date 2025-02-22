from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from src.medai_flow.tools.bmi_calculator import BMICalculator
from src.medai_flow.tools.bri_calculator import BRICalculator
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class DiagnoseCrew:
    """Diagnose Crew"""

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    # instance of the tools
    bmi_calculator = BMICalculator()
    bri_calculator = BRICalculator()
    # If you would lik to add tools to your crew, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    
    @agent
    def diagnosis_expert(self) -> Agent:
        return Agent(
            config=self.agents_config["diagnosis_expert"],
            verbose=True,
            tools=[self.bmi_calculator, self.bri_calculator],
        )

    @task
    def diagnosis_task(self) -> Task:
        return Task(
            config=self.tasks_config["diagnosis_task"],
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
