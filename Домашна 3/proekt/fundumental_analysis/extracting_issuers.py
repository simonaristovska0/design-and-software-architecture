import os


def rename_folders():
    """Returns a dictionary mapping issuer codes to full issuer names."""
    return {
        "ALK": "Алкалоид АД Скопје",
        "AMEH": "Агромеханика АД Скопје",
        "AUMK": "Аутомакедонија АД Скопје",
        "BIM": "БИМ АД Свети Николе",
        "DIMI": "Димко Митрев АД Велес",
        "EVRO": "Европа АД Скопје",
        "GRNT": "Гранит АД Скопје",
        "GTC": "ГТЦ АД Скопје",
        "KMB": "Комерцијална Банка АД Скопје",
        "LOTO": "Лотарија на Македонија АД Скопје",
        "VITA": "Витаминка АД Прилеп",
        "VTKS": "Ветекс АД Велес",
        "MAKP": "Макпетрол АД Скопје",
        "OILK": "ОИЛКО КДА Скопје",
        "PKB": "Пекабеско АД Кадино, Илинден",
        "POPK": "Попова кула АД Демир Капија",
        "SKP": "Скопски Пазар АД Скопје",
        "SLAV": "Славеј АД Скопје",
        "SDOM": "Современ дом АД Прилеп",
        "TKVS": "ВВ Тиквеш АД Кавадарци",
        "TIKV": "ГД Тиквеш АД Кавадарци",
        "ZAS": "ЖАС АД Скопје",
        "KARO": "Жито Караорман АД Кичево",
        "ZPOG": "Жито Полог АД Тетово",
        "ZPKO": "ЗК Пелагонија АД Битола",
        "INHO": "Интернешнел Хотелс АД Скопје",
        "KLST": "Кристал 1923 АД Велес",
        "STB": "Стопанска банка АД Скопје",
        "STOK": "Стокопромет АД Скопје",
        "TETE": "Тетекс АД Тетово",
        "TNB": "Тутунски комбинат АД Прилеп",
        "UNI": "УНИ Банка АД Скопје ",
        "FERS": "Фершпед АД Скопје",
        "FKTL": "Фруктал Мак АД Скопје",
        "MPOL": "Хотели-Метропол АД Охрид",
        "CKB": "Централна кооперативна банка АД Скопје",
        "USJE": "Цементарница УСЈЕ АД Скопје",
        "TEAL": "ТЕАЛ АД Тетово",
        "SNBTO": "СН Осигурителен Брокер АД Битола",
        "RZUS": "РЖ Услуги АД Скопје",
        "MODA": "Мода АД Свети Николе",
        "MAKS": "Макстил АД Скопје",
        "MPT": "Макпромет АД Штип",
        "NEME": "Неметали Огражден АД Струмица",
        "MTUR": "Македонијатурист АД Скопје",
        "MZPU": "МЗТ Пумпи АД Скопје",
        "RZTK": "РЖ Техничка контрола АД Скопје",
        "MERM": "Мермерен комбинат АД Прилеп",
        "MKSD": "Макошпед АД Скопје",
    }


def rename_txt_files(base_path, dictionary):
    # Iterate through folders in the base_path
    for folder in os.listdir(base_path):
        folder_path = os.path.join(base_path, folder)

        # Skip if not a directory
        if not os.path.isdir(folder_path):
            continue

        # Check if folder matches any value in the dictionary
        matched_key = None
        for key, value in dictionary.items():
            if folder == value or folder == key:  # Match either value or key
                matched_key = key
                break

        if not matched_key:
            print(f"Skipping folder {folder}, no match in dictionary.")
            continue

        # Rename all text files in the folder
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)

            # Skip non-txt files
            if not file_name.endswith('.txt'):
                continue

            # Generate the new file name
            if file_name.startswith("sentiment_"):
                new_file_name = f"sentiment_{matched_key}_combined.txt"
            elif file_name.startswith("translated_"):
                new_file_name = f"translated_{matched_key}_combined.txt"
            else:
                # Default combined file name
                new_file_name = f"{matched_key}_combined.txt"

            new_file_path = os.path.join(folder_path, new_file_name)

            # Rename the file
            os.rename(file_path, new_file_path)
            print(f"Renamed: {file_path} -> {new_file_path}")

        # Optionally, rename the folder to its key (standardized name)
        new_folder_path = os.path.join(base_path, matched_key)
        if folder_path != new_folder_path:
            os.rename(folder_path, new_folder_path)
            print(f"Renamed folder: {folder_path} -> {new_folder_path}")


if __name__ == "__main__":
    # Base path where the folders are located
    base_path = os.path.join(os.path.dirname(__file__), "pdf_downloads")

    # Call the rename function with the dictionary
    dictionary = rename_folders()
    rename_txt_files(base_path, dictionary)

if __name__ == "__main__":
    base_path = os.path.join(os.path.dirname(__file__), "pdf_downloads")
    dictionary = rename_folders()
    rename_txt_files(base_path, dictionary)
