# CasePilot: An Agentic Case Study Interview Practice Platform
CasePilot is a platform designed to help users practice business case interviews, emulating the style of top consulting firms. Leveraging advanced language models and agent architectures, the platform provides realistic case studies, interactive questioning, and personalized feedback to enhance your interview preparation.

## Overview

In today’s competitive job market, job seekers are increasingly turning to ways to perform better in interviews to secure desirable positions. Specifically, case study interviews, common in industries such as consulting, finance, and technology, require candidates to demonstrate strong problem-solving, critical thinking, and communication skills. Traditional interview preparation tools, such as case books or mock interview sessions, can often fall short in providing the interactive, dynamic environment required to truly excel in these complex interviews. CasePilot is designed to simulate dynamic, role-specific interviews tailored to case study interviews of various industries. The goal is to create an interactive, dynamic simulation to help users refine their interview performance effectively.

Existing case study AI tools typically generate answers based on predefined case inputs but are unable to support any level of realistic interaction. They typically rely on static inputs and predefined solutions, failing to engage in the interactive, back-and-forth dialogue that is central to a real case interview.  CasePilot aims to address this gap by:

- Providing tailored, dynamic questions for case studies based on industry.
- Analyze user responses in real time, offering insights and guidance as the interview progresses.
- Generate follow-up questions that adapt to the user’s previous answers, promoting a deeper, more engaged interview experience.
- Offer comprehensive feedback on the user’s performance, focusing on key areas like structure, communication, creativity, and analytical reasoning.

CasePilot aims to provide the most personalized interview experience, while still maintaining the essence of self-learning and improvement. The motivation behind CasePilot is rooted in the belief that effective interview preparation requires more than just passive practice; it demands real-time interaction, personalized guidance, and iterative learning. As students ourselves, we know the amount of effort and drive it takes to prepare and secure desirable employment in today’s job market. Traditional methods, while valuable, often fall short in engaging users in the nuanced process of developing their interview skills over time.

CasePilot’s interactive agents offer a unique solution to this problem, giving users the ability to engage in continuous learning, develop critical thinking skills, and build the confidence needed to excel in competitive job markets. By incorporating adaptive questioning and personalized feedback, CasePilot strives to offer a platform that goes beyond static preparation. 


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

**Make sure to also activate the environment in your IDE**

Install ffmpeg (required for audio processing):

```bash
conda install ffmpeg -c conda-forge
```

Install other required packages:

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
