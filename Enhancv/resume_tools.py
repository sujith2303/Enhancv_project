from smolagents import CodeAgent, LiteLLMModel, tool
from pypdf import PdfReader
import google.generativeai as genai
import os
from typing import List
from utils import CURRENT_RESUME_LATEX as LATEX_TEMPLATE 
from utils import CURRENT_RESUME_LATEX
import os
import re
import json
from dotenv import load_dotenv

# load_dotenv(".env")


@tool
def header_details(name: str, mobile_number: str, email_id: str, linkedin_profile_link : str, github_link: str) -> str:
    """
    Generates header details of the person. It will display the name, mobile_number, email_id, linkedin profile and github profile
    
    Args:
        name(str): Name of the candidate
        mobile_number(str): Mobile number of the candidate
        email_id(str): email_id
        linkedin_profile_link(str): Linkedin profile link of the candidate.
        github_link(str): github link of the candidate.
    
    Returns:
        str: Instruction for the next steps
    """

    header_latex = r""" 

            \begin{center}
                \textbf{\Huge \scshape """
    header_latex+= name + r"""} \\ \vspace{1pt}
                \small""" + mobile_number + r""" $|$ \href{mailto:""" + email_id + r"""}{\underline{"""
    header_latex+= email_id + r"""}} $|$ 
                \href{""" + linkedin_profile_link + r"""}{\underline{"""
    header_latex+= r"""linkedin}} $|$
    \href{""" + github_link + r"""}{\underline{"""
    header_latex+=r"""github}}
    \end{center}


    """
    global CURRENT_RESUME_LATEX
    CURRENT_RESUME_LATEX = LATEX_TEMPLATE
    CURRENT_RESUME_LATEX += header_latex
    response_message = "Now call professional_summary_tool"
    return response_message


@tool
def professional_summary(summary: str) -> str:
    """
    Creates a Professional Experience summary section of the candidate. 
    
    Args:
        summary (str): The generated summary should be in less than 4 lines. It should follow the STAR method while generating the summary. It should speak about the experience and the role he is applying for.
        (e.g: Accomplished Gen AI Specialist with expertise in machine learning (ML), deep learning (DL), generative AI, and AI Agents, proficient in end-to end development from design to deployment. Skilled in problem-solving, data structures and algorithms (DSA), strong analytical abilities, and debugging complex systems. Passionate about optimizing ML model performance to deliver efficient, high-impact AI solutions. Adept at leveraging the full AI stack to drive innovation and achieve business objectives in fast-paced, technology-focused environments)
    
    
    Returns:
        str: Instruction for the next steps
    """

    summary_latex = """
    
    \section{Professional Summary}
    """
    summary_latex += rf"""
    {{{summary}}}
    """
    summary_latex = summary_latex.replace("%","\%")
    global CURRENT_RESUME_LATEX
    CURRENT_RESUME_LATEX += summary_latex
    response_message = "Now call the professional_experience_tool"
    return response_message

@tool
def professional_experience(experiences: List[dict]) -> str:
    """
   Creates an Experience section for a user.Processes the user work experiences across different companies and generates a string in latex form which will be used in further steps


    Args:
        experiences (list of dict): A list where each dict contains:
            - company_name (required) (str): Name of the company.
            - place (Optional) (str): Location of the company. If not mentioned in the resume then keep it as empty string "".
            - period (required) (str): Employment duration (e.g., "Jan 2020 - Dec 2022").
            - role (required) (str): Title or designation.
            - bullet_points (required) (list of str): Key achievements/responsibilities. These points must be in ATS friendly format, quantifying things and  following the STAR method(situation, task , action and result)(eg. reduced latency by 5ms, improved accuracy by 50%).

    Returns:
        str: Instruction for the next steps
    """
    Experience_latex = r"""
    
    \section{Professional Experience}
    \resumeSubHeadingListStart
    """
    for exp in experiences:
        company = exp['company_name']
        period  = exp['period']
        place   = exp['place']
        role    = exp['role']
        bullet_points = exp['bullet_points']
        Experience_latex += rf"""
            \resumeSubheading
              {{{role}}}{{{period}}}
              {{{company}}}{{{place}}}
              \resumeItemListStart
              
            """
        for item in bullet_points:
            Experience_latex += rf"""
            \resumeItem{{{item}}}
            """
        Experience_latex += r"""
        \resumeItemListEnd
       
    \resumeSubHeadingListEnd
    """
    Experience_latex = Experience_latex.replace("%","\%")
    global CURRENT_RESUME_LATEX
    CURRENT_RESUME_LATEX += Experience_latex
    response_message = "Now call the projects tool"
    return response_message


