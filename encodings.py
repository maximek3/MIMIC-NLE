"""Dictionaries to uncode the one-hot encodings used as labels in the dataset."""

MIMIC_DIAGNOSIS2LABEL = {
    'Atelectasis': 0,
    'Consolidation': 1,
    'Edema': 2,
    'Enlarged Cardiomediastinum': 3,
    'Lung Lesion': 4,
    'Lung Opacity': 5,
    'Pleural Effusion': 6,
    'Pleural Other': 7,
    'Pneumonia': 8,
    'Pneumothorax': 9
} # ordered by alphabet
MIMIC_LABEL2DIAGNOSIS = {v: k for k, v in MIMIC_DIAGNOSIS2LABEL.items()}

MIMIC_CAT2ONEHOT = {
    'nan': [1,0,0],
    '0.0': [1,0,0],
    '-1.0': [0,1,0],
    '1.0': [0,0,1]
}

MIMIC_STR2ONEHOT = {
    'nan': [1,0,0],
    'Negative': [1,0,0],
    'Uncertain': [0,1,0],
    'Positive': [0,0,1]
}