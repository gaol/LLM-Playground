import os
from abc import ABC, abstractmethod

from dataclasses import dataclass, field
from enum import Enum, Flag, auto
from typing import Dict, List, Union

class _ModelProvider(Enum):
    """
    The base.py contains internal classes which are implementation related.

    New provider can be added later.
    The lowercase of the provider will be loaded to call specific constructor to AI provider dependent instances.

    ie: in openai.py, call `__llm__(modelConfig)` method to return an instance of `LLMHandler`
    """
    OPENAI = 1
    OLLAMA = 2

class _ModalityType(Flag):
    """
    Defines different AI model modalities, allowing multi-modal support.
    Normally different type means different ways of calling and different parameters and responses.
    """
    TEXT = auto()
    IMAGE = auto()
    AUDIO = auto()
    VIDEO = auto()
    EMBEDDING = auto()
    TEXT_TO_TEXT = TEXT
    TEXT_TO_IMAGE = TEXT | IMAGE
    TEXT_TO_AUDIO = TEXT | AUDIO
    TEXT_TO_VIDEO = TEXT | VIDEO
    IMAGE_TO_TEXT = IMAGE | TEXT
    IMAGE_TO_3D = IMAGE
    IMAGE_TO_VIDEO = IMAGE | VIDEO
    AUDIO_TO_TEXT = AUDIO | TEXT
    AUDIO_TO_AUDIO = AUDIO
    VIDEO_TO_TEXT = VIDEO | TEXT
    VIDEO_TO_IMAGE = VIDEO | IMAGE
    VIDEO_TO_VIDEO = VIDEO
    MULTIMODAL = TEXT | IMAGE | AUDIO | VIDEO  # Example: OpenAI GPT-4o

@dataclass(frozen=True)
class ModelConfig:
    """
    Reprefrom langchain_core.messages import HumanMessagesents a globally unique AI model configuration.
    """
    name: str  # Global unique model name
    base_url: str # required, may have default value depends on the provider
    api_key: str  # required
    model: str    # required, may have default value depends on the provider
    modality: _ModalityType = _ModalityType.TEXT_TO_TEXT  # Multi-modality support
    tools: List[str] = field(default_factory=list)  # AI model's tools to be used, default is empty list
    provider: _ModelProvider = _ModelProvider.OPENAI  # provider, defaults to OPENAI compatible
    additional_params: Dict[str, str] = field(default_factory=dict)

    def get_headers(self) -> Dict[str, str]:
        """Returns the required headers for API requests."""
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    @classmethod
    def from_dict(cls, data: Dict) -> "ModelConfig":
        """Create a ModelConfig from a dictionary (e.g., from JSON)."""
        return cls(
            name = data["name"],
            base_url = data["base_url"],
            api_key = os.getenv(data["api_key"]),
            model = data.get("model"),
            modality = _ModalityType[data.get("modality", "TEXT_TO_TEXT")],
            provider = _ModelProvider[data.get("provider", "OPENAI")],
            tools=data.get("tools", []),
            additional_params=data.get("additional_params", {})
        )


class LLMHandler(ABC):
    """
    A generic LLMHandler that can support different AI providers and model config.
    """
    def __init__(self, model_config: ModelConfig):
        """
        Initialize the LLMHandler.

        :param model_config: The ModelConfig.
        """
        self.model_config = model_config

    @abstractmethod
    def chat(self, input: Union[str, List[str]], sys_message = None, user_params = None) -> str:
        """ Chat with the model. """
        pass

    @abstractmethod
    def embedding(self, input: Union[str, List[str]], user_params = None) -> List[float]:
        """ Get Embedding by talking to an embedding model. """
        pass

    @abstractmethod
    def image(self, input: Union[str, List[str]], user_params = None):
        """ Talk with an image model to generate images based on the input text. """
        pass

    @abstractmethod
    def audio(self, input: Union[str, List[str]], user_params = None):
        """ Talk with an model to generate audios based on the input text. """
        pass

    @abstractmethod
    def video(self, input: Union[str, List[str]], user_params = None):
        """ Talk with an model to generate videos based on the input text. """
        pass

