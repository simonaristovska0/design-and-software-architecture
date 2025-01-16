import os
from transformers import pipeline, AutoTokenizer


class SentimentAnalysisStrategy:
    def __init__(self, model_name):
        self.model_name = model_name
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.analyzer = pipeline("sentiment-analysis", model=model_name)

    def analyze_chunk(self, chunk):
        label_map = {"LABEL_0": "NEGATIVE", "LABEL_1": "NEUTRAL", "LABEL_2": "POSITIVE"}
        result = self.analyzer(chunk)[0]
        sentiment_label = label_map[result['label']]
        return sentiment_label, result['score']

    def tokenize_text(self, text, max_length=512):
        tokens = self.tokenizer.encode(text, add_special_tokens=False)
        chunks = [tokens[i:i + max_length] for i in range(0, len(tokens), max_length)]
        return [
            self.tokenizer.decode(chunk, skip_special_tokens=True, clean_up_tokenization_spaces=True)
            for chunk in chunks
        ]


def analyze_sentiment(file_path, sentiment_strategy, sentiment_texts):
    """Analyze the sentiment of a file using the specified sentiment strategy."""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Tokenize content into manageable chunks
    chunks = sentiment_strategy.tokenize_text(content)

    # Sentiment scores
    sentiment_scores = {"POSITIVE": 0, "NEGATIVE": 0, "NEUTRAL": 0}

    # Analyze each chunk and aggregate scores
    for chunk in chunks:
        sentiment_label, score = sentiment_strategy.analyze_chunk(chunk)
        sentiment_scores[sentiment_label] += score

    overall_sentiment = max(sentiment_scores, key=sentiment_scores.get)
    overall_probability = sentiment_scores[overall_sentiment] / len(chunks)

    sentiment_explanation = sentiment_texts[overall_sentiment.lower()]
    output_content = (
        f"{overall_sentiment}: {overall_probability:.5f}\n{sentiment_explanation}\n\n"
    )

    output_file_path = file_path.replace("translated_", "sentiment_")
    with open(output_file_path, "w", encoding="utf-8") as f:
        f.write(output_content)
    print(f"Sentiment analysis saved to: {output_file_path}")


if __name__ == "__main__":
    sentiment_texts = {
        "positive": (
            "Според анализата на содржината од последните вести, текстот има јасно позитивен тон, "
            "што укажува на здрави и охрабрувачки финансиски резултати и стабилност на компанијата. "
            "Ова создава силна основа за инвеститорите да размислат за вложување во оваа компанија. "
            "Високиот степен на позитивност сугерира дека компанијата има добри перформанси, растечки приходи "
            "и можност за понатамошно проширување. Препорачуваме детално разгледување на финансиските податоци "
            "како потврда за ваквите заклучоци."
        ),
        "neutral": (
            "Според анализата на содржината од последните вести, текстот покажува избалансиран тон без "
            "истакнати позитивни или негативни аспекти. Ова може да укаже на стабилност во работењето на компанијата, "
            "но без јасни показатели за раст или пад. Препорачуваме дополнителна анализа на финансиските податоци и "
            "информации за донесување на информирана инвестициска одлука."
        ),
        "negative": (
            "Според анализата на содржината од последните вести, текстот има негативен тон, што укажува на предизвици "
            "и можни ризици во работењето на компанијата. Ова може да биде поврзано со опаѓање на приходите, "
            "зголемени трошоци или други финансски проблеми. Препорачуваме претпазливост и детално разгледување "
            "на потенцијалните ризици пред донесување на инвестициска одлука."
        ),
    }

    model_name = "cardiffnlp/twitter-roberta-base-sentiment"
    sentiment_strategy = SentimentAnalysisStrategy(model_name)

    folder_path = "pdf_downloads"

    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            if file_name.startswith("translated_") and file_name.endswith(".txt"):
                file_path = os.path.join(root, file_name)
                analyze_sentiment(file_path, sentiment_strategy, sentiment_texts)
