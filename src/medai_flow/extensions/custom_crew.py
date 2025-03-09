# this has not been thought through yet
from crewai import Agent, Crew, Process, Task
# define a custom crew subclass 

class CustomCrew(Crew):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test(self, inputs: dict, **kwargs):
        print("--------------------------------")
        print("test")
        print("--------------------------------")
        return 
