
from typing import Any

from pydantic import BaseModel, ValidationError

from spyllm.graph.consts import APP_NODE_ID
from spyllm.graph.models import (Edge, GraphExtractor, GraphStructure, LLMNode, ModelGenerateEdge, Node, ToolCallEdge,
                                 ToolNode)
from spyllm.llm.models import AssistantMessage, Message, UserMessage


class FunctionParameters(BaseModel):
    type: str
    required: list[str]
    properties: dict[str, dict[str, str]]

class Function(BaseModel):
    name: str
    description: str
    parameters: FunctionParameters

class OllamaTool(BaseModel):
    type: str
    function: Function

class OllamaRequestModel(GraphExtractor):
    model: str
    stream: bool
    options: dict[str, str]
    messages: list[UserMessage | AssistantMessage]
    tools: list[OllamaTool]

    def extract_graph_structure(self) -> GraphStructure:
        nodes: list[Node] = []
        edges: list[Edge] = []
        
        model: LLMNode = LLMNode(node_id=self.model)
        nodes.append(model)
        
        for message in self.messages:
            if isinstance(message, UserMessage):
                model_generate_edge = ModelGenerateEdge(prompt=message.content, 
                                                        source_node_id=APP_NODE_ID, 
                                                        target_node_id=model.node_id)
                edges.append(model_generate_edge)
        
        for tool in self.tools:
            tool_node = ToolNode(node_id=tool.function.name, tool_description=tool.function.description)
            nodes.append(tool_node)

        return nodes, edges

class OllamaToolCall(BaseModel):
    name: str
    parameters: dict[str, Any]

class OllamaAssistantMessage(Message):
    content: str

class OllamaResponseModel(GraphExtractor):
    model: str
    created_at: str
    message: OllamaAssistantMessage
    total_duration: int
    load_duration: int
    prompt_eval_count: int
    prompt_eval_duration: int
    eval_count: int
    eval_duration: int

    def extract_graph_structure(self) -> GraphStructure:
        edges: list[Edge] = []

        # First check if it's a tool call
        message_parts = self.message.content.split("\n")
        for part in message_parts: 
            try:
                tool_call = OllamaToolCall.model_validate_json(part)
                tool_call_edge = ToolCallEdge(source_node_id=APP_NODE_ID,
                                    target_node_id=tool_call.name,
                                    tool_input=tool_call.parameters)
                edges.append(tool_call_edge)
            except ValidationError:
                model_generate_edge = ModelGenerateEdge(prompt=self.message.content,
                                                    source_node_id=self.model,
                                                    target_node_id=APP_NODE_ID)
                edges.append(model_generate_edge)

        return [], edges
