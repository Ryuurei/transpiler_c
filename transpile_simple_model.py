import joblib
import pandas as pd
import os
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression

def train_and_joblib_linear_regression():
    dataset = pd.read_csv('salary_data.csv') # Predict salary based on years of experience
    X = dataset.iloc[:, :-1].values
    y = dataset.iloc[:, 1].values

    regressor = LinearRegression()
    regressor.fit(X, y)

    joblib.dump(regressor, "linearRegressor.joblib")

def train_and_joblib_logistic_regression():
    dataset = pd.read_csv('01_heights_weights_genders.csv') # Predict a person's gender based on their weight and height
    le = LabelEncoder()
    le.fit(dataset.iloc[:, 0])
    res = le.transform(dataset.iloc[:, 0])
    dataset['Gender'] = res

    X = dataset.iloc[:, 1:3].values
    y = dataset.iloc[:, 0].values

    regressor = LogisticRegression(C=1e40, solver='newton-cg')
    regressor.fit(X, y)

    joblib.dump(regressor, "logisticRegressor.joblib")

def generate_for_linear(joblib_file, predict_value):
    model = joblib.load(joblib_file)
    # We need the intercept (bias) and the coefficients
    thetas_list = []
    len_thetas = 1
    thetas_list.append(model.intercept_)  # put bias is at index 0
    for coef in model.coef_:
        thetas_list.append(coef)
        len_thetas += 1

    # convert theta list to string
    thetas = "{"
    for i in thetas_list:
        thetas += str(i) + ", "
    thetas = thetas[:-2]  # remove last ", "
    thetas += "}"

    # Create and write .c file with values defined above
    c = f"""#include <stdio.h>

float thetas[{len_thetas}] = {thetas};

float linear_regression_prediction(float *features, int n_features) {{
    float res = thetas[0]; //get bias
    for (int i = 0; i < n_features; i++) {{
        res += features[i] * thetas[i + 1]; // move
    }}
    return res;
}}

int main() {{
    float predict_value = {{{predict_value}}};
    float get_prediction[1] = {{predict_value}};
    float predict = linear_regression_prediction(get_prediction, 1);
    printf("For %f years of experience, the salary would be around %f\\n", predict_value,predict);
}}
"""

    f = open("fichier.c", "w")
    f.write(c)

    if (os.system("gcc fichier_logistic.c -o predict")):
        # If can't compile
        print("Use this command to compile the c file: gcc fichier.c -o predict")

def generate_for_logistic(joblib_file, predict_value):
    model = joblib.load(joblib_file)
    thetas_list = []
    thetas_list.append(model.intercept_[0])  # bias is at index 0, get 1st bias value
    len_thetas = 1
    coefs = model.coef_[0] # get first array of coefs
    for coef in coefs:
        thetas_list.append(coef)
        len_thetas += 1

    # build theta list as string
    thetas = "{"
    for i in thetas_list:
        thetas += str(i) + ", "
    thetas = thetas[:-2] # remove last ", "
    thetas += "}"

    # build predict strings
    a, b = predict_value
    get_predict_value = "{"
    get_predict_value += str(a) + ", " + str(b)
    get_predict_value += "}"

    # Create and write .c file with values defined above
    c = f"""#include <stdio.h>
    
float thetas[{len_thetas}] = {thetas};
float factorial(int n) {{
    float f = 1;
    int i = 1;
    while (i <= n) {{
        f *= i;
        i++;
    }}
    return f;
}}

float power(float b, int e) {{
    float res = 1;
    if (e == 0) {{
        return 1;
    }}
    while (e > 0) {{
        res *= b;
        e--;
    }}
    return res;
}}

float exp_approx(float x, int n_term) {{
    float res = 0;
    for (int i = 0; i <= n_term; i++) {{
        float p = power(x, i);
        float fact = factorial(i);
        res += p / fact;
    }}
    return res;
}}

float sigmoid(float x) {{
    float e = exp_approx(-x, 10);
    return 1 / (1 + e);
}}

float linear_regression_prediction(float *features, int n_thetas) {{
    float res = thetas[0]; //get bias
    for (int i = 0; i < n_features; i++) {{
        res += features[i] * thetas[i + 1]; // move
    }}
    return res;
}}

float logistic_regression(float *features, int n_features) {{
    float pred = sigmoid(linear_regression_prediction(features, theta, n_features));
    if (pred <= 0.5) {{
        return 0.0;
    }}
    else {{
        return 1.0;      
    }}
}}

int main() {{
    float get_prediction[2] = {get_predict_value};
    float predict = logistic_regression(get_prediction, 2);
    if (predict == 1) {{
        printf("For weight %f and height %f, that person seems to be male\\n", get_prediction[0], get_prediction[1]);
    }}
    else {{
        printf("For weight %f and height %f, that person seems to be female\\n", get_prediction[0], get_prediction[1]);
    }}
}}
"""

    f = open("fichier_logistic.c", "w")
    f.write(c)

    if (os.system("gcc fichier_logistic.c -o predict")):
        # Can't compile
        print("Use this command to compile the c file: gcc fichier_logistic.c -o predict_logistic")

def generate_predict_in_c(joblib_file, predict_value, type):
    if str.lower(type) == "linear":
        generate_for_linear(joblib_file, predict_value)
    elif str.lower(type) == "logistic":
        generate_for_logistic(joblib_file, predict_value)
    else:
        print("Specify linear or logistic")


train_and_joblib_linear_regression()
train_and_joblib_logistic_regression()

# Predict values are arbitrary, change them either here or in the .c file
generate_predict_in_c("linearRegressor.joblib", 5, "linear")
generate_for_logistic("logisticRegressor.joblib", (50, 160))