import os
import json
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from index2 import ReasoningExtractor
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize the extractor using environment variables
extractor = ReasoningExtractor(use_demo_keys=False)

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/api/process', methods=['POST'])
def process():
    """Process the user prompt and return results."""
    user_prompt = request.json.get('prompt', '')
    
    if not user_prompt:
        return jsonify({
            'status': 'error',
            'message': 'No prompt provided'
        }), 400
    
    try:
        # Process the prompt
        results = extractor.process_complete_pipeline(user_prompt)
        
        # Save results to a file
        output_file = 'reasoning_results.json'
        extractor.save_results(results, output_file)
        
        return jsonify(results)
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/results')
def get_results():
    """Get the latest results."""
    try:
        with open('reasoning_results.json', 'r') as f:
            results = json.load(f)
        return jsonify(results)
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Could not load results: {str(e)}'
        }), 500

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    
    # Check if API keys are set
    if not os.getenv('OPENAI_API_KEY') or not os.getenv('DEEPSEEK_API_KEY'):
        print("WARNING: API keys not found in environment variables.")
        print("Set OPENAI_API_KEY and DEEPSEEK_API_KEY environment variables before running.")
        print("You can create a .env file with these variables for local development.")
    else:
        print("API Keys configured from environment variables.")
    
    print("\nStarting Flask server on http://127.0.0.1:5000")
    app.run(debug=True) 