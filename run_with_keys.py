import os
import subprocess
import sys
import argparse
from index2 import ReasoningExtractor
from dotenv import load_dotenv

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Run the Reasoning Extractor model')
    parser.add_argument('--demo', action='store_true', help='Run in demo mode with placeholder keys')
    parser.add_argument('--prompt', type=str, help='The prompt to process')
    args = parser.parse_args()
    
    # Load environment variables from .env file if present
    load_dotenv()
    
    # Check if API keys are available in environment
    has_api_keys = bool(os.getenv('OPENAI_API_KEY') and os.getenv('DEEPSEEK_API_KEY'))
    
    # Determine whether to use demo mode
    use_demo = args.demo or not has_api_keys
    
    if use_demo:
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
        print("\nOr create a .env file in the project directory with these variables.")
        print("="*80 + "\n")
    else:
        print("Using API keys from environment variables.")
    
    try:
        # Initialize the ReasoningExtractor
        print(f"\nInitializing Reasoning Extractor {'with demo keys' if use_demo else 'with environment variables'}...")
        extractor = ReasoningExtractor(use_demo_keys=use_demo)
        
        # Get prompt from command line or user input
        if args.prompt:
            user_prompt = args.prompt
        else:
            # Default prompt
            default_prompt = "Explain the concept of machine learning in simple terms."
            
            # Allow user to input custom prompt
            user_input = input(f"\nEnter your prompt (press Enter to use default: '{default_prompt}'): ").strip()
            user_prompt = user_input if user_input else default_prompt
        
        print(f"\nProcessing prompt: {user_prompt}")
        results = extractor.process_complete_pipeline(user_prompt)
        
        # Print results
        print("\nResults:")
        print(f"Pipeline status: {results['pipeline_status']}")
        
        if results['pipeline_status'] == 'failed':
            print(f"Error: {results.get('error', 'Unknown error')}")
        else:
            if 'reference_material' in results:
                print("\nReference material:")
                print(results['reference_material'])
            if 'final_answer' in results:
                print("\nFinal answer:")
                print(results['final_answer'])
        
        # Save results to a file
        output_file = 'reasoning_results.json'
        extractor.save_results(results, output_file)
        print(f"\nResults saved to {output_file}")
        
    except Exception as e:
        print(f"\nError: {str(e)}")
        print("\nIf you're seeing API authentication errors, please verify that:")
        print("1. The API keys are correct and active")
        print("2. You have proper internet connectivity")
        print("3. The API service endpoints are functioning properly")

if __name__ == "__main__":
    main() 