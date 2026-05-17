"""
LLM Client Module - Handles interaction with OpenAI API

This module abstracts away the OpenAI API call logic so app.py can focus on UI.
It loads the system prompt, sends user input to GPT-4o-mini, and parses the JSON response.
"""

import os
import json
import re
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

class PolicyAnalyzer:
    """
    A helper class to interact with OpenAI's API for policy analysis.
    
    Usage:
        analyzer = PolicyAnalyzer()
        result = analyzer.analyze_policy(policy_text)
        print(result)
    """
    
    def __init__(self):
        """Initialize the OpenAI client and load the system prompt."""
        # Get API key from environment variable
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY not found in .env file. "
                "Please copy .env.example to .env and add your API key."
            )
        
        # Initialize OpenAI client
        self.client = OpenAI(api_key=api_key)
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        
        # Load system prompt from file
        try:
            with open("docs/system_prompt.md", "r") as f:
                self.system_prompt = f.read()
        except FileNotFoundError:
            print("Warning: docs/system_prompt.md not found. Using inline system prompt.")
            self.system_prompt = self._default_system_prompt()
    
    @staticmethod
    def _default_system_prompt():
        """Fallback system prompt if file not found."""
        return """You are an expert educational data analyst assistant.
Your job: Parse charter school policy changes and extract structured data.
Output ONLY valid JSON with no additional text."""
    
    def analyze_policy(self, policy_text: str) -> dict:
        """
        Send a policy update to OpenAI and get structured analysis.
        
        Args:
            policy_text (str): The policy or rule update to analyze
            
        Returns:
            dict: Parsed JSON response from the LLM
            
        Raises:
            ValueError: If the response is not valid JSON
        """
        try:
            # Create message to send to OpenAI
            # The system prompt tells the model HOW to respond
            # The user message is the policy to analyze
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": self.system_prompt
                    },
                    {
                        "role": "user",
                        "content": policy_text
                    }
                ],
                temperature=0.3,  # Lower temperature = more consistent, deterministic output
                max_tokens=500    # Limit response length to keep costs down
            )
            
            # Extract the text response from OpenAI
            response_text = response.choices[0].message.content
            
            # Try to parse as JSON
            # Sometimes the model might add text before/after JSON, so we extract it
            parsed_response = self._extract_json(response_text)
            
            return parsed_response
            
        except json.JSONDecodeError as e:
            raise ValueError(
                f"OpenAI response was not valid JSON. "
                f"Response: {response_text[:200]}... Error: {str(e)}"
            )
        except Exception as e:
            raise Exception(f"Error calling OpenAI API: {str(e)}")
    
    @staticmethod
    def _extract_json(text: str) -> dict:
        """
        Extract JSON from text response (handles cases where model adds extra text).
        
        Args:
            text (str): Raw response text from OpenAI
            
        Returns:
            dict: Parsed JSON object
        """
        # Try to find JSON object in the text (handles markdown code blocks, etc.)
        # Look for first { and last }
        start_idx = text.find("{")
        end_idx = text.rfind("}")
        
        if start_idx != -1 and end_idx != -1:
            json_str = text[start_idx:end_idx + 1]
            return json.loads(json_str)
        else:
            # If no JSON found, try parsing the whole text
            return json.loads(text)
