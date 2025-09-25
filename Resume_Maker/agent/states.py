from pydantic import BaseModel,Field
from typing import List,Optional,Annotated,Literal
from typing_extensions import TypedDict


class GraphState(TypedDict):
    LaTeX : str
    resume : str
    job_description : str 
    custom_instructions : str 
    links : str
    status : str
    max_iters : int
    status    : Literal["DONE","INPROGRESS"] 

class Header(BaseModel):
    name : str = Field(default=None,description="Name of the candidate")    
    mobile_number : str = Field(default=None,description="Mobile number of the candidate")
    email_id : str = Field(default=None,description="email_id if the candidate")
    linkedin_profile_link : str = Field(default=None,description="valid Linkedin profile link of the candidate.")
    github_link : str = Field(default=None,description="Valid github link of the candidate.")



class ProfessionalSummary(BaseModel):
    summary  : str = Field(default=None,description=(
        "Generate a concise professional summary (max 4 lines) using the STAR method. Focus on the candidate's experience, key skills, relevant tools, and the specific role being applied for. Do not quantify achievements in numbers; instead, emphasize alignment with the target position and required skills. Example: 'Experienced Gen AI Specialist skilled in ML, DL, and AI Agents, with a strong background in end-to-end development and a passion for driving innovation in technology-focused environments.'"
    ))

class ProfessionalExperience(BaseModel):
    company_name : str =  Field(default=None,description="Name of the organization/company the candidate worked at")
    location : str = Field(default=None,description = "Location of the company. If not mentioned in the resume then keep it as empty string ''.")
    period : str = Field(default=None,description = 'Employment duration (e.g., "Jan 2020 - Dec 2022"). Give the exact duration dont synthesize')
    role : str = Field(default=None,description = "Title or designation. Don't synthesize anything here." )
    bullet_points : List[str] = Field(default=None,description = "Key achievements/responsibilities. These points must be in ATS friendly format, quantifying things and  following the STAR method(situation, task , action and result)(eg. reduced latency by 5ms, improved accuracy by 50%).")

class Project(BaseModel):
    project_name : str = Field(default=None,description="Project Name")
    tools_used : List[str] =  Field(default=None,description="Tools and technologies used in the project (eg Python, Flask, React, PostgreSQL, Docker)")
    period : Optional[str] = Field(default=None,description="Project Duration.(eg. Jan 2020- Dec 2022)")
    bullet_points : List[str] = Field(default=None,description='Key achievements/responsibilities.These points must be in ATS friendly format, quantifying things and  following the STAR method(situation, task , action and result)(eg. reduced latency by 5ms, improved accuracy by 50%')

class Education(BaseModel):
    Institute : str  = Field(default=None,description="Name of the Institute.")
    location  : str  = Field(default=None,description="Location of the Institute.")
    period    : str  = Field(default=None,description="Education duration (e.g., Jan 2020 - Dec 2022)")
    specialization : str = Field(default=None,description="Specialization of education (e.g., Bachelors in computer science, Intermediate, High School)")

class Achievements(BaseModel):
    achievements : List[str] = Field(default=None,description= "Achievement should be a concise statement highlighting a significant accomplishment, award, or recognition relevant to the candidate's professional background. Put it an empty string if there are no achievements to include in the resume.")

class Skills(BaseModel):
    programming_languages : List[str] = Field(default=None,description="list of all the programming languages the candidate is aware of and the new job is expecting. (eg. Python,java,js, HTML, CSS)")
    technologies : List[str] = Field(default=None,description="contains a list of all the technologies which are relevant to the Job description as well as the technologies which the candidate know")
    # other_skills : Optional[List[str]] = Field(description="")
    frameworks  : Optional[List[str]] = Field(default=None,description="list of all frameworks the candidate knows and the job is expecting")
    tools  : Optional[List[str]] = Field(default=None,description="include generic tools like vscode, git version control if the resume is too short else include tools like AWS lambda, langchainm etc..")

class QuickResume(BaseModel):
    header : Header = Field(default=None,description="Header details of the user.")
    professional_summary : ProfessionalSummary = Field(default=None,description="ProfessionalSummary of the user")
    professional_experience : List[ProfessionalExperience] = Field(default=None,description= "list of professional experiences of the candidate")
    projects : List[Project] = Field(default=None,description= "List of projects of the candidate")
    education : List[Education] = Field(default=None,description= "list of all educational backgrounds. Include only the most recent one unless the user provides any custom instructions")
    achievements : Optional[Achievements] = Field( default=None,description = "Achievements of the candidates to include in resume")
    skills : Skills = Field(default=None,description="all the skills the job is expecting and the user know. Dont bold any thing here")


class HumanFeedback(BaseModel):
    feedback  : str = Field(default ="", description="detailed feedback of the user which helps in improving the resume's ATS score")


## LLM with tools , with structuted output of header --> will call on prompt 
## Create react agent for llm with structured output
## For Quick resume give ATS prompt and Quickresume as structured output
## For personal and header details use HIL tool
