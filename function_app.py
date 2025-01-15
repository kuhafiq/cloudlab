import azure.functions as func
import logging
import math
import json

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

# Numerical integration function
def numerical_integration(func, lower, upper, n):
    dx = (upper - lower) / n
    total_area = 0
    for i in range(n):
        x = lower + i * dx
        total_area += func(x) * dx
    return total_area

# Numerical integration service route
@app.route(route="numericalintegralservice")
def numerical_integration_service(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Numerical integration service request received.')

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
