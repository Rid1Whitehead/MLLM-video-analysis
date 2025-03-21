import os
import json

def generate_html(json_directory, image_directory, output_html_file):
    # Open the output HTML file
    with open(output_html_file, 'w') as html_file:
        # Write the HTML header
        html_file.write('<html><head><title>Vision Processing Evaluation</title></head><body>\n')
        
        # Iterate over JSON files and match with images
        for json_filename in os.listdir(json_directory):
            if json_filename.endswith('.json'):
                # Extract the base filename without extension
                base_filename = os.path.splitext(json_filename)[0]
                
                # Find the corresponding image
                image_filename = next((f for f in os.listdir(image_directory)
                                       if f.startswith(base_filename) and f.lower().endswith(('.png', '.jpg', '.jpeg'))), None)
                
                # If a corresponding image is found, display it with JSON data
                if image_filename:
                    image_path = os.path.join(image_directory, image_filename)
                    json_path = os.path.join(json_directory, json_filename)

                    # Write the image tag
                    html_file.write(f'<div><h2>{base_filename}</h2>\n')
                    html_file.write(f'<img src="{image_path}" alt="{base_filename}" style="max-width: 500px;"><br>\n')

                with open(json_path, 'r') as json_file:
                    content = json_file.read()  # Directly read the file content, which is expected to be a plain string

                    # Prepare the content for HTML display. If you still need to highlight something, you'd replace directly in 'content'
                    content_for_html = content.replace('\n', '<br>')  # Example of simple formatting, adjust as necessary

                    # Write the content into an HTML file
                    html_file.write(f'<div><pre>{content_for_html}</pre></div>\n')



    print(f"HTML file created at {output_html_file}")

# Specify the paths
json_directory_path = "your_JSON_directory_path"  # Replace with your JSON directory path
image_directory_path = "your_image_directory_path"  # Replace with your image directory path
output_html_file = "visualization_output_file_name.html"  # Replace with the path to your master file

# Generate the HTML file
generate_html(json_directory_path, image_directory_path, output_html_file)

