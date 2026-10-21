from typing import Annotated , Literal , TypedDict 
from langchain_core.messages import BaseMessage 
from langgraph.graph import add_messages 

class InspectionState(TypedDict):
    messages : Annotated[list[BaseMessage],add_messages]
    inspection_id : str 
    property : str 
    crew : str 
    report : str 
    work_orders : list[dict[str,str]]
    summary : str 
    status : Literal['input','extracting','assigning','completed']
