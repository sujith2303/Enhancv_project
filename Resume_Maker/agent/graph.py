from langchain_groq import ChatGroq
from dotenv import load_dotenv
from helper import *
from states import *
from langchain_google_genai import ChatGoogleGenerativeAI
from prompts import resume_prompt, resume_prompt_1, job_description_summary_prompt, custom_instructions_eloboration_prompt, MAX_ITERATIONS
from tools import create_resume, human_assistance
from langgraph.graph import StateGraph,START, END

_ = load_dotenv()


llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
# llm = ChatGroq(model="openai/gpt-oss-120b")

## Nodes

def prompt_summarizer(state : GraphState) -> GraphState:
    job_description = state["job_description"]
    custom_instructions = state['custom_instructions']
    if job_description!="":
        job_description = job_description_summary_prompt(job_description)
        job_description = llm.invoke(job_description)
    
    if custom_instructions!="":
        custom_instructions = custom_instructions_eloboration_prompt(custom_instructions)
        custom_instructions = llm.invoke(custom_instructions)
    return {"job_description": job_description,
            "custom_instructions": custom_instructions}


def quickresume(state : GraphState) -> GraphState:
    prompt = resume_prompt_1(
        resume= state.get("resume"),
        job_description=state.get("job_description",""),
        custom_instructions=state.get("custom_instructions"),
        links =state.get("links")
        )
    state['max_iters'] = state.get("max_iters",0)+1
    response =  llm.with_structured_output(QuickResume).invoke(prompt)
    if state["status"]=="DONE" or state["max_iters"]>MAX_ITERATIONS:
        resume = create_resume(**response.model_dump())
        return {"LaTeX":resume}
    return {"LaTeX": response}


def HumanAssistance(state : GraphState) -> GraphState:
    response = state["LaTeX"]
    ### Check for None outputs and add them in prompt

    tools = [human_assistance]
    llm_with_tools = llm.bind_tools(tools)
    
    prompt = ("You are an expert in taking human assistance and convert them into a proper feedback. Based on the user's ",
              "response change the status to either DONE or INPROGRESS. Here are the details you can fetch from user",
              "")
    
    message = llm_with_tools.with_structured_output(HumanFeedback).invoke(prompt)
    

## Start the Graph 

graph_builder = StateGraph(GraphState)


graph_builder.add_node("quickresume", quickresume)
graph_builder.add_node("prompt_summarizer", prompt_summarizer)

graph_builder.add_edge("prompt_summarizer","quickresume")
graph_builder.set_entry_point("prompt_summarizer")


graph = graph_builder.compile()

if __name__=="__main__":

    resume_path = r"C:\Users\Sujith\Downloads\Enhancv_project\Lavanya_Resume.pdf"
    resume = read_pdf_file(resume_path)
    links = extract_hyperlinks_from_pdf(resume_path)



    job_description = """Lead the design and architecture of Agentic AI solutions, including agent reasoning, memory, and orchestration pipelines.
    Own end-to-end solution delivery design, development, optimization, and deployment of AI/ML systems ensuring scalability, reliability, and performance.
    Build and refine AI applications using modern frameworks (LangChain, LangGraph, OpenAI/Anthropic SDKs/APIs), with strong focus on prompt engineering and pipeline optimization.
    Provide technical leadership mentor engineers, review code, set best practices, and foster a culture of innovation and collaboration.
    Work closely with data scientists, product managers, Architectes and leadership to translate business requirements into technical solutions with measurable impact.
    Stay at the forefront of emerging LLM/Agentic AI advancements, integrating new techniques into the platform.
    Publish and share insights (internally and externally) through blogs, presentations, or papers to advance thought leadership in LLM and Agentic AI.
    Qualifications
    To be successful in this role, you have

    Experience with methods of training and fine-tuning large language models, such as distillation, supervised fine-tuning, and policy optimization
    Experience in using AI Productivity tools such as Cursor, Windsurf, etc. is a plus or nice to have
    2+ years of experience designing and implementing complex enterprise applications, with proven success in conversational AI and NLP platforms.
    Experience developing LLM-based features. Experience in prompt engineering is a plus or nice to have.
    Strong development skills in Java and Python (production-grade AI systems).
    Expertise in LLM powered applications, including LangChain, LangGraph, and OpenAI/Anthropic APIs.
    Deep understanding of Agentic reasoning pipelines, evaluation frameworks, and advanced NLP techniques.
    Strong problem solving abilities with a bias for action, customer first mindset, and ability to work in fast paced environments.
    Analytical expertise in evaluating model performance, optimizing inference costs, and improving system efficiency.
    Proven ability to translate complex AI concepts into business value and communicate effectively with technical and non-technical stakeholders.
    Experience providing technical leadership and guiding successful AI/ML engineering projects.
    Bonus: Publications, technical blogs, or open-source contributions in LLM/AI."""

    custom_instructions = ""

    response = graph.invoke({
        "resume":resume,
        "job_description": job_description,
        "custom_instructions":custom_instructions,
        "links": links}, 
        debug = True
        )
    
    print(response.get("LaTeX",""))
    # job_description = job_description_summary_prompt(job_description=job_description)
    # custom_instructions = custom_instructions_eloboration_prompt(custom_instructions=custom_instructions)

    # prompt = resume_prompt_1(
    #         job_description=job_description, 
    #         resume=resume,
    #         custom_instructions=custom_instructions,
    #         links=links
    #         )

    # # print(prompt)
    # response =  llm.with_structured_output(QuickResume).invoke(prompt)


    # resume = create_resume(**response.model_dump())

    # print(resume)


    # with open("resume.txt","w",encoding="utf-8") as f:
    #     f.write(resume)