from faiss import IndexFlatL2
from langchain.chat_models import ChatOpenAI
from langchain.docstore import InMemoryDocstore
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS

from pdca_gpt.agent import Agent


class TestAgent:
    agent: Agent

    @classmethod
    def setup_class(cls):
        cls.agent = Agent.from_llm(
            llm=ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo"),
            vectorstore=FAISS(
                embedding_function=OpenAIEmbeddings().embed_query,
                index=IndexFlatL2(1536),
                docstore=InMemoryDocstore({}),
                index_to_docstore_id={},
            ),
            verbose=True,
            max_iterations=5,
        )

    def test_logic(self):
        result = self.agent.run(objective="What is Sergey Brin's age times 12?")
        assert result == "5764801"

    def test_thinking(self):
        self.agent.run(objective="How can we ensure the safe development of AGI?")
