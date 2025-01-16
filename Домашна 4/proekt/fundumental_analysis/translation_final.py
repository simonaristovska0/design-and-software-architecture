import os
from transformers import MarianMTModel, MarianTokenizer


class TranslationStrategy:
    """Abstract base class for translation strategies."""

    def translate(self, text):
        raise NotImplementedError("Translate method must be implemented by subclasses.")


class MarianTranslationStrategy(TranslationStrategy):
    """Translation strategy using MarianMT model."""

    def __init__(self, model_name):
        self.tokenizer = MarianTokenizer.from_pretrained(model_name)
        self.model = MarianMTModel.from_pretrained(model_name)

    def translate(self, text):
        try:
            inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
            translated_tokens = self.model.generate(**inputs)
            translated_text = self.tokenizer.decode(translated_tokens[0], skip_special_tokens=True)
            return translated_text
        except Exception as e:
            print(f"Error translating text: {e}")
            return None


def translate_files(folder_path, translation_strategy):
    """Translates all .txt files in the given folder using the provided translation strategy."""
    for root, _, files in os.walk(folder_path):
        print(f"Processing directory: {root}")
        for file_name in files:
            if file_name.endswith(".txt"):
                file_path = os.path.join(root, file_name)
                print(f"Translating file: {file_path}")
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()

                    if content.strip():  # Check if the file contains text
                        # Translate the text
                        translated_content = translation_strategy.translate(content)

                        if translated_content:
                            # Save the translated content to a new file
                            translated_file_path = os.path.join(root, f"translated_{file_name}")
                            with open(translated_file_path, "w", encoding="utf-8") as f:
                                f.write(translated_content)
                            print(f"Translated content saved to: {translated_file_path}")
                        else:
                            print(f"Failed to translate file: {file_name}")
                    else:
                        print(f"File is empty: {file_name}")
                except Exception as e:
                    print(f"Error processing file {file_name}: {e}")
            else:
                print(f"Skipping non-txt file: {file_name}")


if __name__ == "__main__":
    model_name = "Helsinki-NLP/opus-mt-mk-en"
    print("Loading the MarianMT translation strategy...")
    translation_strategy = MarianTranslationStrategy(model_name)

    pdf_downloads_folder = "pdf_downloads"

    translate_files(pdf_downloads_folder, translation_strategy)
