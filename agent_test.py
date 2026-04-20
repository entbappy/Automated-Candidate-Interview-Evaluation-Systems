from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.teams import RoundRobinGroupChat
from dotenv import load_dotenv
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.base import TaskResult
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

model_client = OpenAIChatCompletionClient(model="gpt-4o", api_key=OPENAI_API_KEY)



async def my_agents(job_position = "AI Engineer"):
    interviewer = AssistantAgent(
        name = "Interviewer",
        model_client= model_client,
        description=f"An AI agent that conducts interviews for a {job_position} position.",
        system_message=f'''
        You are a professional interviewer for a {job_position} position.
        Ask one clear question at a time and Wait for user to respond. 
        Your job. is to continue and ask questions, don't pay any attention to career coach response. 
        Make sure to ask question based on Candidate's answer and your expertise in the field.
        Ask 3 questions in total covering technical skills and experience, problem-solving abilities, and cultural fit.
        After asking 3 questions, say 'TERMINATE' at the end of the interview.
        Make question under 50 words.
    '''
    )

    
    candidate = UserProxyAgent(
        name= "Candidate",
        description=f"An agent that simulates a candidate for a {job_position} position.",
        input_func=input
    )


    evaluation = AssistantAgent(
        name = "Evaluator",
        model_client= model_client,
        description=f"An AI agent that provides feedback and advice to candidates for a {job_position} position.",
        system_message=f'''
        You are a career coach specializing in preparing candidates for {job_position} interviews.
        Provide constructive feedback on the candidate's responses and suggest improvements.
        After the interview, summarize the candidate's performance and provide actionable advice.
        Make it under 100 words.
    '''

    )

    terninate_condition = TextMentionTermination(text="TERMINATE")

    team = RoundRobinGroupChat(
        participants=[interviewer, candidate, evaluation],
        termination_condition= terninate_condition,
        max_turns=20
    )

    return team



async def run_interview(team):
    async for message in team.run_stream(task='Start the interview with the first question ?'):

        if isinstance(message, TaskResult):
            message = f'Interview completed with result: {message.stop_reason}'
            yield message
        
        else:
            message = f'{message.source}: {message.content}'
            yield message



async def main():
    job_position = "AI Engineer"
    team = await my_agents(job_position)

    async for message in run_interview(team):
        print('-' * 70)
        print(message)




if __name__ == "__main__":
    import asyncio
    asyncio.run(main())