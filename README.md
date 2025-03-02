# Reasoning Extractor

## Overview

The Reasoning Extractor is a Python-based tool designed to extract and enhance reasoning processes using AI models. It leverages the DeepSeek and OpenAI APIs to provide clear, step-by-step reasoning and enhanced logical analysis.

## Features

- Extracts reasoning from text using predefined patterns.
- Enhances reasoning with additional context and examples using ChatGPT.
- Provides a final answer based on the enhanced reasoning.
- Supports demo mode with mock API responses for testing.

## Setup

### Prerequisites

- Python 3.6 or higher
- An internet connection for API requests
- API keys for OpenAI and DeepSeek

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Devashish262/Reasoning-extraction-model.git
   cd Reasoning-extraction-model
   ```

2. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up your environment variables for the API keys:

   - Copy the `.env.example` file to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Edit the `.env` file and add your API keys:
     ```
     OPENAI_API_KEY=your-openai-api-key
     DEEPSEEK_API_KEY=your-deepseek-api-key
     ```

## Usage

### Web Interface

1. Start the Flask web server:

   ```bash
   python app.py
   ```

2. Open your browser and navigate to:

   ```
   http://127.0.0.1:5000
   ```

3. Enter your prompt in the text field and click "Analyze"

### Command Line Interface

Run the model from the command line:

```bash
python run_with_keys.py
```

You can also specify a prompt directly:

```bash
python run_with_keys.py --prompt "Explain the concept of quantum computing."
```

If you don't have API keys set up, you can run in demo mode:

```bash
python run_with_keys.py --demo
```

## API Key Security

This project requires API keys from OpenAI and DeepSeek. To keep your keys secure:

1. Never commit your `.env` file to version control
2. The `.gitignore` file is configured to exclude the `.env` file
3. Use environment variables in production environments
4. Rotate your API keys periodically

## GitHub Setup

To push this project to your own GitHub repository:

1. Make sure you have Git installed
2. Run the setup script:

   ```bash
   python setup_github.py --remote https://github.com/yourusername/your-repo-name.git
   ```

3. The script will:
   - Initialize a Git repository if needed
   - Add all files to the repository
   - Create an initial commit
   - Add the specified remote repository
   - Push the code to GitHub

## Demo Mode

The demo mode uses mock API responses for testing purposes. It is useful for development and testing without incurring API costs.

## Error Handling

- Ensure that your API keys are correctly set in the environment variables.
- Check your internet connection if you encounter connection errors.

## License

This project is for demonstration purposes only. Do not use the demo API keys in production.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## Contact

For questions or support, please contact [your-email@example.com]. 