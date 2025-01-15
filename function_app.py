import azure.functions as func
import logging
from microservice import numerical_integration
import json
import math

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="numericalintegralservice")
def http_example(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Extract 'lower' and 'upper' from query parameters
    try:
        lower = float(req.params.get('lower'))
        upper = float(req.params.get('upper'))
    except (TypeError, ValueError):
        return func.HttpResponse(
            "Invalid or missing query parameters. Please provide 'lower' and 'upper'.",
            status_code=400
        )

    # Define the range of N values for integration
    n_values = [10, 100, 1000, 10000, 100000, 1000000]
    results = {}
    for n in n_values:
        result = numerical_integration(lambda x: abs(math.sin(x)), lower, upper, n)
        results[f'N={n}'] = result

    # Return the results as a JSON response
    return func.HttpResponse(
        json.dumps(results),
        mimetype="application/json",
        status_code=200
    )