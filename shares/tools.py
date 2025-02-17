from enum import Enum
from dataclasses import dataclass, field
from typing import Optional, Dict, List

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
