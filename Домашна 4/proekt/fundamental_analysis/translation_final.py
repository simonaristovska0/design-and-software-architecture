import os
from transformers import MarianMTModel, MarianTokenizer


def translate_text(text, model, tokenizer):
    """Translates Macedonian text to English using Hugging Face."""
    try:
        inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
        translated_tokens = model.generate(**inputs)
        translated_text = tokenizer.decode(translated_tokens[0], skip_special_tokens=True)
        return translated_text
    except Exception as e:
        print(f"Error translating text: {e}")
        return None


def translate_files(folder_path, model, tokenizer):
    """Translates all .txt files in the given folder."""
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
                        translated_content = translate_text(content, model, tokenizer)

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
    # Initialize the MarianMT model and tokenizer
    model_name = "Helsinki-NLP/opus-mt-mk-en"
    print("Loading the model and tokenizer...")
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)

    # Define the folder containing the .txt files
    pdf_downloads_folder = "pdf_downloads"

    # Translate all files in the folder
    translate_files(pdf_downloads_folder, model, tokenizer)
