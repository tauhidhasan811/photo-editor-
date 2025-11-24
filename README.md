# Image Editor

A Python-based image editor leveraging Google's Gemini API for advanced image manipulation. This project allows users to edit images based on textual prompts, offering functionalities such as resizing, cropping, and applying filters. It utilizes the Pillow library for core image processing and integrates with Langchain and Google Generative AI for AI-driven editing capabilities.

## Run Instructions

1.  **Clone the repository.**
2.  **Set up a virtual environment.**
    *   `python -m venv venv`
    *   `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (macOS/Linux)
3.  **Install dependencies.**
    *   `pip install -r requirements.txt`
4.  **Create a `.env` file** in the root directory and add your Google API key:
    *   `GOOGLE_API_KEY=YOUR_API_KEY`
5.  **Run the main script.**
    *   `python main.py`

## Folder Structure

```
root
|
---> .gitignore
|
---> check_api_avaiablities.py
|
---> LICENSE
|
---> main.py
|
---> README.md
|
---> requirements.txt
|
---> services
    |---> model.py
    |---> prompt.py
```

## File Descriptions

*   **`.gitignore`**: Specifies files and directories to be ignored by Git, including virtual environments, environment files, cached Python files, and `.png` images.
*   **`check_api_avaiablities.py`**: A script to check and list available Google AI models, their supported actions, and detailed information, loaded via an API key from a `.env` file.
*   **`LICENSE`**: Contains the terms and conditions of the Apache License, Version 2.0, governing the usage, reproduction, and distribution of the software.
*   **`main.py`**: The primary script for the image editor. It uses Google's Gemini API to edit images based on user prompts and displays the edited image using Matplotlib.
*   **`README.md`**: This file, providing an overview of the repository, its features, setup, and usage instructions.
*   **`requirements.txt`**: Lists all necessary Python libraries for the project, including FastAPI, Pillow, NumPy, dotenv, Langchain, Google Generative AI, and Matplotlib.
*   **`services/model.py`**: Initializes and configures the `ChatGoogleGenerativeAI` object for interacting with Google's Gemini 2.5 Pro large language model for conversational AI.
*   **`services/prompt.py`**: Defines a `generate_prompt` function that constructs AI prompts for image editing by combining system messages, user instructions, and image data using `PromptTemplate`.