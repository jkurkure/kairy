import os
from difflib import SequenceMatcher


def get_similarity(file1_data, file2_data):
    return SequenceMatcher(None, file1_data, file2_data).ratio()


def get_all_python_files(directory):
    python_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                python_files.append(os.path.join(root, file))
    return python_files


def rank_similarities(directory):
    python_files = get_all_python_files(directory)
    similarities = []
    for i in range(len(python_files)):
        for j in range(i + 1, len(python_files)):
            with open(python_files[i], encoding="utf8") as file_1, open(
                python_files[j], encoding="utf8"
            ) as file_2:
                file1_data = file_1.read()
                try:
                    file2_data = file_2.read()
                except:
                    print(file_2.name)
                similarity_ratio = get_similarity(file1_data, file2_data)
                similarities.append(
                    (python_files[i], python_files[j], similarity_ratio)
                )
    similarities.sort(key=lambda x: x[2], reverse=True)
    return similarities


if __name__ == "__main__":
    directory = "../"
    similarities = rank_similarities(directory)
    for file1, file2, ratio in similarities:
        print(f"{file1} <-> {file2}: {ratio}")
