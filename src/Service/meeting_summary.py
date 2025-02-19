import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate
)

class MeetingSummarizer:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('OPENAI_API_KEY')

        self.template = """
        너는 회의 내용을 요약하는 AI야. 회의 내용을 알아보기 쉽고 이해하기 쉽게 정리해줘.
        마크다운(Markdown)을 사용해 가독성을 높여줘.
        제목을 포함하고, 중요한 핵심 내용은 강조해줘.
        문장은 ~함, 했음 등의 형태로 자연스럽게 마무리해줘.

        <회의 내용>
        {회의내용}
        """

        self.prompt = ChatPromptTemplate.from_template(self.template)
        self.model = ChatOpenAI(model_name = 'gpt-4o', temperature=0)
    
    def summarize_meeting(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            meeting_text = f.read()
        
        formatted_prompt = self.prompt.format(회의내용=meeting_text)
        output = self.model.invoke(formatted_prompt)
        return output.content

# load_dotenv()
# answer = MeetingSummarizer().summarize_meeting(os.getenv('MEETING_NOTES_PATH'))
# print(answer, answer)


