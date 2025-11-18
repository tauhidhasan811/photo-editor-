import langchain
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage


def generate_prompt(user_preferance, user_instraction, image):
    systemmMessage=SystemMessage(
        content = "Consider you are a profeshonal photo edititor. YOu should edit user photot based on user prompt and there instraction"
    )
    humanMessage=HumanMessage(
        content = [
            {'type': 'text', 'text': user_instraction},
            {'type': 'image', 'image': image}
        ]
    )

    temp = PromptTemplate(
        template = "{system_message}. Edit the image based on the preferance, user Query and Image and return the image where preferance is {user_preferance} and user instraction {human_Message}",
        input_variable=['system_message', 'user_preferance', 'human_Message']
    )

    prompt = temp.invoke(input={
        'system_message':systemmMessage,
        'user_preferance': user_preferance,
        'human_Message': humanMessage
        })
    return prompt


