#include <stdio.h>
    
float thetas[3] = {0.6925417780420726, -0.49261999102598536, 0.19834041900101915};
float factorial(int n) {
    float f = 1;
    int i = 1;
    while (i <= n) {
        f *= i;
        i++;
    }
    return f;
}

float power(float b, int e) {
    float res = 1;
    if (e == 0) {
        return 1;
    }
    while (e > 0) {
        res *= b;
        e--;
    }
    return res;
}

float exp_approx(float x, int n_term) {
    float res = 0;
    for (int i = 0; i <= n_term; i++) {
        float p = power(x, i);
        float fact = factorial(i);
        res += p / fact;
    }
    return res;
}

float sigmoid(float x) {
    float e = exp_approx(-x, 10);
    return 1 / (1 + e);
}

float linear_regression_prediction(float *features, int n_thetas) {
    float res = thetas[0]; //get bias
    for (int i = 0; i < n_features; i++) {
        res += features[i] * thetas[i + 1]; // move
    }
    return res;
}

float logistic_regression(float *features, int n_features) {
    float pred = sigmoid(linear_regression_prediction(features, theta, n_features));
    if (pred <= 0.5) {
        return 0.0;
    }
    else {
        return 1.0;      
    }
}

int main() {
    float get_prediction[2] = {50, 160};
    float predict = logistic_regression(get_prediction, 2);
    if (predict == 1) {
        printf("For weight %f and height %f, that person seems to be male\n", get_prediction[0], get_prediction[1]);
    }
    else {
        printf("For weight %f and height %f, that person seems to be female\n", get_prediction[0], get_prediction[1]);
    }
}
