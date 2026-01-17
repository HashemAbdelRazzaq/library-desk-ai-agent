from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI

from server.tools import (
    find_books,
    create_order,
    restock_book,
    update_price,
    order_status,
    inventory_summary
)


def create_agent():
    

    llm = ChatOpenAI(
        temperature=0
    )

    tools = [
        find_books,
        create_order,
        restock_book,
        update_price,
        order_status,
        inventory_summary
    ]

    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.OPENAI_FUNCTIONS,
        verbose=True
    )

    return agent
 