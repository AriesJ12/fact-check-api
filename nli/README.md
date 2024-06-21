('---\ndatasets:\n- ctu-aic/ctkfacts_nli\nlanguages:\n- cs\nlicense: cc-by-sa-4.0\ntags:\n- natural-language-inference\n\n---',)

# 🦾 xlm-roberta-large-squad2-ctkfacts_nli
Transformer model for **Natural Language Inference** in ['cs'] languages finetuned on ['ctu-aic/ctkfacts_nli'] datasets.

## 🧰 Usage

### 👾 Using UKPLab `sentence_transformers` `CrossEncoder`
The model was trained using the `CrossEncoder` API and we recommend it for its usage.
```python
from sentence_transformers.cross_encoder import CrossEncoder
model = CrossEncoder('ctu-aic/xlm-roberta-large-squad2-ctkfacts_nli')
scores = model.predict([["My first context.", "My first hypothesis."],  
                        ["Second context.", "Hypothesis."]])
```

### 🤗 Using Huggingface `transformers`
```python
from transformers import AutoModelForSequenceClassification, AutoTokenizer
model = AutoModelForSequenceClassification.from_pretrained("ctu-aic/xlm-roberta-large-squad2-ctkfacts_nli")
tokenizer = AutoTokenizer.from_pretrained("ctu-aic/xlm-roberta-large-squad2-ctkfacts_nli")
```




## 🌳 Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## 👬 Authors
The model was trained and uploaded by **[ullriher](https://udb.fel.cvut.cz/?uid=ullriher&sn=&givenname=&_cmd=Hledat&_reqn=1&_type=user&setlang=en)** (e-mail: [ullriher@fel.cvut.cz](mailto:ullriher@fel.cvut.cz))

The code was codeveloped by the NLP team at Artificial Intelligence Center of CTU in Prague ([AIC](https://www.aic.fel.cvut.cz/)).

## 🔐 License
[cc-by-sa-4.0](https://choosealicense.com/licenses/cc-by-sa-4.0)


## 💬 Citation
If you find this repository helpful, feel free to cite our publication:
```

@article{DBLP:journals/corr/abs-2201-11115,
  author    = {Herbert Ullrich and
               Jan Drchal and
               Martin R{'{y}}par and
               Hana Vincourov{'{a}} and
               V{'{a}}clav Moravec},
  title     = {CsFEVER and CTKFacts: Acquiring Czech Data for Fact Verification},
  journal   = {CoRR},
  volume    = {abs/2201.11115},
  year      = {2022},
  url       = {https://arxiv.org/abs/2201.11115},
  eprinttype = {arXiv},
  eprint    = {2201.11115},
  timestamp = {Tue, 01 Feb 2022 14:59:01 +0100},
  biburl    = {https://dblp.org/rec/journals/corr/abs-2201-11115.bib},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}

```

