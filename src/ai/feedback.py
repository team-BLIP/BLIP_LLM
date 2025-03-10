from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains.llm import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_core.documents import Document
from langchain.chat_models import ChatOpenAI


class PersonalFeedback:
    def __init__(self):
        self.prompt_template = """
            <한 사람의 회의 내용>
            {content}

            이 텍스트는 회의를 진행하고 있는 한 사람의 말이야.
            이 사람의 개인 피드백을 수행해줘.(피드백을 할 때 사람들의 이름은 적지마)
            개인 피드백을 수행을 할 때, 문장은 ~함, 했음 등의 형태로 자연스럽게 마무리줘.
            또 개인 피드백을 수행을 할 때, 문제점이 있다면 문제점 제시와 해결방안에 대해 알려주고, 큰 문제점이 없다면 그냥 넘어가도 좋아.
            잘한 점이 있다면 이것에 대해서도 말해줘.
            추가 개선 사항이 있다면 말해주면 좋아.
            또 너무 길지 않게 200자 내외로 해줘
        """
        
        self.prompt = PromptTemplate.from_template(self.prompt_template)
        self.llm = ChatOpenAI(model_name = 'gpt-4o', temperature=0)
        self.llm_chain = LLMChain(llm=self.llm, prompt=self.prompt)
        self.stuff_chain = StuffDocumentsChain(llm_chain=self.llm_chain, document_variable_name='content')
    
    def generate_feedback(self, contents):
        meeting_doc = Document(page_content=contents)
        result = self.stuff_chain.run([meeting_doc])
        return result