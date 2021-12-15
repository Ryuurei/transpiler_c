# transpiler_c
By Benoit PHAM

Transpiler from a linear/logistic regression into a C file.

How to use:
```
python3 transpile_simple_model.py

```
To build the models, generate the joblib files and generate the C file.

In the `utils.py`, precise in the `train_and_joblib` functions, specify your datasets and when calling function `generate_predict_in_c` precise the type of your model to generate your .c file.
