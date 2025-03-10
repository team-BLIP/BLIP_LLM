from langchain_core.prompts import ChatPromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chat_models import ChatOpenAI
from langchain.chains.llm import LLMChain
from langchain.chains import MapReduceDocumentsChain, ReduceDocumentsChain
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from src.env_variable import OPENAI_KEY, MEETING_TEXT

class MeetingSummary:
    def __init__(self):
        self.OPENAI_KEY = OPENAI_KEY
        
        self.map_prompt = ChatPromptTemplate.from_template("""
        너는 회의 내용을 요약하는 AI야.
        다음 내용을 알맞고 핵심적이게 요약해 주세요.
        <회의 내용>
        {content}
        """)
        
        self.reduce_prompt = ChatPromptTemplate.from_template("""
        다음은 회의 요약 모음이야.
        {docs}

        이것들을 가져와서 최종 통합 요약해.
        회의 내용을 알아보기 쉽고 이해하기 쉽게 정리해줘.
        마크다운(Markdown)을 사용해 가독성을 높여줘.
        제목을 포함하고, 중요한 핵심 내용은 강조해줘.
        """)
        
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=100, length_function=len
        )
        
        self.llm = ChatOpenAI(model_name='gpt-4o', temperature=0)
        
        self.map_chain = LLMChain(llm=self.llm, prompt=self.map_prompt)
        self.reduce_chain = LLMChain(llm=self.llm, prompt=self.reduce_prompt)
        
        self.combine_documents_chain = StuffDocumentsChain(
            llm_chain=self.reduce_chain, document_variable_name="docs"
        )
        
        self.reduce_documents_chain = ReduceDocumentsChain(
            combine_documents_chain=self.combine_documents_chain,
            token_max=4000
        )
        
        self.map_reduce_chain = MapReduceDocumentsChain(
            llm_chain=self.map_chain,
            reduce_documents_chain=self.reduce_documents_chain,
            document_variable_name="content",
            return_intermediate_steps=False,
        )

    def generate_text(self, text:str):
        texts = self.text_splitter.create_documents([text])
        summary_result = self.map_reduce_chain.invoke({'input_documents': texts})
        return summary_result['output_text']

# if __name__ == "__main__":
#     with open(MEETING_TEXT, encoding='utf-8') as f:
#         meeting_text = f.read()
    
#     summarizer = MeetingSummary()
#     summary = summarizer.generate_text(meeting_text)
#     print(summary)