from index2 import ReasoningExtractor
import os
import json

def check_api_keys():
    """Check if the required API keys are available."""
    openai_key = os.getenv('OPENAI_API_KEY')
    deepseek_key = os.getenv('DEEPSEEK_API_KEY')
    
    if not openai_key:
        print("WARNING: OPENAI_API_KEY environment variable is not set.")
    if not deepseek_key:
        print("WARNING: DEEPSEEK_API_KEY environment variable is not set.")
    
    return bool(openai_key and deepseek_key)

def print_demo_warning():
    """Print warning about using demo keys."""
    print("\n" + "="*80)
    print("DEMO MODE WARNING")
    print("="*80)
    print("You are running in demo mode with placeholder API keys.")
    print("These demo keys are not valid and are provided for demonstration purposes only.")
    print("\nTo use this model properly, you need to:")
    print("1. Obtain valid API keys from OpenAI and DeepSeek")
    print("2. Set them as environment variables:")
    print("   - OPENAI_API_KEY='your-openai-api-key'")
    print("   - DEEPSEEK_API_KEY='your-deepseek-api-key'")
    print("\nOr modify the code to use your actual API keys.")
    print("="*80 + "\n")

def main():
    # Check for environment variables
    has_api_keys = check_api_keys()
    
    # Print demo warning if no real API keys are found
    if not has_api_keys:
        print_demo_warning()
    
    # Initialize the extractor
    use_demo = not has_api_keys
    try:
        print(f"Initializing Reasoning Extractor {'with demo keys' if use_demo else 'with environment variables'}")
        extractor = ReasoningExtractor(use_demo_keys=use_demo)
        
        # Define a sample prompt
        user_prompt = "Explain the concept of machine learning in simple terms."
        
        # Run the complete reasoning pipeline
        print(f"Processing prompt: {user_prompt}")
        results = extractor.process_complete_pipeline(user_prompt)
        
        # Print the results
        print("\nResults:")
        print(f"Pipeline status: {results['pipeline_status']}")
        
        if results['pipeline_status'] == 'failed':
            print(f"Error: {results.get('error', 'Unknown error')}")
        else:
            if 'reasoning_process' in results:
                print("\nReasoning process:")
                print(results['reasoning_process'])
            if 'final_answer' in results:
                print("\nFinal answer:")
                print(results['final_answer'])
        
        # Save results to a file
        output_file = 'reasoning_results.json'
        extractor.save_results(results, output_file)
        print(f"\nResults saved to {output_file}")
        
        # Also print the saved results for inspection
        print("\nSaved results (JSON format):")
        with open(output_file, 'r') as f:
            saved_data = json.load(f)
            print(json.dumps(saved_data, indent=2))
    
    except Exception as e:
        print(f"Error running Reasoning Extractor: {str(e)}")
        print("\nPlease ensure you have:")
        print("1. Valid API keys for OpenAI and DeepSeek")
        print("2. Proper internet connection")
        print("3. All required dependencies installed")

if __name__ == "__main__":
    main() 