## Setup to work with this project

# 1. Install Python and create virtual environment

py -m venv analysis

.\analysis\Scripts\activate

(if you should encounter ExecutionPolicy error, run this command: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser)

# 2. Install dependencies

pip install -r setup\requirements.txt

# 3. Run project
Run the code depending on what you want to do. The arguments are explained in the next section.

main.py u -> only update data
main.py p -> only plot data
main.py a -> only analyze data
main.py up -> update and plot data
main.py pa -> plot and analyze data
main.py ua -> update and analyze data
main.py upa -> update, plot and analyze data
