from typing import Optional

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch


class LocalLLM:
    """
    Minimal wrapper around a local seq2seq LLM with configuration and a
    single generate(prompt) method that returns decoded text.
    """

    def __init__(self, model_name: str = "google/flan-t5-base", device: Optional[str] = None) -> None:
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to(self.device)

    def generate(
        self,
        prompt: str,
        max_length: int = 64,
        max_new_tokens: int | None = None,
        num_beams: int = 4,
        early_stopping: bool = True,
    ) -> str:
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        outputs = self.model.generate(
            **inputs,
            max_length=max_length,
            num_beams=num_beams,
            early_stopping=early_stopping,
        )
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True).strip()


