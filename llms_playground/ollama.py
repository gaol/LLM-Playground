from llms_playground.base import LLMHandler, ModelConfig, _ModalityType
from typing import List, Union
from langchain_core.messages import HumanMessage, SystemMessage


class OllamaLLM(LLMHandler):
    def __init__(self, model_config: ModelConfig):
        super().__init__(model_config)
        model_type = self.model_config.modality
        if model_type == _ModalityType.TEXT_TO_TEXT:
            self.llm_client = None
        elif model_type == _ModalityType.EMBEDDING:
            self.llm_client = None

    def chat(self, input: Union[str, List[str]], sys_message = None, user_params = None) -> str:
        """ Chat with the model. """
        if self.llm_client is None:
            raise ValueError("llm_client is None")
        messages = []
        if sys_message is not None:
            messages.append(SystemMessage(sys_message))
        messages.append(HumanMessage(input))
        return self.llm_client.invoke(messages)

    def embedding(self, input: Union[str, List[str]], sys_message = None, user_params = None) -> List[float]:
        """ Get Embedding by talking to an embedding model. """
        pass

    def image(self, input: Union[str, List[str]], sys_message = None, user_params = None):
        """ Talk with an image model to generate images based on the input text. """
        pass

    def audio(self, input: Union[str, List[str]], sys_message = None, user_params = None):
        """ Talk with an model to generate audios based on the input text. """
        pass

    def video(self, input: Union[str, List[str]], sys_message = None, user_params = None):
        """ Talk with an model to generate videos based on the input text. """
        pass
