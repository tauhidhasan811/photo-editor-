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
import google.generativeai as genai
from PIL import Image
import matplotlib.pyplot as plt
from io import BytesIO
from dotenv import load_dotenv
import os

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# 1. Load input image
img = Image.open("pic.png")

# 2. Use an image-capable model
model = genai.GenerativeModel("models/gemini-2.0-flash")

# 3. Generate content WITHOUT request_options
response = model.generate_content(
    [
        "Create a new improved corporate-style version of this image.",
        img
    ]
)

# 4. Extract generated image bytes (correct field for new SDK)
image_bytes = response.parts[0].inline_data.data

# 5. Convert bytes → image
generated_img = Image.open(BytesIO(image_bytes))

# 6. Show result
plt.imshow(generated_img)
plt.axis("off")
plt.show()
