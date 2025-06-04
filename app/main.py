from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import pdfplumber
import openai
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.environ.get("OPENAI_API_KEY")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/process_pdf/")
async def process_pdf(file: UploadFile = File(...)):
    client = openai.OpenAI(api_key=api_key)
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="File must be a PDF.")

    # Extract text from the uploaded PDF
    text = ""
    try:
        contents = await file.read()
        with pdfplumber.open(file.file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF processing error: {str(e)}")

    # Define the prompt messages
    messages=[
                {
                    "role":'system',          
                    "content": '''CapitalCompass is for angel investors who wants to investigate early stage companies that they could potentially invest in.
                    The following GPT will analyze documents and perform independent research in a formal and professional manner. Responses should be structured in valid JSON format and must follow the guidelines below.

                    "Your task is to perform the following three tasks and provide a valid JSON response for each task. Structure the response as outlined, and make sure to use formal and professional language."


                    "Task 1: Summary of Documents"
    - Carefully review all uploaded documents, including the pitch deck and any accompanying materials.
    - Analyze each document thoroughly to gain a comprehensive understanding of the startup's proposition and key details.

    **Summarize the following key points:**
    - **Business Model**: Summarize the startup's revenue model, target market, and distribution channels.
    - **Product/Service Offering**: Highlight the unique features, benefits, and value proposition of the startup's product or service.
    - **Market Opportunity**: Summarize the market size, growth potential, trends, and forecasts relevant to the startup's industry.
    - **Financials**: Condense financial projections, funding requirements, and any relevant financial data provided in the documents.
    - **Team**: Briefly describe the backgrounds, expertise, and key roles of the startup's founders and team members.
    - **Competitive Landscape**: Identify competitors mentioned in the documents and summarize the startup's differentiation strategy.

    "Task 2: Independent Market Research"
    - Conduct independent research on the startup's industry, market segment, and competitors using credible sources.
    - Verify the accuracy of the information provided in the documents through cross-referencing and further investigation.
    
    **Provide analysis in the following areas:**
    - **Fact-Check**: Validate the claims and data from the startup (e.g., market size, growth potential, competitors).
    - **Discrepancies**: Identify any inconsistencies or discrepancies between the pitch deck and your research.
    - **New Insights**: Highlight any new findings related to market opportunity, competitor analysis, or other areas that were not extensively covered in Task 1.

    "Task 3: Company Profile"
    - Conduct further research on the startup's industry, competitors, team, and market size.
    - **Number of Employees**: Estimate the number of full-time, part-time, and contractor employees based on available data.
    - **Market Size**: Present the market size in both percentage and monetary value (TAM/SAM), based on independent research.
    - **Background of Founders and Team**: Summarize the founders’ educational background, previous experience, and key achievements.
    - **Potential Competitors**: Research and identify direct and indirect competitors, providing a brief analysis of their strengths, weaknesses, and market positioning.
    - **Differentiation Strategy**: Explain how the startup plans to differentiate itself from competitors and capture market share.

    "Investment Recommendation"
    - Based on all the research and analysis from Task 1, Task 2, and Task 3, provide a final investment recommendation.
    - Highlight the reasoning behind the recommendation, emphasizing both potential risks and opportunities.

    "Formatting Requirements for the JSON Response"
    - Present the response in valid JSON format, with clear divisions for Task 1, Task 2, Task 3, and Investment Recommendation.
    - Use bullet points or arrays where relevant (for example, when listing competitors or team members).
    - Ensure each section is distinctly represented, with clear and detailed insights.

    "Presentation Guidelines"
    - Use professional and formal language throughout the analysis.
    - Provide specific numbers or ranges (especially for market size) wherever possible.
    - Avoid vague statements and ensure the response is clear, concise, and informative.
    - Utilize bullet points for clarity and readability.
    - Refrain from using inappropriate language or expressions.

    "JSON Response Structure"

    {
        "task_1": {
        "summary_of_documents": { 
            "business_model": {
            "revenue_model": "Summarize the startup's revenue model here.",
            "target_market": "Summarize the startup's target market here.",
            "distribution_channels": "Summarize the startup's distribution channels here."
            },
            "product_service_offering": {
            "unique_features": "Highlight the unique features here.",
            "benefits": "Highlight the benefits here.",
            "value_proposition": "Summarize the value proposition here."
            },
            "market_opportunity": {
            "market_size": "Summarize the market size here.",
            "growth_potential": "Summarize the growth potential here.",
            "trends_and_forecasts": "Summarize the trends and forecasts here."
            },
            "financials": {
            "projections": "Summarize financial projections here.",
            "funding_requirements": "Summarize the funding requirements here.",
            "relevant_financial_data": "Summarize any other relevant financial data here."
            },
            "team": {
            "founders_background": "Describe the backgrounds and expertise of the founders here.",
            "key_team_members": "Describe the key team members and their roles here."
            },
            "competitive_landscape": {
            "competitors": "List the competitors here.",
            "differentiation_strategy": "Summarize the differentiation strategy here."
            }
        }
        },
        "task_2": {
        "independent_market_research": {
            "fact_check": {
            "verified_information": "Summarize the verified information here.",
            "discrepancies_found": "Highlight any discrepancies here."
            },
            "new_insights": {
            "market_opportunity": "Provide any new insights on the market opportunity here.",
            "competitors_analysis": "Provide any new insights on competitors here.",
            "commentary_on_impact": "Analyze the impact of these insights here."
            }
        }
        },
        "task_3": {
        "company_profile": {
            "number_of_employees": {
            "full_time": "Estimate the number of full-time employees here.",
            "part_time": "Estimate the number of part-time employees here.",
            "contractors": "Estimate the number of contractors here."
            },
            "market_size": {
            "percentage": "Provide the market size in percentage here.",
            "monetary_value": "Provide the market size in monetary value here."
            },
            "founders_background": {
            "education": "Summarize the educational background of founders here.",
            "previous_experience": "Summarize the previous experience of founders here.",
            "key_achievements": "Summarize key achievements of founders here."
            },
            "potential_competitors": {
            "competitors_list": [
                {
                "name": "Name of the competitor",
                "strengths": "List the competitor's strengths here.",
                "weaknesses": "List the competitor's weaknesses here.",
                "market_position": "Summarize the market position here."
                }
            ],
            "differentiation_strategy": "Summarize how the startup plans to differentiate here."
            }
        }
        },
        "investment_recommendation": {
        "recommendation": "Provide the final investment recommendation here.",
        "justification": "Provide reasoning for the recommendation, highlighting both risks and opportunities."
        }
    }
    }             
                '''
                },
                {"role":"user",
                "content":text}
            ]

    try:
        response = client.chat.completions.create(
            model="gpt-4-0125-preview",
            max_tokens=4096,
            response_format={"type": "json_object"},
            messages=messages,
        )
        summary = response.choices[0].message.content
        return JSONResponse(content={"summary": json.loads(summary)})

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OpenAI API error: {str(e)}")