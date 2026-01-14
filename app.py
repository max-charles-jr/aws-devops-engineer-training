from flask import Flask, jsonify, render_template_string
import os

app = Flask(__name__)

# HTML template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>AWS DevOps Demo App</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            background-color: #f0f0f0;
        }
        .container {
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #232f3e;
        }
        .status {
            color: #28a745;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 AWS DevOps Demo Application</h1>
        <p class="status">✓ Application is running successfully!</p>
        <p><strong>Environment:</strong> {{ env }}</p>
        <p><strong>Version:</strong> 1.0.0</p>
        <hr>
        <p>This is a sample Python Flask application for AWS CodeBuild and CI/CD pipeline testing.</p>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    environment = os.getenv('ENVIRONMENT', 'development')
    return render_template_string(HTML_TEMPLATE, env=environment)

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'service': 'aws-devops-demo',
        'version': '1.0.0'
    }), 200

@app.route('/api/info')
def info():
    return jsonify({
        'application': 'AWS DevOps Demo',
        'environment': os.getenv('ENVIRONMENT', 'development'),
        'version': '1.0.0'
    })

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
