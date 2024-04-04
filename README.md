# From Text to 3D

Our project aims to simplify 3D printing for users by addressing the complexity of 
traditional 3D modeling software. Recognizing the challenge many faces in learning 
such software, the project proposes a chatbot-based solution, called "From Text to 3D 
using LLM." This system allows users to input plain text descriptions of desired 3D 
objects, which are then interpreted, visualized, and modified interactively before 
generating printer-ready code. Unlike existing platforms like "Addithive", which solely 
generate code from text descriptions, this project offers an innovative approach by 
providing users with a virtual 3D model that they can modify before printing. Leveraging 
a multi-agent system with a finetuned GPT-4 model, the project ensures efficient 
translation of user prompts into 3D printing instructions (G-code).

**NOTE:**
we are using api key for using the fine tuned gpt4 model. in the future when the model will be ready you can add to the const.py insinde the Consts folder a new variable:
OPENAI_API_KEY = "your_api_key"

for now we dont use this option as the fine tuned model is not perfectly ready yet because there are still not enough examples for doing so.
hence we are using already generated python codes examples that creating the object we are presenting.
hence we only support prompts which contain the following objects:
 'box', 'bowl', 'ellipse baking mold', 'plate', 'cup', 'glass',
                'bottle', 'baking mold', 'flower pot', 'hook', 'toothpick dispenser'



1. **Environment Setup:** Create a Conda environment using the provided `environment.yml` file. Run the command:
   `conda env create -f environment.yml`

2. **Activate Environment:** Activate the environment using the following command:
`conda activate env-nev`

3. **Launch the Application:** Start the application by running:
python app.py

