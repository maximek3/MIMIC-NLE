# MIMIC-NLE Dataset

This repository contains the scripts to extract the MIMIC-NLE dataset from the MIMIC-CXR radiology reports. In order to download MIMIC-CXR, head [here](https://physionet.org/content/mimic-cxr-jpg/2.0.0/). More details on MIMIC-NLE are provided in our MICCAI 2022 paper:

*Explaining Chest X-ray Pathologies in Natural Language* ([arxiv](https://arxiv.org/abs/2207.04343))

## Extracting the dataset

To run our extraction script, please first a create an environment by running `conda env create -f environment.yml`. It is crucial that you use the same `spaCy` library, as otherwise there may be a discrepancy in the sentence splitting.

After you downloaded MIMIC-CXR, get the path of the radiology reports, which should be given in the following structure: 

```
mimic_reports
└───p10
│   └───p10000032
│   │     s50414267.txt
│   │     s53189527.txt
│   │     ...
│   └───p10000764
│   ...
└───p11
...
└───p19
```

You can then generate MIMIC-NLE by simply running: 
```
python extract_mimic_nle.py --reports_path path/to/your/reports
```
The train, dev, and test set will be stored in the `mimic-nle` folder.

## Dataset details

For each Natural Language Explanation (NLE), we get the following information: 

```
{
"sentence_ID": "s51038639#2",                                   // unique NLE identifier
"nle": "Subtle lower lobe opacities may reflect atelectasis.",  // the NLE
"patient_ID": "p11662490",                                      // unique patient ID
"report_ID": "s51038639",                                       // unique radiology report ID
"diagnosis_label": [1, 0, 0, 0, 0, 0, 0, 0, 1, 0],              // one-hot encoding of the diagnosis label, i.e. the label that is being explained
"evidence_label": [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],               // one-hot encoding of the evidence label, i.e. the label that is evidence for another label
"img_labels": [[0, 1, 0], [1, 0, 0], ..., [1, 0, 0]]            // image-wide labels, given as [negative, uncertain, positive] for each class
}
```

The diagnosis and evidence labels apply only specifically to the NLE at hand, while the `img_labels` apply to the whole image and may contain labels not referred to in the NLE. Dictionaries to uncode the one-hot encoding are provided in `encodings.py`.

# Citation

If you make use of MIMIC-NLE, please cite our paper:

```
@inproceedings{MICCAI-KECPPL-2022,
  title = "Explaining Chest X-ray Pathologies in Natural Language",
  author = "Maxime Kayser and Cornelius Emde and Oana Camburu and Guy Parsons and Bartlomiej Papiez and Thomas Lukasiewicz",
  year = "2022",
  booktitle = "Proceedings of the 25th International Conference on Medical Image Computing and Computer-Assisted Intervention, MICCAI 2022, Singapore, 18--22 September 2022",
  month = "September",
  publisher = "Springer",
  series = "Lecture Notes in Computer Science (LNCS)",
}
