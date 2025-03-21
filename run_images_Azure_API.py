#!/usr/bin/env python3
"""
interactive_azure_api_image_analysis.py

This script interactively gathers parameters from the user to process images using the Azure API.
You can choose to process a single image or a whole directory (batch mode).
For single images, the API response is printed.
For batch mode, responses are saved as JSON files in the specified output directory.

Requirements:
    pip install requests
"""

import os
import time
import requests
import json
import base64

def encode_image_to_base64(image_path):
    """Encodes a local image file to base64."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def process_single_image(api_base, deployment_name, API_KEY, prompt_text, image_path):
    """Processes a single image through the API and prints the response."""
    image_base64 = encode_image_to_base64(image_path)
    base_url = f"{api_base.rstrip('/')}/openai/deployments/{deployment_name}"
    headers = {
        "Content-Type": "application/json",
        "api-key": API_KEY
    }
    endpoint = f"{base_url}/chat/completions?api-version=2023-12-01-preview"

    data = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant"},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt_text},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_base64}",
                            "detail": "high"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 500
    }

    try:
        response = requests.post(endpoint, headers=headers, data=json.dumps(data))
        print(f"Status Code: {response.status_code}")
        print(response.text)
    except Exception as e:
        print(f"Error processing image: {e}")

def process_image(api_base, deployment_name, API_KEY, prompt_text, image_path, output_directory):
    """Processes an image through the API and saves the response as JSON."""
    image_base64 = encode_image_to_base64(image_path)
    base_url = f"{api_base.rstrip('/')}/openai/deployments/{deployment_name}"
    headers = {
        "Content-Type": "application/json",
        "api-key": API_KEY
    }
    endpoint = f"{base_url}/chat/completions?api-version=2023-12-01-preview"

    data = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant"},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt_text},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_base64}",
                            "detail": "high"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300,
        "temperature": 0.1
    }

    success = False
    retries = 5
    wait_time = 10  # seconds

    while not success and retries > 0:
        try:
            response = requests.post(endpoint, headers=headers, data=json.dumps(data))
            response.raise_for_status()
            success = True
        except requests.exceptions.HTTPError as e:
            if response.status_code == 429:  # Too Many Requests
                print(f"Rate limit exceeded for image '{image_path}'. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
                retries -= 1
            else:
                print(f"Error processing image '{image_path}': {e}")
                return None

    if not success:
        print(f"Failed to process image '{image_path}' after multiple retries.")
        return None

    output_filename = f"{os.path.splitext(os.path.basename(image_path))[0]}.json"
    output_filepath = os.path.join(output_directory, output_filename)

    try:
        with open(output_filepath, 'w') as output_file:
            json.dump(response.json(), output_file, indent=4)
        print(f"Output saved to {output_filepath}")
    except Exception as e:
        print(f"Error saving output for image '{image_path}': {e}")

def process_directory(api_base, deployment_name, API_KEY, prompt_text, directory_path, output_directory):
    """Processes all images in a directory and saves outputs as JSON files with throttling."""
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    images_processed = 0
    batch_start_time = time.time()
    for entry in os.scandir(directory_path):
        if entry.is_file() and entry.name.lower().endswith(('.png', '.jpg', '.jpeg')):
            process_image(api_base, deployment_name, API_KEY, prompt_text, entry.path, output_directory)
            images_processed += 1
            time.sleep(1)  # Delay between requests to respect rate limits
            if images_processed % 20 == 0:
                elapsed_time = time.time() - batch_start_time
                if elapsed_time < 60:
                    time.sleep(60 - elapsed_time)
                batch_start_time = time.time()
    
    if images_processed % 20 != 0:
        elapsed_time = time.time() - batch_start_time
        if elapsed_time < 60:
            time.sleep(60 - elapsed_time)

def main():
    print("=== Azure API Image Analysis Interactive Script ===")
    print("Select mode:")
    print("1. Process a single image")
    print("2. Process a directory of images (batch mode)")
    mode = input("Enter 1 or 2: ").strip()

    # Gather common parameters
    api_base = input("Enter the API base URL (default: https://api.openai.azure.com/): ").strip()
    if not api_base:
        api_base = "https://api.openai.azure.com/"

    deployment_name = input("Enter the deployment name (default: gpt-4o): ").strip()
    if not deployment_name:
        deployment_name = "gpt-4o"

    API_KEY = input("Enter your API key: ").strip()
    prompt_text = input("Enter the prompt text (default: your_prompt_here): ").strip()
    if not prompt_text:
        prompt_text = "your_prompt_here"

    if mode == "1":
        image_path = input("Enter the path to the image file: ").strip()
        if not os.path.exists(image_path):
            print(f"Image file '{image_path}' does not exist.")
            return
        process_single_image(api_base, deployment_name, API_KEY, prompt_text, image_path)
    elif mode == "2":
        directory_path = input("Enter the directory path containing images: ").strip()
        if not os.path.isdir(directory_path):
            print(f"Directory '{directory_path}' does not exist.")
            return
        output_directory = input("Enter the output directory for JSON files (default: output): ").strip()
        if not output_directory:
            output_directory = "output"
        os.makedirs(output_directory, exist_ok=True)
        process_directory(api_base, deployment_name, API_KEY, prompt_text, directory_path, output_directory)
    else:
        print("Invalid mode selected. Please enter 1 or 2.")

if __name__ == '__main__':
    main()
