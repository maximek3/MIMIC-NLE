"""This script contains all the steps to extract MIMIC-NLE from MIMIC-CXR"""
import argparse

from utils.json_processing import read_jsonl_lines, write_jsonl_lines
from utils.preprocess_mimic import extract_sentences


def assign_sentences(query_file, data):
    """
    Matches the sentence ID in our query files to the corresponding sentences in the MIMIC reports.
    Args:
        - query_file: provided files that contain sentence IDs and labels
        - data: all the sentences extracted from the MIMIC reports
    Returns:
        - nles: mimic-nle dataset
    """
    nles = []
    for line in query_file:
        nle_content = line
        source_data = data[line["sentence_ID"]]
        nle_content["nle"] = source_data["sentence"]
        nle_content["report_ID"] = source_data["report_ID"]
        nle_content["patient_ID"] = source_data["patient_ID"]
        nles.append(nle_content)
    return nles


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--reports_path", type=str, help="path to MIMIC-CXR reports")
    args = parser.parse_args()

    reports_sample = extract_sentences(args.reports_path)  # this may take a while

    for subset in ["dev", "test", "train"]:
        query_file = read_jsonl_lines(f"mimic-nle/query/{subset}-query.json")
        nles = assign_sentences(query_file, reports_sample)
        write_jsonl_lines(f"mimic-nle/mimic-nle-{subset}.json", nles)
        
    print("MIMIC-NLE train, dev, and test successfully generated!")
