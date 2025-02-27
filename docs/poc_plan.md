
## 1. Project Overview
- **Project Name:** Agentic Framework for AI Agents on Medical Decision Support System 
- **Duration:** Mar. 1 - Apr. 17
- **Resources:** 
    - **Core Team:** Daphna, Zoran, Francesco and myself, 4 headcounts. but 3 members full-time on an average basis (sometimes less than 3 sometimes more than 3 for the next few weeks due to vacations etc.), but the personals should be 100% on this project and not splitting time into other projects on their discretion. full authority to lead.
    - **Liaising Team:** Claudio that to provide curated data source and science support; Melisa that could do some ad-hoc tools and market research
    - **Tools:** GitHub, Cursor, Notion, Different LLM and where to sort them in.
    - **Liaising Tech Support:** 25% of GYZ

## 2. Approach Statement
- **Characteristics:** 
    - **Traceability:** Unclear, but we will keep it in mind. should be a toggle on toggle off possibility
    - **Granularity:** Ideally it should be customized to GP's different needs, but for now, it should be one size fits all (we will try to aligh to the Gold Standard)
    - **Personalization:** Currently we will not build anything in addition to this aspect, outside of the KG and LLM own capability. 
    - **Scalability:** Moduralized, friendly to add and modify agents and even crews
    - **Accuracy, Stability:** It will be less deterministic, but we will aim for a better accuracy and stability when possible.
    - **Longevity-biased:** Unclear, i think we should have curated data sources to reflect longevity aspect. 
- **Input:** Patient profile in PDF/txt/md format, questionnaire (optional). No OCR, no picture.
- **Output:** 2 categories as otuputs for poc: 1. supplements/nutrition; 2. one extra category. We are not building a front-end for the poc.
- **Process:** 
    - to start with, we need a crew of input parser; 
    - then we need a crew of diagnostics; 
    - then we need a crew of supplements; 
    - then we need a crew of nutrition; 
    - then we need a crew of output formatter; 
    - other parts to power the agents include: tools, knowledge, logger and memory system, and ideally we want to have a simple evaluation framwork already in place.

## 3. Data Requirements
- **Data Sources:** (format PDF/txt/md)
    - **Papers:** As well as use Graph; Curated papers from either the pmc database (in this case, you can get html) or general medical papers (we can deal with the pdf)
    - **Books:** Curated books from the internet
    - **Medical Guidelines:** Curated medical guidelines (need to specify what kind of guidelines, e.g., guidelines of nutrition specifically, or guidelines of everything.)
    - **DrugBank, EPA, etc:** Use what we have in-house
    - **Other:** nothing for poc.

## 4. Communications and Feedbacks
- **Feedback:** 
    - We should have a running simple front-end to allow pdf upload and the recommendation output. 
    - Feedback is invited, please write me in email, title: "Feedback for AgenticPOC", and then itemize your issues or feedbacks. 
    - We will aim for a weekly new version release.

## 5. Task-to-be-deligated
- **Gold Standard:** minimal 10, separate by profile.md and recommendation.md. Clearly referenced to match a profile with a recommendation. Itemize the recommendation.
- **Curated Paper:** PDF/txt/md
- **Curated Books:** PDF/txt/md
- **Curated Medical Guidelines** PDF/txt/md and their strucutre description.
 
High quality, no OCR needed! Please send to me in one-go that includes all curateed paper PDFs/all curated books PDFs/...

Please give PDFs that has the right reference. And in the email attach a bibliography that also can be easily traced to the PDF attached. 

e.g.,
bibliography

{

    article_name_a, author, jounal, year (following AMA or something) | name_of_pdf.pdf
    article_name_b, author, jounal, year (following AMA or something) | name_of_pdf.pdf

}

If it remains unclear, let me know. 


## 6. Time-table
- **Mar. 3 - Mar. 10:**: 1p (me), goal is to laydown all function blocks in rough
- weeks coming is to be defined.