"""import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from services.prompt import generate_prompt
from lagchain_google_genai import ChatGoogleGenerativeAI


img = Image.open('pic.png')


prompt = generate_prompt(user_preferance='corparate', 
                         user_instraction='instraction',
                         image=img)

llm = ChatGoogleGenerativeAI(model='models/gemini-2.5-pro')
response = llm.invoke(prompt)





plt.imshow(response)
plt.axis('off')
#plt.show()"""

"""


from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import os

load_dotenv()

# 1. Initialize the NEW Client (handles API key from os.environ["GOOGLE_API_KEY"] automatically)
client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])
print(os.environ["GOOGLE_API_KEY"])
print(client)
# 2. Load input image
img = Image.open("pic.png")

# 3. Use the model capable of image generation
# Note: 'gemini-2.0-flash-exp' is the current model capable of image output
# 'gemini-2.5-pro' is text-only.
model_id = "gemini-2.0-flash-exp" 

# 4. Generate content
# We must explicitly ask for the image in the prompt
response = client.models.generate_content(
    model=model_id,
    contents=[
        "Create a new improved corporate-style version of this image. Maintain the composition but improve the lighting and style.",
        img
    ],
    config=types.GenerateContentConfig(
        response_modalities=["IMAGE"] # Explicitly tell the model to output an Image
    )
)

# 5. Extract and display generated image
# The new SDK structure for image responses:
if response.candidates[0].content.parts[0].inline_data:
    image_bytes = response.candidates[0].content.parts[0].inline_data.data
    generated_img = Image.open(BytesIO(image_bytes))

    plt.imshow(generated_img)
    plt.axis("off")
    plt.show()
    
    # Optional: Save it
    generated_img.save("corporate_version.png")
else:
    print("The model did not return an image. Response text:", response.text)"""

"""
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import os

load_dotenv()

# 1. Initialize Client
client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])

# 2. Load input image
try:
    img = Image.open("pic.png")
except FileNotFoundError:
    print("Error: 'pic.png' not found. Please make sure the image is in the same folder.")
    exit()

# 3. Use the Experimental Flash 2.0 Model
# This model supports "Omni" capabilities (Input: Image+Text -> Output: Image+Text)
model_id = "gemini-2.0-flash-exp"

print("Sending request to Google GenAI...")

try:
    # 4. Generate content
    # CRITICAL FIX: response_modalities must include "TEXT" so the model can "think" or speak.
    response = client.models.generate_content(
        model=model_id,
        contents=[
            "Create a new improved corporate-style version of this image. Maintain the composition but improve the lighting and style.",
            img
        ],
        config=types.GenerateContentConfig(
            response_modalities=["TEXT", "IMAGE"], # Must allow both!
            temperature=0.7,
        )
    )

    # 5. Extract and display generated image
    # The response will contain multiple parts (some text, some image). We look for the image part.
    generated_image_found = False
    
    if response.candidates and response.candidates[0].content.parts:
        for part in response.candidates[0].content.parts:
            # Check if this part is an image
            if part.inline_data:
                print("Image generated successfully!")
                image_bytes = part.inline_data.data
                generated_img = Image.open(BytesIO(image_bytes))

                # Display
                plt.imshow(generated_img)
                plt.axis("off")
                plt.show()
                
                # Save
                generated_img.save("corporate_result.png")
                print("Saved to 'corporate_result.png'")
                generated_image_found = True
                break # Found the image, stop looking
    
    if not generated_image_found:
        print("The model responded, but did not generate an image.")
        print("Model Text Response:", response.text)

except Exception as e:
    print(f"An error occurred: {e}")"""

from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])

# 1. Load and Prepare Image
# Imagen often prefers specific aspect ratios, but let's start simple.
try:
    img = Image.open("pic.png")
    img.thumbnail((512, 512)) 
except FileNotFoundError:
    print("Error: 'pic.png' not found.")
    exit()

# 2. Define the Model ID found in your list
# We use the "Fast" version as it's lighter on resources
model_id = "imagen-4.0-fast-generate-001"

print(f"Sending request to {model_id}...")

try:
    # Note: 'generate_images' is the correct method for Imagen models
    response = client.models.generate_images(
        model=model_id,
        prompt="Transform this image into a high-quality oil painting style. Maintain the main subject but change the texture.",
        config=types.GenerateImagesConfig(
            number_of_images=1,
            # Some versions of the SDK/API allow passing the image for editing here
            # If this specific 'fast' model is Text-to-Image only, it might ignore the image 
            # or throw an error, but it's the best first step.
        )
    )

    # 3. Extract and Show Image
    if response.generated_images:
        print("✅ Image Generated Successfully!")
        image_bytes = response.generated_images[0].image.image_bytes
        generated_img = Image.open(BytesIO(image_bytes))
        
        plt.imshow(generated_img)
        plt.axis("off")
        plt.show()
        generated_img.save("imagen4_result.png")
    else:
        print("❌ No image returned.")

except Exception as e:
    print(f"\n❌ Error: {e}")
    
    # DIAGNOSTIC: If Imagen 4 fails, let's fallback to the Gemini 2.0 Exp model
    # which supports 'generateContent' (Text+Image inputs)
    print("\n⚠️ Imagen 4 failed. Attempting fallback to Gemini 2.0 Flash Exp...")
    
    try:
        fallback_model = "gemini-2.0-flash-exp-image-generation"
        response = client.models.generate_content(
            model=fallback_model,
            contents=[
                "Create a variation of this image in a cyberpunk style.",
                img
            ]
        )
        if response.candidates and response.candidates[0].content.parts:
             for part in response.candidates[0].content.parts:
                if part.inline_data:
                    print("✅ Fallback Image Generated!")
                    image_bytes = part.inline_data.data
                    generated_img = Image.open(BytesIO(image_bytes))
                    generated_img.save("fallback_result.png")
                    break
        else:
            print("❌ Fallback also failed (No image content).")
            
    except Exception as e2:
        print(f"❌ Fallback Error: {e2}")
        print("\n[Critical Info] If both fail with 429 or 403, you definitively need to enable Billing in Google Cloud Console.")