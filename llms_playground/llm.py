import json
import logging

from typing import Optional, Dict

from llms_playground.base import BASE_DIR, ModelConfig, LLMHandler, _ModelProvider

LOGGER = logging.getLogger(__name__)

def load_openai_handler(model_path: ModelConfig) -> LLMHandler:
    try:
        from llms_playground.openai import OpenAILLM
        return OpenAILLM(model_path)
    except Exception as e:
        LOGGER.error(f"Faied to load OpenAILLM: {e}", exc_info=True)
        raise e # throw it out

def load_ollama_handler(model_path: ModelConfig) -> LLMHandler:
    try:
        from llms_playground.ollama import OllamaLLM
        return OllamaLLM(model_path)
    except Exception as e:
        LOGGER.error(f"Faied to load OllamaLLM: {e}", exc_info=True)
        raise e # throw it out

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

    def load_from_default(self):
        """ read from the default location: models/models.json """
        return self.load_from_json(f"{BASE_DIR}/models/models.json")

    def save_to_json(self, file_path: str):
        """Saves the current model configurations to a JSON file."""
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump([model.__dict__ for model in self.models.values()], file, indent=4)

    def get_llm_handler(self, name: str) -> Optional[LLMHandler]:
        """
        Retrieves an AI model by name.
        """
        model_config = self.get_model(name)
        if model_config is None:
            return None
        if model_config.provider is _ModelProvider.OPENAI:
            return load_openai_handler(model_config)
        elif model_config.provider is _ModelProvider.OLLAMA:
            return load_ollama_handler(model_config)
        else:
            raise ValueError(f"Not supported LLM Provider: {model_config.provider}")
