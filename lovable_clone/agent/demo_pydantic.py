from pydantic import BaseModel, Field
from typing import List
from langchain_groq import ChatGroq
from dotenv import load_dotenv

_ = load_dotenv()



llm = ChatGroq(model="openai/gpt-oss-120b")

class ImplementationTask(BaseModel):
    path : str  = Field(description= "path of the file to be implemented")
    description : str = Field(description= "detailed description of the implementation steps of the file.")

class DeveloperState(BaseModel):
    implementation_task : List[ImplementationTask] = Field(description="List of implementation tasks to be implemented by the developer")
    current_index : int = Field(description="current index")

it1 = ImplementationTask(path = "app.py",description = "some desc")
# print(it1)

# print(it1.model_dump_json())


it2 = DeveloperState(implementation_task=[it1], current_index=0)

# print(it2)

# print(it2.model_dump_json())

print(llm.with_structured_output(DeveloperState).invoke(it1.model_dump_json()))