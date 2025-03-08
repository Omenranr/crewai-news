from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool, ScrapeWebsiteTool, FileWriterTool
from dotenv import load_dotenv

# Load environment variables (e.g., API keys for tools)
load_dotenv()

@CrewBase
class AiNews():
    """AiNews crew"""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def manager(self) -> Agent:
        """Manager agent to oversee the workflow"""
        return Agent(
            config=self.agents_config['manager'],
            tools=[],
            verbose=True
        )

    @agent
    def research_agent(self) -> Agent:
        """Agent responsible for researching and gathering news content"""
        return Agent(
            config=self.agents_config['research_agent'],
            tools=[SerperDevTool(), ScrapeWebsiteTool()],
            verbose=True
        )

    @agent
    def evaluator(self) -> Agent:
        """Agent to evaluate the sufficiency of collected content"""
        return Agent(
            config=self.agents_config['evaluator'],
            tools=[],
            verbose=True
        )

    @agent
    def ai_news_writer(self) -> Agent:
        """Agent to write the news article"""
        return Agent(
            config=self.agents_config['ai_news_writer'],
            tools=[],
            verbose=True
        )

    @agent
    def file_writer(self) -> Agent:
        """Agent to save the article to a file"""
        return Agent(
            config=self.agents_config['file_writer'],
            tools=[FileWriterTool()],
            verbose=True
        )

    @task
    def research_task(self) -> Task:
        """Task to gather sufficient news content"""
        return Task(
            config=self.tasks_config['research_task'],
        )

    @task
    def evaluate_task(self) -> Task:
        """Task to evaluate the collected content"""
        return Task(
            config=self.tasks_config['evaluate_task'],
        )

    @task
    def write_task(self) -> Task:
        """Task to write the news article"""
        return Task(
            config=self.tasks_config['write_task'],
        )

    @task
    def file_write_task(self) -> Task:
        """Task to save the article to a file"""
        return Task(
            config=self.tasks_config['file_write_task'],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the AiNews crew with a hierarchical process"""
        return Crew(
            agents=[
                self.research_agent(),
                self.evaluator(),
                self.ai_news_writer(),
                self.file_writer()
            ],  # Exclude manager from agents list
            tasks=[
                self.research_task(),
                self.evaluate_task(),
                self.write_task(),
                self.file_write_task()
            ],
            process=Process.hierarchical,
            manager_agent=self.manager(),  # Manager specified separately
            verbose=True,
        )