@tool
def projects(projects: List[dict]) -> str :
    """
    Creates an projects section for a user. Processes the projects and generates a string in latex form which will be used in further steps

    Args:
        projects (list of dict): A list where each dict contains:
            - project_name (required) (str): Name of the project.
            - tools_used (required)(list[str]): Tools and technologies used in the project (eg Python, Flask, React, PostgreSQL, Docker). It is a list of strings.
            - period (required)(str): Project duration (e.g., "Jan 2020 - Dec 2022").
            - bullet_points (required) (list of str): Key achievements/responsibilities.These points must be in ATS friendly format, quantifying things and  following the STAR method(situation, task , action and result)(eg. reduced latency by 5ms, improved accuracy by 50%).

    Returns:
        str: Instruction for the next steps
    """
    Projects_latex = r"""
    
    \section{Projects}
    \resumeSubHeadingListStart
    """
    for project in projects:
        project_name = project['project_name']
        period = project['period']
        tools = ", ".join(project['tools_used'])
        bullet_points = project['bullet_points']
        
        Projects_latex += rf"""
        \resumeProjectHeading
            {{\textbf{{{project_name}}} \textit{{| {tools}}}}}{{}}
        \resumeItemListStart"""
        
        for item in bullet_points:
            Projects_latex += rf"""\resumeItem{{{item}}}"""
            
        Projects_latex += r"""\resumeItemListEnd"""
        
    Projects_latex += r"""\resumeSubHeadingListEnd"""
    Projects_latex = Projects_latex.replace("%","\%")
    
    global CURRENT_RESUME_LATEX
    CURRENT_RESUME_LATEX += Projects_latex
    response_message = "Now call the skills tool"
    return response_message

@tool
def Education(education : List[dict]) -> str:
    """
    Generates an Education section for the candidate. It generates a string which will be processed in the further steps.

    Args:
        education (list of dict): A list where each dict contains:
            - Institute (required) (str): Name of the Institute.
            - place (required)(str): Location of the Institute.
            - period (required)(str): Education duration (e.g., "Jan 2020 - Dec 2022").
            - specialization (required) (str): Specialization of education (e.g., "Bachelors in computer science", "Intermediate", "High School")

    Returns:
        str: Instruction for the next steps
    """
    Education_latex = r"""
    
    \section{Education}
    \resumeSubHeadingListStart
    """
    for edu in education:
        institute_name = edu["Institute"]
        place = edu["place"]
        period = edu["period"]
        specialization = edu["specialization"]
        studies = rf"""
        \resumeSubheading
            {{{institute_name}}}{{{place}}}
            {{{specialization}}}{{{period}}}
        """
        Education_latex+=studies
    Education_latex = Education_latex.replace("%","\%")
    global CURRENT_RESUME_LATEX
    CURRENT_RESUME_LATEX += Education_latex
    response_message = "Now call the achievements tool"
    return response_message

@tool
def achievements(achievements : List[str]) -> str:
    """
    Generates an achievements section for the candidate's resume in LaTeX format.

    Args:
        achievements (List[str]): List of achievement strings to be included in the resume

    Returns:
        str: Instruction for the next steps
    """
    achievements_latex = r"""
    
    \section{Achievements}
    \resumeItemListStart"""

    for achievement in achievements:
        achievements_latex += rf"""
        \resumeItem{{{achievement}}}"""
        
    achievements_latex += r"""
    \resumeItemListEnd

    \end{document}
    """
    achievements_latex = achievements_latex.replace("%","\%")
    global CURRENT_RESUME_LATEX
    CURRENT_RESUME_LATEX += achievements_latex
    response_message = "Created a file in your pc"
    return response_message

@tool
def skills(Programming_languages : List[str], Technologies : List[str], other_skills: dict) -> str:
    """
    Generates an technical skills section for the candidate.It includes programming langugage the candidate is aware of, frameworks, developer tools, technologies. It generates a string which will be processed in the further steps.

    Args:
        Programming_languages (list of strings): contains a list of all the programming languages the candidate is aware of and the new job is expecting. (eg. Python,java,js, HTML, CSS)
        Technologies (list of strings): contains a list of all the technologies which are relevant to the Job description as well as the technologies which the candidate is aware of.
        other_skills (dict): Contains a list of keyworded arguments specifying more about the skills. Each key is the heading like ML Framworks, Developer tools,etc and the values are a list of strings containing the details. Here is an example (eg. kwargs = {"Frameworks": ["React", "Node.js", "Express.js", "UIKit", "SwiftUI", ".NET Core"],"ML Frameworks & tools":[ TensorFlow, PyTorch, Hugging Face, LangChain, Llama Index, JAX, ML Flow, Chroma DB, CrewAI, Numpy,Databricks, Pandas, Hadoop, Pyspark, scikit-learn]})
    Returns:
        str: Instruction for the next steps
    """

    skills_latex = r"""

    \section{Technical Skills}
    \begin{itemize}[leftmargin=0.15in, label={}]
        \small{\item{
            \textbf{Languages}{: """ + ", ".join(Programming_languages) + r"""} \\
            \textbf{Technologies}{: """ + ", ".join(Technologies) + r"""}
            """

    for category, items in other_skills.items():
        skills_latex += rf""" \\
            \textbf{{{category}}}{{{": " + ", ".join(items)}}}
            """

    skills_latex += r"""
        }}
    \end{itemize}
    """
    global CURRENT_RESUME_LATEX
    CURRENT_RESUME_LATEX += skills_latex
    response_message = "Now call the achievements_latex"
    return response_message

    
def create_resume_agent(prompt: str): 
    try:
        model = LiteLLMModel(model_id="gemini/gemini-2.0-flash-exp",
                        api_key=os.getenv("GOOGLE_API_KEY"))
        resume_agent =CodeAgent(
        tools = [header_details,professional_summary,professional_experience,projects,skills,Education,achievements],
        model = model
        )
        # print(resume_agent)
        resume_agent.run(prompt)
        global CURRENT_RESUME_LATEX
        # print(CURRENT_RESUME_LATEX)
        CURRENT_RESUME_LATEX = re.sub(r'\bextbf\s*{(.*?)}', r'\\textbf{\1}', CURRENT_RESUME_LATEX)
        return CURRENT_RESUME_LATEX
    except Exception as e:
        return e