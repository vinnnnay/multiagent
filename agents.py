from langgraph.prebuilt import create_react_agent
from langchain.chat_models import init_chat_model
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search , scrape_url
from dotenv import load_dotenv
import os

load_dotenv()

# model setup

def get_llm():
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    openai_api_key = os.getenv("OPENAI_API_KEY")

    if gemini_api_key:
        model_name = os.getenv("GEMINI_MODEL_NAME", "gemini-2.5-flash")
        try:
            return init_chat_model(
                model=model_name,
                model_provider="google_genai",
                api_key=gemini_api_key,
            )
        except Exception as exc:
            raise EnvironmentError(
                f"Failed to initialize Gemini model '{model_name}'. "
                "Set GEMINI_MODEL_NAME to a supported model, or use OPENAI_API_KEY instead."
            ) from exc

    if openai_api_key:
        return ChatOpenAI(
            model="gpt-4o-mini",
            api_key=openai_api_key,
        )

    raise EnvironmentError(
        "No GEMINI_API_KEY or OPENAI_API_KEY is configured. Set one in your environment or in a .env file."
    )


# 1st agent

def build_search_agent():
    return create_react_agent(
        model=get_llm(),
        tools=[web_search]
    )


# 2nd agent

def build_reader_agent():
    return create_react_agent(
        model=get_llm(),
        tools=[scrape_url]
    )


# writer chain

writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert research writer. Write clear, structured and insightful reports."),
    ("human", """Write a detailed research report on the topic below.

Topic: {topic}

Research Gathered:
{research}

Structure the report as:
- Introduction
- Key Findings (minimum 3 well-explained points)
- Conclusion
- Sources (list all URLs found in the research)

Be detailed, factual and professional."""),
])

def build_writer_chain():
    return writer_prompt | get_llm() | StrOutputParser()


# critic chain

critic_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a sharp and constructive research critic. Be honest and specific."),
    ("human", """Review the research report below and evaluate it strictly.

Report:
{report}

Respond in this exact format:

Score: X/10

Strengths:
- ...
- ...

Areas to Improve:
- ...
- ...

One line verdict:
..."""),
])

def build_critic_chain():
    return critic_prompt | get_llm() | StrOutputParser()


# Export chain instances
writer_chain = build_writer_chain()
critic_chain = build_critic_chain()
