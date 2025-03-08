from crew import AiNews  # Adjust import based on your project structure
from datetime import date

from crewai.telemetry import Telemetry

def noop(*args, **kwargs):
    print("Telemetry method called and noop'd\n")
    pass

for attr in dir(Telemetry):
    if callable(getattr(Telemetry, attr)) and not attr.startswith("__"):
        setattr(Telemetry, attr, noop)

# Instantiate the crew
crew_instance = AiNews()

# Set the current date
current_date = date.today().strftime("%Y-%m-%d")  # e.g., "2025-03-08"

# Run the crew with both topic and date inputs
result = crew_instance.crew().kickoff(inputs={"topic": "Most recent news about AI", "date": current_date})
print(result)