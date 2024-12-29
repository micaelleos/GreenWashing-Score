run:
	source myenv/bin/activate
	python -m streamlit run app.py
install:
	mkdir data/stage
	mkdir data/processed
	python -m venv myenv
	source myenv/bin/activate
	pip install -r requirements.txt