# transpiler_c
By Benoit PHAM

Transpiler from a linear/logistic regression into a C file.

# Install dependencies with 
```
pip install -r requirements.txt
```
or
```
conda create --name <env> --file requirements.txt
```

# How to use:
```
python3 transpile_simple_model.py
```
To build the models, generate the joblib files and generate the C file.

In the `utils.py`, specify in the `train_and_joblib` functions the paths to your datasets.
When calling function `generate_predict_in_c` precise the type of your model to generate your .c file.
