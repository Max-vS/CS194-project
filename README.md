# CasePilot: An Agentic Case Study Interview Practice Platform

## Overview

CasePilot is a platform designed to help users practice business case interviews, emulating the style of top consulting firms. Leveraging advanced language models and agent architectures, the platform provides realistic case studies, interactive questioning, and personalized feedback to enhance your interview preparation.

## Features

- Realistic Case Studies: Generate industry-specific case studies that mimic real consulting scenarios.
- Interactive Interview Process: Engage in a simulated interview with sequenced questions and follow-ups.
- Speech Recognition and Synthesis: Utilize voice recording for responses and receive audio playback of questions.
- Personalized Feedback: Obtain detailed feedback on your answers to improve your performance.
- User-Friendly Interface: Built with Streamlit for accessible and straightforward interaction.

## Prerequisites

- Python 3.12
- Conda (for environment management)
- OpenAI API Key (for language model integration)

## Installation

Clone the repository and navigate to the project directory:

```bash
git clone https://github.com/yourusername/CS194-project.git
cd CS194-project
```

Create a Conda environment:

```bash
conda create -n project_casepilot python=3.12
```

Activate the environment:

```bash
conda activate project_casepilot
```
Install the required packages:

```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the root directory to store environment variables:

```bash
touch .env
```

Add your OpenAI API key to the ``.env`` file:

```bash
OPENAI_API_KEY=your_openai_api_key_here
```

## Usage

To start the Streamlit application:

```bash
streamlit run app.py
```

Follow the on-screen instructions to:

1. Select Industry: Choose your industry of interest from the provided options.
2. Generate Case Study: The application will create a case study context tailored to your chosen industry.
3. Participate in the Interview.
4. Receive Feedback: Obtain detailed feedback on your performance at the end of the interview.

## Project Structure

```plaintext
├── agents/
│   ├── agent_configs.py       # Defines agent types and system messages
│   ├── factory.py             # Factory functions to create agents
│   ├── groupchat.py           # Manages group chat interactions between agents
│   └── __init__.py
├── config/
│   ├── settings.py            # Configuration settings for LLM and industry options
│   └── __init__.py
├── utils/
│   ├── audio.py               # Functions for audio playback, recording, and transcription
│   └── __init__.py
├── app.py                     # Main Streamlit application script
├── requirements.txt           # Project dependencies
├── .gitignore                 # Git ignore patterns
└── README.md                  # Project documentation
```

## Dependencies

Refer to `requirements.txt` for the complete list of dependencies.