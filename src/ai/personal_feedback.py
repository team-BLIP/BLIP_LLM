from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from src.infrastructure.env_variable import OPENAI_API_KEY

class PersonalFeedback:
    def __init__(self):
        self.api_key = OPENAI_API_KEY

        self.template = """
        <한 사람의 회의 내용>
        {내용}

        이 텍스트는 회의를 진행하고 있는 한 사람의 말이야.
        이 사람의 개인 피드백을 수행해줘.(피드백을 할 때 사람들의 이름은 적지마)
        개인 피드백을 수행을 할 때, 문장은 ~함, 했음 등의 형태로 자연스럽게 마무리줘.
        또 개인 피드백을 수행을 할 때, 문제점이 있다면 문제점 제시와 해결방안에 대해 알려주고, 큰 문제점이 없다면 그냥 넘어가도 좋아.
        잘한 점이 있다면 이것에 대해서도 말해줘.
        추가 개선 사항이 있다면 말해주면 좋아.
        또 너무 길지 않게 200자 내외로 해줘
        """
        self.prompt = ChatPromptTemplate.from_template(template=self.template)
        self.model = ChatOpenAI(model_name='gpt-4o', temperature=0)

    def generate_feedback(self, content:str):
        formatted_prompt = self.prompt.format(내용=content)
        output = self.model.invoke(formatted_prompt)
        return output.content