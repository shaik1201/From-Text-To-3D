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

> [!NOTE]
> In the future, when the fine-tuned GPT-4 model is ready, you can add a new variable to the const.py file inside the Consts folder:
`OPENAI_API_KEY = "your_api_key"`
However, for now, we do not use this option as the fine-tuned model is not perfectly ready yet due to insufficient examples. Therefore, we are currently using already generated Python code examples that create the object we are presenting. Consequently, we only support prompts which contain the following objects: 'box', 'bowl', 'ellipse baking mold', 'plate', 'cup', 'glass', 'bottle', 'baking mold', 'flower pot', 'hook', and 'toothpick dispenser'.

> [!NOTE]
> Currently, the generation of G-code for printing the object is not supported (pressing the generate G-code button should show you how it will look like). However, in the future, we plan to implement a solution that facilitates this process. This will likely involve integrating with external software capable of converting an OBJ file into a G-code file, which can then be used to input into a 3D printer.

## How to start:
1. **Environment Setup:** Create a Conda environment using the provided `environment.yml` file. Run the command:
```
conda env create -f environment.yml
```
   

2. **Activate Environment:** Activate the environment using the following command:
```
conda activate env-nev
```

3. **Launch the Application:** Start the application by running:
```
python app.py
```

