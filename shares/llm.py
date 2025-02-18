import os
import json
from dataclasses import dataclass, field
from enum import Flag, auto
from typing import Optional, Dict, List

# An Enum based class
class ModalityType(Flag):
    """Defines different AI model modalities, allowing multi-modal support."""
    TEXT = auto()
    IMAGE = auto()
    AUDIO = auto()
    VIDEO = auto()
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

@dataclass
class ModelConfig:
    """Represents a globally unique AI model configuration."""
    name: str  # Global unique model name
    base_url: str # required, may have default value depends on the provider
    api_key: str  # required
    model: str    # required, may have default value depends on the provider
    modality: ModalityType = ModalityType.TEXT_TO_TEXT  # Multi-modality support
    tools: List[str] = field(default_factory=list)  # AI model's tools to be used, default is empty list
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
            name=data["name"],
            base_url=data["base_url"],
            api_key=os.getenv(data["api_key"]),
            model=data.get("model"),
            modality=ModalityType[data.get("modality", "TEXT_TO_TEXT")],
            tools=data.get("tools", []),
            additional_params=data.get("additional_params", {})
        )


class LLMProviderRegistry:
    """Manages a collection of AI models with dynamic configuration support."""

    def __init__(self):
        self.models: Dict[str, ModelConfig] = {}

    def register_model(self, model: ModelConfig):
        """Registers a new AI model dynamically (ensures global uniqueness)."""
        self.models[model.name] = model

    def get_model(self, name: str) -> Optional[ModelConfig]:
        """Retrieves an AI model by name."""
        return self.models.get(name)

    def list_models(self) -> Dict[str, ModelConfig]:
        """Lists all registered AI models."""
        return self.models

    def __iter__(self):
        """Iterates over the models in the registry."""
        return iter(self.models.values())

    def load_from_json(self, file_path: str):
        """Loads models from a JSON file."""
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            for model_data in data:
                model = ModelConfig.from_dict(model_data)
                self.register_model(model)

    def save_to_json(self, file_path: str):
        """Saves the current model configurations to a JSON file."""
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump([model.__dict__ for model in self.models.values()], file, indent=4)


