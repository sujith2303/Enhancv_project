from typing import List,Optional
from prompts import BASE_LATEX
from langchain_core.tools import tool
from langgraph.types import Command, interrupt




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
    header_latex = header_latex.replace("%","\%")
    return header_latex



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
    return summary_latex


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
        place   = exp['location']
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
    return Experience_latex



def Projects(projects: List[dict]) -> str :
    """
    Creates an projects section for a user. Processes the projects and generates a string in latex form which will be used in further steps

    Args:
        projects (list of dict): A list where each dict contains:
            - project_name (required) (str): Name of the project.
            - tools_used (required)(list[str]): Tools and technologies used in the project (eg Python, Flask, React, PostgreSQL, Docker). It is a list of strings.
            - period (required)(str): Employment duration (e.g., "Jan 2020 - Dec 2022").
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
    

    return Projects_latex


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
        place = edu["location"]
        period = edu["period"]
        specialization = edu["specialization"]
        studies = rf"""
        \resumeSubheading
            {{{institute_name}}}{{{place}}}
            {{{specialization}}}{{{period}}}
        """
        Education_latex+=studies
    Education_latex = Education_latex.replace("%","\%")
    return Education_latex


def Achievements(achievements : List[str]) -> str:
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

    """
    achievements_latex = achievements_latex.replace("%","\%")
    return achievements_latex


def Skills(Programming_languages : List[str], Technologies : List[str], frameworks: Optional[List[str]], tools : Optional[List[str]]) -> str:
    """
    Generates an technical skills section for the candidate.It includes programming langugage the candidate is aware of, frameworks, developer tools, technologies. It generates a string which will be processed in the further steps.

    Args:
        Programming_languages (list of strings): contains a list of all the programming languages the candidate is aware of and the new job is expecting. (eg. Python,java,js, HTML, CSS)
        Technologies (list of strings): contains a list of all the technologies which are relevant to the Job description as well as the technologies which the candidate is aware of.
        frameworks (list of strings): list of all frameworks the candidate knows and the job is expecting
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
    if len(frameworks):
        skills_latex+= r"""\textbf{Frameworks}""" + ", ".join(frameworks)
    if len(tools):
        skills_latex+= r"""\textbf{Tools}""" + ", ".join(tools)

    skills_latex += r"""
        }}
    \end{itemize}
    """
    return skills_latex

@tool
def human_assistance(query: str) -> str:
    """Use this tool when you require information from the user about their resume, like more details about their experience, education, or skills."""
    human_response = interrupt({"query": query})
    return human_response["data"]
    
def create_resume(**kwargs):
    latex = BASE_LATEX 
    latex+=header_details(
        name=kwargs["header"]['name'],
        email_id=kwargs["header"]['email_id'],
        linkedin_profile_link=  kwargs["header"]['linkedin_profile_link'],
        github_link=kwargs["header"]['github_link'],
        mobile_number=kwargs["header"]['mobile_number']
        )
    
    latex += professional_summary(summary=kwargs["professional_summary"]["summary"])
    if kwargs.get("professional_experience") and len(kwargs["professional_experience"])>0:
        latex += professional_experience(experiences = kwargs["professional_experience"])
    
    if kwargs.get("projects") and len(kwargs["projects"])>0:
        latex += Projects(kwargs["projects"])
    
    if kwargs.get("skills") and len(kwargs["skills"])>0:
        latex+= Skills(Programming_languages=kwargs["skills"]["programming_languages"],
                    Technologies= kwargs["skills"]["technologies"],
                    frameworks = kwargs["skills"]["frameworks"],
                    tools = kwargs["skills"]["tools"]
                    )
    if kwargs.get("education") and len(kwargs["education"])>0:
        latex+= Education(kwargs["education"])
    if kwargs.get("achievements") and len(kwargs["achievements"])>0:
        latex+= Achievements(kwargs["achievements"])

    # latex = latex.replace("%","\%")
    # ## remove ** bold ** and replace with \textbf{}
    # latex = re.sub(r"\*\*(.*?)\*\*", r"\\textbf{\1}", latex)
    # ## remove * italics * and replace with \textit{}
    # latex = re.sub(r"\*(.*?)\*", r"\\textit{\1}", latex)
    return latex + "\n  \end{document}\n"



if __name__ == "__main__":
    d = {   
            "name":'Rohith Anumala', 
            "mobile_number":'+1(602)-566-2762', 
            "email_id":'ranumala@asu.edu', 
            "linkedin_profile_link":'', 
            "github_link":'https://github.com/RohithAnumala' ,
            "professional_summary":"summary"
        }
    resume = create_resume(**d)

    with open('resume.tex','w') as f:
        f.write(resume)