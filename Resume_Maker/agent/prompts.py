MAX_ITERATIONS = 3
def resume_prompt(job_description: str, resume: str, custom_instructions: str, links: str) -> str:
    prompt = f"""
You are an expert Resume Optimization Agent specializing in creating concise, ATS-friendly, single-page resumes tailored strictly to a given Job Description (JD).

Your task is to **align the candidate’s resume with the JD to achieve a high ATS (Applicant Tracking System) score**, while preserving the integrity of the original content.

---

###  **Core Instructions:**

1. **Resume Length & Structure:**
- One page only.
- Professional Summary: 3 lines — introduce tools, technologies, problem-solving ability (no numbers here).
- Professional Experience: 4–6 bullets for recent role; older roles: 2–3 bullets. Follow Star methods while writing bullet points focussing on quantifying impacts.
- Projects: Max 2 projects; 2–3 bullets each.
- Bullet points ≤ 25 words, bullet points should not be very long and not exceed 2 lines.
- Quantify things in bullet points especially for professional experience.

2. **JD Alignment Rules:**
- You are allowed to modify **0-80% of the content** of any bullet point to align with the JD.
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
links to profiles : {links}
---

#### User Custom Instructions:
{custom_instructions}

---
Now begin by following above rules strictly.
"""
    return prompt



def resume_prompt_1(job_description: str, resume: str, custom_instructions: str, links: str) -> str:
  prompt = f'''
# **Role:**

You are an **ATS Resume Optimization Agent**.
Your responsibility is to transform the candidate’s resume into a **concise, ATS-friendly, one-page resume** that is tightly aligned with the given Job Description (JD), while preserving authenticity of the candidate’s experience.

---

## **Rules & Constraints**

### 1. Resume Length & Structure

* **One page only**.
* **Professional Summary:** Exactly 3 lines. Introduce candidate’s tools, technologies, and problem-solving ability.

  * No numbers or percentages here.
* **Professional Experience:**

  * Most recent role → 4–6 bullet points.
  * Older roles → 2–3 bullet points.
  * Each bullet ≤ 25 words, ≤ 2 lines.
  * Use **STAR method (Situation, Task, Action, Result)** and quantify outcomes (e.g., time saved, accuracy improved, cost reduced).
* **Projects:** Max 2 projects, 2–3 bullets each.
* **Education, Certifications, Skills:** Keep concise.

---

### 2. JD Alignment

* Modify **0–80% of the content** in any bullet to align with JD.
* Allowed edits:

  * Replace tools/technologies with JD-relevant ones.
  * Adjust phrasing to include domain-specific keywords.
* **Do not fabricate**: Never invent skills, achievements, or titles absent from the original resume.
* Ensure modifications are **meaningful and realistic**.

  * Example: If React → Angular is substituted, ensure the described feature actually exists in Angular.
* Balance: Maintain **authenticity** + **ATS keyword alignment**.

---

### 3. Bullet Point Rules

* Each bullet point must:

  * Follow STAR format.
  * Contain measurable outcomes (\textbf{{%}}, \textbf{{time saved}}, \textbf{{cost reduced}}, etc.).
  * Be rewritten with **20–30% change only** (not a full rewrite).
  * Use varied action verbs (don’t repeat any verb more than 3 times).

---

### 4. Formatting Rules

* Highlight all important **technologies, tools, and results** with:
  `\\textbf{{...}}` (strictly double backslashes, not single).
* Resume should be **450–800 words**.
* Must fit on a **single page**.

---

### 5. Skills Section

* Include:

  * Candidate’s skills that overlap with JD.
  * Add relevant JD keywords/frameworks for ATS alignment.
* Avoid clutter:

  * Do not include every skill from the candidate; select those most relevant.
  * Maintain balance between **JD match** and **candidate authenticity**.

---

### 6. Strict Warnings

* Never fabricate achievements, skills, or titles.
* Never exceed 2 lines per bullet.
* Never reuse the same action verb more than 3 times.
* Do not produce a resume longer than one page.

---

## **Inputs**

* **Job Description (JD):**
  {job_description}

* **Original Resume:**
  {resume}

* **Profile Links:**
  {links}

* **User Custom Instructions:**
  {custom_instructions}

---

## **Task**

Using the above rules, **rewrite the candidate’s resume** so that it:

* Strongly aligns with the JD,
* Scores highly in ATS parsing,
* Preserves the candidate’s authentic experience,
* Is concise, quantified, and keyword-rich.
---
Begin now.
'''
  return prompt


