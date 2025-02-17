import json
from enum import Enum
from dataclasses import dataclass, field
from typing import Optional, Dict

class ToolType(Enum):
    """Defines types of tools a model can use."""
    OPENAPI = "openapi"  # External API calls
    LOCAL_FUNCTION = "local_function"  # Python functions

class ResponseType(Enum):
    """Defines expected response types for tools."""
    JSON = "json"
    TEXT = "text"
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"
    NONE = "none"  # No response, just trigger action

@dataclass
class ToolConfig:
    """Defines a tool that an AI model can use."""
    name: str  # Tool name global unique
    type: ToolType  # Type of tool (OpenAPI or Local Function)
    description: str  # Description of the tool
    parameters: Dict[str, str] = field(default_factory=dict)  # Expected parameters
    endpoint: Optional[str] = None  # API URL if it's an OpenAPI tool
    function_ref: Optional[str] = None  # Function reference if it's a local function
    response_type: ResponseType = ResponseType.JSON  # Expected response type from the tool

class ToolRegistry:
    """Manages a collection of tools with dynamic configuration support."""

    def __init__(self):
        self.tools: Dict[str, ToolConfig] = {}

    def register_tool(self, tool: ToolConfig):
        """Registers a new tool dynamically (ensures global uniqueness)."""
        self.tools[tool.name] = tool

    def get_tool(self, name: str) -> Optional[ToolConfig]:
        """Retrieves a tool by name."""
        return self.tools.get(name)

    def list_tools(self) -> Dict[str, ToolConfig]:
        """Lists all registered tools."""
        return self.tools

    def load_from_json(self, file_path: str):
        """Loads tools from a JSON file."""
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            for tool_data in data:
                tool = ToolConfig(**tool_data)
                self.register_tool(tool)

    def save_to_json(self, file_path: str):
        """Saves the current tool configurations to a JSON file."""
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump([tool.__dict__ for tool in self.tools.values()], file, indent=4)

    def __iter__(self):
        """Iterates over the tools in the registry."""
        return iter(self.tools.values())
