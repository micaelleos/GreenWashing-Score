run:
	myenv\Scripts\activate
	python -m streamlit run app.py
install:
	mkdir data/stage
	mkdir data/processed
	python -m venv myenv
	myenv\Scripts\activate
	pip install -r requirements.txt