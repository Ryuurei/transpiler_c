#include <stdio.h>

float thetas[2] = {25792.20019866871, 9449.962321455074};

float linear_regression_prediction(float *features, int n_features) {
    float res = thetas[0]; //get bias
    for (int i = 0; i < n_features; i++) {
        res += features[i] * thetas[i + 1]; // move
    }
    return res;
}

int main() {
    float predict_value = {5};
    float get_prediction[1] = {predict_value};
    float predict = linear_regression_prediction(get_prediction, 1);
    printf("For %f years of experience, the salary would be around %f\n", predict_value,predict);
}
