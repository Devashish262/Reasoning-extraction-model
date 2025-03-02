import re
import os
import json
import requests
from typing import Dict, List, Optional, Union
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

class ReasoningExtractor:
    """
    A class that extracts and enhances reasoning processes using AI models.
    
    This class leverages the DeepSeek and OpenAI APIs to:
    1. Generate reference material from DeepSeek
    2. Use that reference to create a comprehensive answer with GPT-3.5 Turbo
    """
    
    # Demo/test API keys placeholders - these will be replaced with env vars
    DEMO_OPENAI_KEY = "demo-openai-key-placeholder"
    DEMO_DEEPSEEK_KEY = "demo-deepseek-key-placeholder"
    
    def __init__(self, use_demo_keys: bool = False):
        """
        Initialize the ReasoningExtractor with API keys.
        Will try to load from environment variables first, then fall back to demo keys if specified.
        
        Args:
            use_demo_keys (bool): If True, use demo keys for testing. Default False.
        """
        if use_demo_keys:
            self.openai_api_key = self.DEMO_OPENAI_KEY
            self.deepseek_api_key = self.DEMO_DEEPSEEK_KEY
            print("WARNING: Using demo keys. These are placeholders and will not work for actual API calls.")
        else:
            # Try to get from environment variables
            self.openai_api_key = os.getenv('OPENAI_API_KEY')
            self.deepseek_api_key = os.getenv('DEEPSEEK_API_KEY')
            
            # If environment variables not found, raise error
            if not self.openai_api_key or not self.deepseek_api_key:
                raise ValueError(
                    "API keys not found in environment variables. "
                    "Set OPENAI_API_KEY and DEEPSEEK_API_KEY environment variables "
                    "or initialize with use_demo_keys=True for testing."
                )

    def is_demo_mode(self) -> bool:
        """Check if running in demo mode with test keys."""
        return self.openai_api_key == self.DEMO_OPENAI_KEY

    def get_deepseek_response(self, prompt: str) -> str:
        """
        Get response from DeepSeek API focusing only on reasoning.
        
        Args:
            prompt (str): The input prompt for DeepSeek

        Returns:
            str: DeepSeek's reasoning response
        """
        headers = {
            "Authorization": f"Bearer {self.deepseek_api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": "You are an AI assistant that provides clear step-by-step reasoning. Focus on explaining the thinking process and logical steps in a natural, flowing manner."},
                {"role": "user", "content": f"""
                Explain your reasoning process for this question in a natural, flowing way:
                {prompt}
                
                Provide your thinking as a coherent narrative, walking through your reasoning steps naturally without using bullet points, section headers, or artificial structure. Just explain your thought process as you would in a conversation, moving from understanding the question to analyzing it and finally reaching a conclusion.
                """}
            ],
            "temperature": 0.7,
            "max_tokens": 1000
        }
        
        try:
            response = requests.post(
                "https://api.deepseek.com/v1/chat/completions",
                headers=headers,
                json=data,
                verify=True
            )
            
            if response.status_code != 200:
                raise Exception(f"DeepSeek API error: {response.text}")
                
            full_response = response.json()["choices"][0]["message"]["content"]
            print("DeepSeek Response:")
            print(full_response)
            
            # Return the full response with no filtering
            return full_response
            
        except requests.exceptions.RequestException as e:
            print(f"Request error: {str(e)}")
            raise Exception(f"Failed to connect to DeepSeek API: {str(e)}")
        except Exception as e:
            print(f"General error: {str(e)}")
            raise

    def process_with_gpt(self, reasoning: str) -> Dict[str, str]:
        """
        Process extracted reasoning using DeepSeek R1 model.
        In demo mode, returns a mock response.
        
        Args:
            reasoning (str): Extracted reasoning text

        Returns:
            Dict[str, str]: Processed results
        """
        if self.is_demo_mode():
            # Return mock response for testing
            return {
                "original_reasoning": reasoning,
                "enhanced_reasoning": f"""
                [DEMO MODE - Mock Analysis]
                Analysis of the reasoning:
                1. Logical Structure: Clear step-by-step approach
                2. Improvements: Could add more specific examples
                3. Confidence Score: 85%
                
                Note: This is a demo analysis. For actual DeepSeek R1 analysis, please provide a valid API key.
                
                Enhanced version:
                {reasoning}
                With additional context and examples...
                """,
                "status": "success"
            }
            
        headers = {
            "Authorization": f"Bearer {self.deepseek_api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "deepseek-ai/deepseek-coder-33b-instruct",
            "messages": [
                {"role": "system", "content": "You are an AI assistant focused on analyzing and improving logical reasoning."},
                {"role": "user", "content": f"""
                Analyze and enhance the following reasoning:
                
                {reasoning}
                
                Please provide:
                1. An evaluation of the logical structure
                2. Any potential improvements or expansions
                3. A confidence score for the reasoning
                """}
            ],
            "temperature": 0.7,
            "max_tokens": 1000
        }
        
        try:
            response = requests.post(
                "https://api.deepseek.ai/v1/chat/completions",
                headers=headers,
                json=data
            )
            
            if response.status_code != 200:
                raise Exception(f"DeepSeek API error: {response.text}")
                
            return {
                "original_reasoning": reasoning,
                "enhanced_reasoning": response.json()["choices"][0]["message"]["content"],
                "status": "success"
            }
            
        except Exception as e:
            return {
                "original_reasoning": reasoning,
                "error": str(e),
                "status": "error"
            }

    def extract_reasoning(self, text: str) -> Optional[str]:
        """Extract reasoning sections from text."""
        reasoning_patterns = [
            r"Let's think about this step by step:(.*?)(?=\n\n|$)",
            r"Here's my reasoning:(.*?)(?=\n\n|$)",
            r"Reasoning:(.*?)(?=\n\n|$)",
            r"Let me break this down:(.*?)(?=\n\n|$)"
        ]
        
        for pattern in reasoning_patterns:
            match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
            if match:
                return match.group(1).strip()
                
        paragraphs = text.split('\n\n')
        for para in paragraphs:
            if any(marker in para.lower() for marker in 
                ['because', 'therefore', 'thus', 'since', 'as a result']):
                return para.strip()
                
        return None

    def enhance_with_chatgpt(self, reasoning: str) -> str:
        """
        Enhance the reasoning using ChatGPT API.
        
        Args:
            reasoning (str): The initial reasoning from DeepSeek

        Returns:
            str: Enhanced reasoning from ChatGPT
        """
        headers = {
            "Authorization": f"Bearer {self.openai_api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "You are an expert at analyzing and improving reasoning processes. Your task is to enhance and expand upon the given reasoning while maintaining its logical structure."},
                {"role": "user", "content": f"""
                Here is a reasoning process that needs enhancement:

                {reasoning}

                Please improve this reasoning by:
                1. Adding more depth to each logical step
                2. Including relevant examples or analogies
                3. Explaining the connections between steps more clearly
                4. Adding any missing considerations
                5. Strengthening the conclusion

                Keep the same step-by-step structure but make it more comprehensive and insightful.
                """}
            ],
            "temperature": 0.7,
            "max_tokens": 2000
        }
        
        try:
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=data
            )
            
            if response.status_code != 200:
                raise Exception(f"ChatGPT API error: {response.text}")
                
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"ChatGPT enhancement error: {str(e)}")
            raise

    def get_gpt_answer(self, reasoning: str, original_prompt: str) -> str:
        """
        Get final answer from ChatGPT based on DeepSeek's reasoning.
        
        Args:
            reasoning (str): The reasoning from DeepSeek as reference material
            original_prompt (str): The original user prompt

        Returns:
            str: Final answer from ChatGPT
        """
        # Use the DeepSeek response as reference
        headers = {
            "Authorization": f"Bearer {self.openai_api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "You are an expert at providing clear, direct answers to questions with the help of references."},
                {"role": "user", "content": f"""
                I need you to answer this question: "{original_prompt}"

                Please use the following reference to help you craft a comprehensive answer:

                REFERENCE:
                {reasoning}

                Your task is to directly answer the question asked. Use the reference material to inform your answer, 
                but respond in your own words in a natural, conversational style. Don't mention that you're using a reference.
                Just provide a clear, helpful answer to the question as if you're having a conversation.
                """}
            ],
            "temperature": 0.7,
            "max_tokens": 1000
        }
        
        try:
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=data
            )
            
            if response.status_code != 200:
                raise Exception(f"ChatGPT API error: {response.text}")
            
            gpt_response = response.json()["choices"][0]["message"]["content"]
            print("GPT Response:")
            print(gpt_response)
            
            return gpt_response
        except Exception as e:
            print(f"ChatGPT answer error: {str(e)}")
            raise

    def process_complete_pipeline(self, user_prompt: str) -> Dict[str, Union[str, Dict]]:
        """Run reasoning pipeline with final answer from ChatGPT."""
        results = {
            "timestamp": datetime.now().isoformat(),
            "original_prompt": user_prompt,
            "pipeline_status": "initialized"
        }
        
        try:
            # Get reference material from DeepSeek
            print(f"Getting reference material from DeepSeek for prompt: {user_prompt[:100]}...")
            reference_material = self.get_deepseek_response(user_prompt)
            
            if not reference_material or len(reference_material.strip()) == 0:
                results["pipeline_status"] = "failed"
                results["error"] = "No reference material received from DeepSeek API"
                return results
            
            results["reference_material"] = reference_material
            
            # Get answer from ChatGPT using the reference
            print("Getting answer from ChatGPT using the reference material...")
            try:
                final_answer = self.get_gpt_answer(reference_material, user_prompt)
                results["final_answer"] = final_answer
                results["pipeline_status"] = "completed"
            except Exception as e:
                print(f"Getting answer from ChatGPT failed: {str(e)}")
                results["error"] = f"Answer generation failed: {str(e)}"
                results["pipeline_status"] = "partial"
                
        except Exception as e:
            error_msg = str(e)
            print(f"Pipeline error: {error_msg}")
            results["pipeline_status"] = "failed"
            results["error"] = f"Error processing request: {error_msg}"
            
            if "Failed to connect" in error_msg:
                results["error"] += ". Please check your internet connection and API keys."
            
        return results

    def save_results(self, results: Dict, filepath: str) -> None:
        """Save results to JSON file."""
        with open(filepath, 'w') as f:
            json.dump(results, f, indent=2)