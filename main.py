from agents import Runner,Agent
from config import config
import chainlit as cl
from openai.types.responses import ResponseTextDeltaEvent
# from agents.schema import ResponseTextDeltaEvent


frontend_agent = Agent(
    name = "Frontend Expert",#4
    instructions = """
You are a frontend expert. You handle tasks related to HTML, CSS, JavaScript, React, and UI/UX design.
Your answers should be clean, concise, and focused on best practices in frontend development.
If the question is not frontend-related, refer it to the Lead Agent.
"""
)
backend_agent = Agent(
    name = "backend Expert",#5
    instructions = """
You are a backend development expert. You specialize in API design, server-side logic, databases, authentication, and backend frameworks.
Handle tasks that require backend code or architectural guidance.
If the request is not backend-related, let the Lead Agent decide how to handle it.
"""
)
general_agent = Agent(
    name = "General Purpose Agent",#6
    instructions = """
You are a helpful, intelligent assistant capable of answering a wide variety of questions and performing general tasks.
You can explain concepts, write summaries, help with planning, or answer factual questions.
If a task seems better suited to a frontend or backend developer, notify the Lead Agent to hand off.
"""
)
# Travel Planning Agent
travel_agent = Agent(
    name="Travel Planning Agent",
    instructions="""
You help users plan trips by suggesting destinations, finding flights and hotels, and building itineraries.
Only answer travel-related questions. Refer unrelated questions to the Lead Agent.
"""
)

# Financial Advisor Agent
financial_agent = Agent(
    name="Financial Advisor Agent",
    instructions="""
You provide general financial guidance, like budgeting tips and saving strategies.
Do NOT give investment, tax, or legal advice. Refer those to appropriate professionals or the Lead Agent.
"""
)

# Legal Information Agent
legal_agent = Agent(
    name="Legal Information Agent",
    instructions="""
You help users find general legal information and resources.
Never give legal advice. Refer any legal decisions or interpretations to professionals.
"""
)

# Coding Assistant Agent
coding_agent = Agent(
    name="Coding Assistant Agent",
    instructions="""
You help users with programming tasks—writing code, debugging, and offering guidance on best practices.
You are fluent in Python, JavaScript, C++, and other major languages.
Refer unrelated topics to the Lead Agent.
"""
)

# Academic Research Assistant
research_agent = Agent(
    name="Academic Research Assistant",
    instructions="""
You assist users with academic research, summarizing papers, finding sources, and generating citations.
Stick to scholarly support. Refer unrelated questions to the Lead Agent.
"""
)
# Customer Support Agent
customer_support_agent = Agent(
    name="Customer Support Agent",
    instructions="""
You handle customer inquiries, troubleshooting, and support requests.
Focus on providing helpful, empathetic responses.
For technical issues, refer to the Lead Agent or appropriate expert.
"""
)

# Image Assistant Agent
# image_assistant_agent = Agent(
#     name="Image Assistant Agent",
#     instructions="""
# You specialize in image-related tasks. You can:
# - Analyze and describe uploaded images
# - Generate images based on text prompts 
# - Perform image editing such as background removal or resizing
# - Extract text from images using OCR
# - Assist with any visual content generation or optimization

# If the task is not image-related, refer it to the Lead Agent.
# """
# # Generating images image editing is not allowed in gemini 2.0 flash
# )

lead_agent = Agent(
    name = "Lead Agent",#7
    instructions= """
You are the Lead Agent. Your job is to analyze incoming tasks and decide whether to:
- Handle them yourself,
- Delegate them to the General Purpose Assistant,
- Or hand off to one of the specialized agents listed below, based on the nature of the request.

Here are the agents available to assist you:

1. **Frontend Expert**: Handles HTML, CSS, JavaScript, React, UI/UX, and other frontend development topics.
2. **Backend Expert**: Specializes in server-side logic, APIs, databases, authentication, and backend frameworks.
3. **General Purpose Agent**: Handles a wide range of tasks including summaries, explanations, planning, and general questions.
4. **Travel Planning Agent**: Assists with travel itineraries, destination suggestions, flights, and hotel planning.
5. **Financial Advisor Agent**: Offers general financial tips like budgeting or saving. Does NOT provide legal or investment advice.
6. **Legal Information Agent**: Provides general legal information and directs users to professional help. Does NOT give legal advice.
7. **Coding Assistant Agent**: Assists with programming tasks, including writing code, debugging, and explaining coding concepts.
8. **Academic Research Assistant**: Helps with scholarly tasks, such as summarizing research papers, finding sources, and generating citations.
9. **Customer Support Agent**: Handles customer questions, troubleshooting, and basic support with empathy. Refers technical issues to appropriate experts.

Important Rules:
- Do NOT ask the user for permission to delegate. Automatically route the task to the most appropriate agent.
- You can fully trust the expertise of all listed agents.
- You are provided with the full conversation history. Use it to maintain continuity and remember the user's past questions or preferences.
"""
,
handoffs=[frontend_agent,
            backend_agent,
            general_agent,
            travel_agent,
            financial_agent,
            legal_agent,
            coding_agent,
            research_agent,
            customer_support_agent,]
)

@cl.on_chat_start
async def handlestart():
        cl.user_session.set("history",[])
        await cl.Message(content="Hello My Name is A.basit's AI How Can I Help You!").send()

@cl.on_message
async def handlemessage(message : cl.Message):
        history = cl.user_session.get("history")
        history.append({"role":"user","content":message.content})

        msg = cl.Message(content="Analyzing your request and determining the best course of action...\n\n")

        result = Runner.run_streamed(
            starting_agent=lead_agent,#7
            input = history,
            run_config= config
        )

        async for event in result.stream_events():
            if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                await msg.stream_token(event.data.delta)
        # async for event in result.stream_events():
        #     if event.type == "raw_response_event":
        #         try:
        #             if isinstance(event.data, ResponseTextDeltaEvent):
        #                 await msg.stream_token(event.data.delta)
        #         except Exception as e:
        #             print("Error while streaming token:", e)
        #             continue  # Skip broken chunk


        await msg.send()  # Ensure the final message is sent after streaming

        history.append({"role":"assistant","content":result.final_output})
        cl.user_session.set("history",history)
        # await cl.Message(content=result.final_output).send()

# @cl.on_chat_start
# async def handlestart():
#         cl.user_session.set("history",[])
#         await cl.Message(content="Hello My Name is A.basit's AI How Can I Help You!").send()

# @cl.on_message
# async def handlemessage(message : cl.Message):
#         history = cl.user_session.get("history")
#         history.append({"role":"user","content":message.content})
#         result = await Runner.run(
#             starting_agent=lead_agent,#7
#             input = history,
#             run_config= config
#         )
#         history.append({"role":"assistant","content":result.final_output})
#         cl.user_session.set("history",history)
#         await cl.Message(content=result.final_output).send()