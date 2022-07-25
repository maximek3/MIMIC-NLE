import os
import math

from spacy.lang.en import English

from utils.section_splitter import section_text


def sentence_splitting(nlp, text):
    return list(nlp(text).sents)


def extract_sentences(mimic_path, report_count=math.inf, patients=None):
    """
    Getting sentences from the reports. We only consider findings and impression sections.
    Includes processing steps:
        - splits sentences by spacy AND keywords in splitters
    Args:
        - mimic_path: path/to/mimic_reports
        - report_count: upper limit to number of reports we consider
        - patients: list of patient IDs we consider (None means no restriction)
    Returns:
        -list[dict]: content dictionary for each report
    """
    
    print("Starting sentence extraction...")

    report_counter = 0

    # output dictionary init
    output = {}

    # set up sentence splitting
    nlp = English()
    # sentencizer = nlp.create_pipe("sentencizer")
    # nlp.add_pipe("sentencizer")
    sentencizer = nlp.add_pipe(nlp.create_pipe("sentencizer"))

    # iterate through sub-folders p10-p19
    for subfolder in os.listdir(mimic_path):
        subfolder_path = os.path.join(mimic_path, subfolder)
        if not os.path.isdir(subfolder_path):  # for things like .DS_Store
            continue
        for patient_ID in os.listdir(subfolder_path):
            if patients and patient_ID not in patients:
                continue
            patient_path = os.path.join(subfolder_path, patient_ID)
            if not os.path.isdir(patient_path): # for things like .DS_Store
                continue
            for report_ID in os.listdir(patient_path):
                report_path = os.path.join(patient_path, report_ID)
                if not os.path.isfile(report_path):
                    print(f"ERROR: no file found for file {report_path}")
                    continue

                with open(report_path, "r") as file:
                    report = file.read()
                report_counter += 1

                sections, section_names, _ = section_text(report)

                # we only keep impression and finding section as "image captions"
                relevant_sections = [
                    text.replace("\n", "")
                    for text, name in zip(sections, section_names)
                    if name in ["impression", "findings"]
                ]

                if len(relevant_sections) == 0:
                    continue

                report = "".join(relevant_sections)
                report = report.replace("  ", " ")
                splitted_sentences = sentence_splitting(nlp, report)
                splitted_sentences = [
                    str(sent).lstrip(" ") for sent in splitted_sentences
                ]

                # make each sentence an entry
                for idx, sentence in enumerate(splitted_sentences):
                    sent_content = {}
                    report_ID = report_ID.replace(".txt", "")
                    sentence_ID = f"{report_ID}#{str(idx)}"

                    sent_content["sentence_ID"] = sentence_ID
                    sent_content["patient_ID"] = patient_ID
                    sent_content["report_ID"] = report_ID
                    sent_content["sentence"] = sentence

                    output[sentence_ID] = sent_content

                if report_counter > report_count:
                    break
            if report_counter > report_count:
                break
        if report_counter > report_count:
            break
        
    print("All sentences extracted!")

    return output
