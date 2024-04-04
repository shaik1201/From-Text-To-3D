# From Text to 3D

Our project is dedicated to revolutionizing the accessibility of 3D printing for users, aiming to mitigate the challenges associated with traditional 3D modeling software. Recognizing the steep learning curve many encounter when delving into such software, we present a novel solution: "From Text to 3D using LLM."

## Overview

Our system offers a user-friendly approach, leveraging natural language input to enable users to effortlessly describe their desired 3D objects. These descriptions are then interpreted, visualized, and interactively modified, culminating in the generation of printer-ready code. Unlike existing platforms such as "Addithive," which merely translate text descriptions into code, our project introduces an innovative paradigm. We provide users with a virtual 3D model that can be customized prior to printing.

## Key Features

- **Chatbot-Based Interface:** Users can input plain text descriptions of their desired 3D objects.
- **Interactive Visualization:** The system generates virtual 3D models based on user input, allowing for real-time modifications.
- **Printer-Ready Code Generation:** Once satisfied with the design, users can generate printer-ready code (G-code) for seamless 3D printing.

## Technology

Our system is powered by a multi-agent architecture, integrating a finely-tuned GPT-4 model. This ensures efficient translation of user prompts into precise 3D printing instructions.

## Usage

To utilize our system, follow these steps:

1. **Environment Setup:** Create a Conda environment using the provided `environment.yml` file.
`conda env create -f environment.yml`