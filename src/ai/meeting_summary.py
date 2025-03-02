from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from src.infrastructure.env_variable import OPENAI_API_KEY

class MeetingSummary:
    def __init__(self):
        self.api_key = OPENAI_API_KEY
        
        self.template = """
        너는 회의 내용을 요약하는 AI야.
        회의 내용을 알아보기 쉽고 이해하기 쉽게 정리해줘.
        마크다운(Markdown)을 사용해 가독성을 높여줘.
        제목을 포함하고, 중요한 핵심 내용은 강조해줘.
        
        <회의내용>
        {회의내용}
        """
        
        self.prompt = ChatPromptTemplate.from_template(template=self.template)
        self.model = ChatOpenAI(model_name='gpt-4o', temperature=0)
    
    def summary(self, content : str):
        formatted_prompt = self.prompt.format(회의내용=content)
        output = self.model.invoke(formatted_prompt)
        return output.content