def job_description_summary_prompt(job_description: str) -> str:
  if not job_description:
      return ""
  prompt = f""" You are an expert career coach specializing in crafting concise summaries of job descriptions for resume tailoring. Here is the job description:
{job_description}
Your task is to generate a brief summary (max 5 lines) that captures the key skills, technologies, and qualifications required for the role. Focus on the most important aspects that a candidate should highlight in their resume to align with this job description. Avoid including any extraneous details or company-specific information. The summary should be clear, concise, and directly relevant to the job requirements.
"""
  return prompt

def custom_instructions_eloboration_prompt(custom_instructions: str) -> str:
  if not custom_instructions:
      return ""
  prompt = f""" You are an expert career coach specializing in resume optimization. Here are the user's custom instructions for tailoring their resume:
{custom_instructions}
Your task is to elaborate on these instructions to provide clear, actionable guidance for enhancing the resume. Expand on the key points, suggest specific strategies for improvement, and highlight any important considerations the user should keep in mind while updating their resume. The elaboration should be detailed enough to help the user effectively implement their custom instructions.
"""    
  return prompt


BASE_LATEX = r"""
%-------------------------
% Resume in Latex
% Author : Sujith
% Based off of: https://github.com/sb2nov/resume
% License : MIT
%------------------------

\documentclass[letterpaper,11pt]{article}

\usepackage{latexsym}
\usepackage[empty]{fullpage}
\usepackage{titlesec}
\usepackage{marvosym}
\usepackage[usenames,dvipsnames]{color}
\usepackage{verbatim}
\usepackage{enumitem}
\usepackage[hidelinks]{hyperref}
\usepackage{fancyhdr}
\usepackage[english]{babel}
\usepackage{tabularx}
\input{glyphtounicode}


%----------FONT OPTIONS----------
% sans-serif
% \usepackage[sfdefault]{FiraSans}
% \usepackage[sfdefault]{roboto}
% \usepackage[sfdefault]{noto-sans}
% \usepackage[default]{sourcesanspro}

% serif
% \usepackage{CormorantGaramond}
% \usepackage{charter}


\pagestyle{fancy}
\fancyhf{} % clear all header and footer fields
\fancyfoot{}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}

% Adjust margins
\addtolength{\oddsidemargin}{-0.5in}
\addtolength{\evensidemargin}{-0.5in}
\addtolength{\textwidth}{1in}
\addtolength{\topmargin}{-.5in}
\addtolength{\textheight}{1.0in}

\urlstyle{same}

\raggedbottom
\raggedright
\setlength{\tabcolsep}{0in}

% Sections formatting
\titleformat{\section}{
  \vspace{-4pt}\scshape\raggedright\large
}{}{0em}{}[\color{black}\titlerule \vspace{-5pt}]

% Ensure that generate pdf is machine readable/ATS parsable
\pdfgentounicode=1

%-------------------------
% Custom commands
\newcommand{\resumeItem}[1]{
  \item\small{
    {#1 \vspace{-2pt}}
  }
}

\newcommand{\resumeSubheading}[4]{
  \vspace{-2pt}\item
    \begin{tabular*}{0.97\textwidth}[t]{l@{\extracolsep{\fill}}r}
      \textbf{#1} & #2 \\
      \textit{\small#3} & \textit{\small #4} \\
    \end{tabular*}\vspace{-7pt}
}

\newcommand{\resumeSubSubheading}[2]{
    \item
    \begin{tabular*}{0.97\textwidth}{l@{\extracolsep{\fill}}r}
      \textit{\small#1} & \textit{\small #2} \\
    \end{tabular*}\vspace{-7pt}
}

\newcommand{\resumeProjectHeading}[2]{
    \item
    \begin{tabular*}{0.97\textwidth}{l@{\extracolsep{\fill}}r}
      \small#1 & #2 \\
    \end{tabular*}\vspace{-7pt}
}

\newcommand{\resumeSubItem}[1]{\resumeItem{#1}\vspace{-4pt}}

\renewcommand\labelitemii{$\vcenter{\hbox{\tiny$\bullet$}}$}

\newcommand{\resumeSubHeadingListStart}{\begin{itemize}[leftmargin=0.15in, label={}]}
\newcommand{\resumeSubHeadingListEnd}{\end{itemize}}
\newcommand{\resumeItemListStart}{\begin{itemize}}
\newcommand{\resumeItemListEnd}{\end{itemize}\vspace{-5pt}}

%-------------------------------------------
%%%%%%  RESUME STARTS HERE  %%%%%%%%%%%%%%%%%%%%%%%%%%%%

\begin{document}


"""