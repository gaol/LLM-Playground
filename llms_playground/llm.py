import sys
import json
import importlib
import logging

from typing import Optional, Dict

from llms_playground import BASE_DIR
from llms_playground.base import ModelConfig, LLMHandler

def _load_function(module_name: str, module_path: str, function_name: str):
    """Load a function dynamically from a Python file."""

    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load module {module_name} from {module_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)  # Load the module dynamically
    return getattr(module, function_name)  # Get the function

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
        provider_name = model_config.provider.name.lower()
        module_path = f"{BASE_DIR}/llms/{provider_name}.py"
        try:
            llm_func = _load_function(provider_name, module_path, "__llm__")
            return llm_func(model_config)
        except Exception as e:
            logging.error(f"An error occurred: {e}", exc_info=True)
            return None
