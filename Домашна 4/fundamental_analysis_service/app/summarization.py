from transformers import pipeline
import os


def summarize_text(file_path, summarizer, max_length=130, min_length=30):
    """Summarizes the content of a text file."""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    print(f"Summarizing: {file_path}")
    summarized_text = summarizer(content, max_length=max_length, min_length=min_length, do_sample=False)[0][
        "summary_text"]

    output_file_path = file_path.replace("translated_", "summary_")
    with open(output_file_path, "w", encoding="utf-8") as f:
        f.write(summarized_text)
    print(f"Summarization saved to: {output_file_path}")


if __name__ == "__main__":
    print("Using Hugging Face hub for summarization model...")
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

    folder_path = "pdf_downloads"

    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            if file_name.startswith("translated_") and file_name.endswith(".txt"):
                file_path = os.path.join(root, file_name)
                summarize_text(file_path, summarizer)
