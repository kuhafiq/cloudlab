from flask import Flask, jsonify
import math

app = Flask(__name__)

def numerical_integration(func, lower, upper, n):
    dx = (upper - lower) / n
    total_area = 0
    for i in range(n):
        x = lower + i * dx
        total_area += func(x) * dx
    return total_area

@app.route('/numericalintegralservice/<lower>/<upper>', methods=['GET'])
def integrate_service(lower, upper):
    # Convert inputs to float
    lower = float(lower)
    upper = float(upper)
    
    n_values = [10, 100, 1000, 10000, 100000, 1000000]
    results = {}
    for n in n_values:
        result = numerical_integration(lambda x: abs(math.sin(x)), lower, upper, n)
        results[f'N={n}'] = result
    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)

