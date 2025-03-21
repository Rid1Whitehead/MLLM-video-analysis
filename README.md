# Multimodal Large Language Models for Posture Analysis in Collaborative Learning from Video

This repository contains the companion code for the paper:

**Utilizing Multimodal Large Language Models for Video Analysis of Posture in Studying Collaborative Learning: A Case Study**  
*Ridwan Whitehead, Andy Nguyen, & Sanna Järvelä (2025)*
*(Published: 19 March 2025)*

https://doi.org/10.18608/jla.2025.8595

The code demonstrates methods for analyzing images and videos to extract and annotate posture behaviors from collaborative learning settings using multimodal large language models (MLLMs).


---

![data pipeline drawio](https://github.com/user-attachments/assets/3b4a8799-423a-4a89-94ac-26380f4f7b7d)

---

## Repository Content

- **requirements.txt**  
  Lists the Python dependencies:
  - `requests`
  - `pandas`
  - `openpyxl`
  - `opencv-python`
  - `Ultralytics`

- **run_images_Azure_API.py**  
  An interactive script that processes images using the Azure API (via the GPT-4-vision-preview model). It supports:
  - Single image processing (printing the API response)
  - Batch processing (saving responses as JSON files)

- **run_images_openai_API.py**  
  Similar to the Azure script but uses the OpenAI API. It allows:
  - Processing a single image (with printed output)
  - Processing a directory of images (saving responses as JSON)

- **directory_json_to_excel.py**  
  Converts JSON output files (produced by the image processing scripts) into an Excel file. It:
  - Reads each JSON file to extract posture category information
  - Creates binary columns for each category (e.g., SIT, STD, ECP, ART, HTR, HFN, HTC, LTB, HRL)

- **html_json_output_visualization.py**  
  Generates an HTML file that visualizes the JSON outputs alongside their corresponding images. The script:
  - Scans a directory for JSON files and finds matching images
  - Creates an HTML file displaying each image with its JSON content for easy review

- **Extract_persons_with_ID.py**  
  Processes video files to extract individual persons using a YOLO model. This script:
  - Loads a pre-trained YOLO model (default: `yolov8n-pose.pt`)
  - Processes a video (e.g., `example_video.mp4`) by tracking objects every N-th frame
  - Crops detected objects and saves them to an output directory

- **yolov8n-pose.pt**  
  A pre-trained YOLO model used by `Extract_persons_with_ID.py` for pose estimation.

- **example_video.mp4**
  A sample video file to test the video processing script.

---

## Installation

1. **Python 3**  
   Ensure Python 3 is installed on your system.

2. **Install Dependencies**  
   Install the required packages by running:
   ```
   pip install -r requirements.txt
   ```

3. **API Keys**  
   If you plan to use the image processing scripts, have your Azure and/or OpenAI API keys ready.

4. **Additional Files**  
   Make sure the YOLO model file (`yolov8n-pose.pt`) and the sample video (`example_video.mp4`) are in the expected locations (or update the script paths accordingly).

---

## Usage

### Azure API Image Analysis

Run the script:
```
python run_images_Azure_API.py
```
Follow the prompts to:
- Choose between single image or batch processing.
- Enter the API base URL, deployment name, API key, prompt text, and image file or directory path.

### OpenAI API Image Analysis

Run the script:
```
python run_images_openai_API.py
```
Follow the interactive prompts similar to the Azure API script to process images.

### Converting JSON to Excel

1. Update the paths in `directory_json_to_excel.py` (set your JSON output directory and desired Excel file name).
2. Run the script:
   ```
   python directory_json_to_excel.py
   ```

### HTML Visualization of JSON Output

1. Set the appropriate directory paths in `html_json_output_visualization.py` for your JSON files and images.
2. Run the script:
   ```
   python html_json_output_visualization.py
   ```
An HTML file will be generated displaying each image along with its corresponding JSON output.

### Video Processing with YOLO

Run the script:
```
python Extract_persons_with_ID.py
```
Follow the prompts to:
- Specify the YOLO model file path (default: `yolov8n-pose.pt`)
- Provide the video file path (default: `example_data/example_video.mp4`)
- Set the frame interval and output directory for the cropped images

---

## License

This project is licensed under the GNU General Public License v3.0 (GPL-3.0).

---

## Example prompt

This prompt was the one used in the study this code was use for. Here is the complete prompt:

"Analyze the image provided and categorize the visible actions and postures according to the following list. The image should be scanned for the individuals’body language. You are to identify and list only the categories that apply to each individual depicted in the image. Ensure no explanations or elaborations are included—only list the categories that are clearly observed in the image. Categories to Identify: Sitting (SIT), Standing (STD), engaged with computer peripherals (ECP), One or two arms resting on table (ART), Hands holding task-related object (HTR), One or two hands on face/neck/ear area (HFN), Hands touching each other/clasped OR hand(s) touching their arm (HTC), Leaning on table with one or both hands (LTB), one or both hands resting on laps (HRL). Begin bydetermining if they are sitting or standing. Once the posture is established, focus on the placement and activity of the hands and arms. Check where the hands are placed in comparison to the keyboard and mouse, if any. The categories are only applicable iftheir hands are directly engaged with them. Pay attention to the resting position of the arms, whether on a table or elsewhere. Look for any objects that might be held in the hands and are relevant to the task at hand. These would include, stationary, paper, balls, etc. Evaluate the facial area to determine if hands are present there. Identify if hands are in contact with each other, suggesting clasping or other forms of touch. Check if there are any hands resting on their lap. Check if they are giving their weight on the table with their hands. The result should be the short version of their names listed. Example: SIT, HTR, LTB."

---

## Citation

If you use this code in your research, please cite the accompanying paper:  
*Whitehead, R., Nguyen, A., & Järvelä, S. (2025). Utilizing Multimodal Large Language Models for Video Analysis of Posture in Studying Collaborative Learning: A Case Study. Journal of Learning Analytics, 1-15. https://doi.org/10.18608/jla.2025.8595*

---

## Acknowledgments

This repository is provided as companion code for the above-mentioned article. For further details and background, please refer to the published paper.

---
