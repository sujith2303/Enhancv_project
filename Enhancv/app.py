import gradio as gr
from pypdf import PdfReader
from resume_tools import create_resume_agent
import google.generativeai as genai
import os

def read_pdf_file(file_path):
    """
    Reads text content from a PDF file.

    Args:
        file_path (str): The path to the PDF file.

    Returns:
        str: The extracted text content from the PDF.
    """
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"  # Add newline between pages
        return text
    except Exception as e:
        return f"Error reading PDF file: {e}"



def verify_gemini_api_key(api_key):
    try:
        genai.configure(api_key=api_key)
        models = genai.list_models()
        for model in models:
            pass
        return True,""
    except Exception as e:
        if "API key not valid" in str(e) or "PERMISSION_DENIED" in str(e):
            return False,"Reason: The API key itself is likely incorrect or lacks necessary permissions."
        elif "FAILED_PRECONDITION" in str(e) and "free tier is not available" in str(e):
            return False,"Reason: Free tier might not be available in your region, or billing needs to be enabled."
        elif "RESOURCE_EXHAUSTED" in str(e):
            return  False,"Reason: Rate limit exceeded or quota exhausted for this API key."
        return False,""
    

def process_inputs(resume, job_description, custom_instructions,gemini_api_key):
    response,code = verify_gemini_api_key(gemini_api_key)
    if not response:
        return code
    os.environ["GOOGLE_API_KEY"] = gemini_api_key
    if resume is not None:
        resume = read_pdf_file(resume)
    else:
        return "Please enter a valid PDF File"
    prompt = f"""
    You are an expert Resume Optimization Agent specializing in creating concise, ATS-friendly, single-page resumes tailored strictly to a given Job Description (JD).
    
    Your task is to **align the candidate’s resume with the JD to achieve a high ATS (Applicant Tracking System) score**, while preserving the integrity of the original content.
    
    ---
    
    ###  **Mandatory Tool Usage Sequence:**
    
    1. header_details_tool
    2. professional_summary_tool
    3. Professional_experience
    4. Projects
    5. Skills
    6. Education
    7. Achievements
    
    Each tool must be called in this exact sequence.
    Each tool should return its respective section content, along with an instruction to proceed to the next tool.
    Never skip, combine, or reorder tools.
    
    ---
    
    ###  **Core Instructions:**
    
    1. **Resume Length & Structure:**
       - One page only.
       - Professional Summary: 2–3 lines — introduce tools, technologies, problem-solving ability (no numbers here).
       - Professional Experience: 4–6 bullets for recent role; older roles: 2–3 bullets. Follow Star methods while writing bullet points focussing on quantifying impacts.
       - Projects: Max 2 projects; 2–3 bullets each.
       - Bullet points ≤ 25 words, bullet points should not be very long and not exceed 2 lines.
       - Quantify things in bullet points especially for professional experience.
    
    2. **JD Alignment Rules:**
       - You are allowed to modify **20–30% of the content** of any bullet point to align with the JD.
       - Modifications may include changing keywords, replacing tools/tech names, adjusting domain-specific phrases — **without altering the fundamental meaning** of the original point.
       - Example:
         example 1:- Original: "Built ML models for recommendation systems."
         JD requires Generative AI → Acceptable change:
         "Built \\textbf{{LLMs}} for recommendation systems."
        example 2:- Original: " build applications using react"
        JD Requires Angular, Node JS -> Acceptable change:
        " build applications using Angular, NodeJS"
    
        - Also note when you apply above modifications, ensure that the bullet point has relevant meaning. If suppose the user mentioned some feature in react and you changed it from react to angular, ensure that the same feature is available in angular as well, else you will fail.
         Other example can be, user mentioned that he has utilized LangGraph and created Human-in-loop and now for instance if Job requires one who is good at smolagents framework, dont just change like created Human-in-loop using smolagents since smolagents don't have such feature.
        - So, change meaningfully.
    
    3. **STAR Format Enforcement:**
       - Ensure each bullet follows **Situation, Task, Action, Result (STAR)** format.
       - Include measurable impact wherever possible (time saved, accuracy improved, cost reduced, etc.).
       - While writing bullet points in experience section, try quantifying things.
    
    4. **Keyword Highlighting:**
       - Bold important technologies, tools, and results using: `\\textbf{{...}}` and use double backward slashes as shown.
       - Example:
         "Reduced training time by \\textbf{{40%}} using mixed-precision optimization."
    
    5. **Skills Section Handling:**
       - Include skills/tools from both the candidate’s background and JD — maximize overlap for ATS.
       - Add relevant frameworks (e.g., TensorFlow if PyTorch is mentioned).
       - Clearly organize for ATS readability.
       - As it is not possible to add every skill that user posses, try to add most of the skills from Job Description and few which are relavant. You can skip a few irrelavant skills that are not inline with JD. Maintain the balance, don't try to add a lot or dont try to skip a lot.
    
    6. **Strict Warnings (Must Follow):**
       - **20–30% change per bullet is allowed — not full rewrites.**
       - Never invent or fabricate achievements, titles, or skills not backed by the original resume.
       - Never change job titles.
       - Vary action verbs — do not reuse any verb (e.g., "developed") more than 3 times. Using so will result a very bad ATS score.
       - A good ATS resume will have 450-800 words.
       - If you want to bold something stricly use double slash not single slash i.e., \\textbf{{content to bold}} and not \textbf{{content to bold}}. The reason is that when we use single slash the program is changing it to tab space.
    
    ---
    
    ###  **ATS Score Motivation:**
    
     You are rewarded for producing a resume that:
     Strongly aligns with JD keywords and required skills,
     Maintains authenticity of original experience,
     Uses measurable impact statements,
     Strictly limits changes to 20–30% per bullet,
     Is ATS-optimized and one page.
    
    ---
    
    ###  **Input Provided:**
    
    ####  Job Description:
    {job_description}
    
    ####  Original Resume:
    {resume}
    
    ---
    
    #### User Custom Instructions:
    {custom_instructions}
    
    **Begin by invoking `header_details_tool` and proceed strictly as per tool order. Ensure JD alignment, STAR format, keyword emphasis, and 20–30% content change limit in every applicable section.**
    Do not generate final resume at once — output tool-wise only.
    """
    
    # print(prompt)
    return create_resume_agent(prompt)

    
custom_instructions_examples = (
    "Few Examples:\n\n"
    "Make a single or double paged resume\n"
    "I don't have projects to write so create some projects which matches Job description\n"
    "Align 100% with the Job description"
)


with gr.Blocks() as demo:
    gr.Markdown("# Enhancv")
    with gr.Row():
        with gr.Column():
            resume = gr.File(label="Upload Resume", file_types=[".pdf"])
            job_description = gr.Textbox(label="Paste Job Description here", lines=5)
            custom_instructions = gr.Textbox(label="Enter Your Instructions", lines=10,placeholder=custom_instructions_examples)
            gr.Markdown("Get your free API key: [Gemini API](https://aistudio.google.com/app/apikey)")
            gemini_api_key = gr.Textbox(label="Enter your Gemini API key..!!!", lines=1,placeholder="Dont worry we won't store your API key!!!")
            submit_btn = gr.Button("Submit")
        with gr.Column():
            output = gr.Textbox(label="LaTEX Resume File", lines=30)
            gr.Markdown("Paste your Latex File here to get your resume: [Overleaf](https://www.overleaf.com/)")
    submit_btn.click(
        fn=process_inputs,
        inputs=[resume, job_description,custom_instructions,gemini_api_key],
        outputs=output
    )

if __name__ =="__main__":
    demo.launch(debug= True)