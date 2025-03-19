source:
	source myenv/bin/activate
run:
	python -m streamlit run app.py
install:
	mkdinr data
	mkdir data/stage
	mkdir data/processed
	python -m venv myenv
	source myenv/bin/activate
	pip install -r requirements.txt