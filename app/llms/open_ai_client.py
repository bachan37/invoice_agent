from app.constants import OPENAI_CHAT_MODEL
from langchain_openai import ChatOpenAI
from app.config.env_config import settings

class OpenAIClient:
    """Factory for OpenAI ."""

    def __init__(self) -> None:
        """Initialize with model name and temperature from constants."""
        self.model_name = OPENAI_CHAT_MODEL.MODEL_NAME.value
        self.temperature = OPENAI_CHAT_MODEL.TEMPERATURE.value

    def create_client(self):
        """Create a chat model client.

        Returns:
            ChatOpenAI instance.
        """
        chat_client = ChatOpenAI(
            model_name=self.model_name,
            temperature=self.temperature,
            api_key=settings.OPENAI_API_KEY,
        )
        return chat_client

    def create_structured_output_parser_client(self, PydanticInvoiceSchema):
        """Create an invoice parser client using OpenAI's chat model.

        Args:
            PydanticInvoiceSchema: Pydantic schema for the expected invoice data.

        Returns:
            JsonOutputParser bound to an OpenAI chat model.
        """
        chat_client = self.create_client().with_structured_output(PydanticInvoiceSchema)

        return chat_client


# singleton
open_ai_client = OpenAIClient()