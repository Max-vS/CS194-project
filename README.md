# UC Berkeley CS194-196 (LLM Agents), Final Project
### Team Name: CasePilot
### Project description: An LLM-Agents-based case interview practice platform to improve your interview skills to get into the consulting firm you want.

## Installation
After git-clone, create a Conda environment:
<code>conda create -n project_casepilot python=3.12</code>

Install the requirements:

<code>conda activate project_casepilot</code>

<code>pip install -r CS194-project/requirements.txt</code>

## Starting Streamlit
<code>streamlit run ./ui/app.py</code>

## FAQ
### I get an error for Whisper! (i.e.  File "...\lib\ctypes\__init__.py", line 364, in \_\_init__)

<code> pip uninstall whisper</code>

<code>pip install git+https://github.com/openai/whisper.git</code>