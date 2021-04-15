# titanic-predict-prob-custom-container
This is an example of using Custom containers for preduction
The model is a scikit learn model wrapped in a FastAPI service.
You can pass a parameter to request probabilities instead of just the preduction
using .predict_proba()

The example model used is a titanic model trained using an SVC algorithm.

The request payload is:
```python
{
    "instances": [
        ["female", 43.0, 211.3375, 1, "S", "St Louis, MO", 1, 0], ["male", 56.0, 35.5, 1, "C", "Basel, Switzerland", 0, 0]
    ],
    "parameters": {
        "predict_proba": true
    }
}
```