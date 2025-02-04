import os
from dotenv import load_dotenv
import json

from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate, ChatPromptTemplate
class PersonalFeedback:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('OPENAI_API_KEY')

        self.template = """
        <회의 내용>
        {회의내용}
        ---
        회의 내용을 보고 각 화자별로 개인 피드백을 JSON 리스트 형식으로 제공해줘.
        - 반드시 JSON 리스트 형식으로만 출력해줘.
        - 각 항목은 speaker(화자 이름)와 feedback(피드백)으로 구성해야 해.
        - 마크다운 코드 블록(```json ... ```)을 포함하지 마.
        - 추가 설명 없이 JSON 데이터만 반환해줘.
        
        개인 피드백을 수행을 할 때, 문장은 ~함, 했음 등의 형태로 자연스럽게 마무리줘
        또 개인 피드백을 수행을 할 때, 문제점이 있다면 문제점 제시와 해결방안에 대해 알려주고, 큰 문제점이 없다면 그냥 넘어가도 좋아.
        잘한 점이 있다면 이것에 대해서도 말해줘.
        추가 개선 사항이 있다면 말해주면 좋아.
        """

        self.prompt = PromptTemplate(
            template=self.template,
            input_variables=['회의내용'],
        )

        self.prompt = ChatPromptTemplate.from_template(self.template)
        self.model = ChatOpenAI(model_name='gpt-4o', temperature=0)
    
    def generate_feedback(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            meeting_text = f.read()

        formatted_prompt = self.prompt.format(회의내용=meeting_text)
        output = self.model.invoke(formatted_prompt)
        json_output = json.loads(output.content)
        return json_output

load_dotenv()
answer = PersonalFeedback().generate_feedback(os.getenv('MEETING_NOTES_PATH'))
print(answer)


