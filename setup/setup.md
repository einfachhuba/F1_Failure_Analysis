## Setup to work with this project

# 1. Install Python and create virtual environment

py -m venv analysis

.\analysis\Scripts\activate

(if you should encounter ExecutionPolicy error, run this command: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser)

# 2. Install dependencies

pip install -r setup\requirements.txt

# 3. Run project

py main.py