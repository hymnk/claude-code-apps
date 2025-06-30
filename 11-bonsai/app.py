from flask import Flask, render_template
import random

app = Flask(__name__)

@app.route('/')
def index():
    # Generate random seed for client-side bonsai generation
    seed = random.randint(1, 1000000)
    return render_template('index.html', seed=seed)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)