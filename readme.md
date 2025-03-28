# **ESG Report Analysis and Greenwashing Detection**  

This project is an interactive application developed with **Streamlit**, **LangChain**, and **LangGraph**, designed to ingest and analyze reports from companies with Environmental, Social, and Governance (ESG) commitments. The tool identifies potential signs of **greenwashing** in reports and assigns a score based on specific criteria. Users can also search for information within the document through a **Retrieval-Augmented Generation (RAG)**-based chat.  

---  

## **Features**  

1. **Report Upload**:  
   - Allows users to upload ESG reports in PDF or text format.  

2. **Automated Analysis**:  
   - The tool evaluates the report based on predefined **greenwashing** risk criteria, such as:  
     - Vague or exaggerated language.  
     - Lack of clear metrics.  
     - Disproportionate or inconsistent claims compared to financial or environmental impact data.  

3. **Risk Scoring**:  
   - Assigns a risk score to the report, indicating the likelihood of **greenwashing**.  

4. **RAG Chat**:  
   - Provides an interactive search system, allowing users to query the report content through Q&A.  

5. **Intuitive Interface**:  
   - Built with Streamlit, ensuring easy navigation and result visualization.  

---  

## **Installation**  

Follow the steps below to set up and run the project in your local environment.  

### **Prerequisites**  

Ensure you have the following tools installed:  
- Python 3.8 or later  
- pip (Python package manager)  

### **Step 1: Clone the Repository**  
```bash
git clone https://github.com/micaelleos/GreenWashing-Score.git
cd GreenWashing-Score
```  

### **Step 2: Create a Virtual Environment**  
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```  

### **Step 3: Install Dependencies**  
```bash
pip install -r requirements.txt
```  

### **Step 4: Configure Environment Variables**  

Create a `.env` file in the project root and set the following variables:  
```env
OPENAI_API_KEY=your_openai_api_key
```  

> ⚠️ Replace `your_openai_api_key` with your actual API key.  

### **Step 5: Run the Application**  
```bash
streamlit run app.py
```  

The application will be available at [http://localhost:8501](http://localhost:8501).  

---  

## **Project Structure**  

```plaintext
GreenWashing Score/
├── app.py                 # Main Streamlit application file
├── src
|   ├── scripts
|   |   ├── analysis/
|   |   │   ├── risk_scoring.py    # Risk scoring module
|   |   │   ├── criteria.json      # Greenwashing analysis criteria
|   |   ├── chat/
|   |   │   ├── document_loader.py # Document loading and processing
|   |   │   ├── chat_rag.py        # RAG Chat implementation with LangChain
├── data/                  # Directory for temporary file storage
├── requirements.txt       # Dependency list
├── README.md              # Project documentation
├── .env.example           # Example environment variable configuration
└── .gitignore             # Git ignore file
```  

---  

## **Licensing**  

This software is licensed under the following terms:  

### **1. Personal and Educational Use**  
You may use, modify, and run this software **only for personal or educational purposes, free of charge**, as long as the copyright notice and license terms remain included.  

### **2. Commercial Use**  
Any commercial use of this software **requires the purchase of a commercial license**. Examples of commercial use include:  
- Integration into products or services that are sold or licensed.  
- Use within for-profit organizations.  
- Any revenue-generating activities.  

#### How to Obtain a Commercial License  
Contact us via email at [micaelle.osouza@gmail.com] for licensing details.  

### **3. Restrictions**  
- You may not sublicense, sell, or redistribute this software without written authorization.  
- You may not remove or modify this license notice in any version of the software.  

---  

## **Contributing**  

Contributions are welcome! Follow these steps to collaborate:  

1. Fork the project.  
2. Create a new branch for your changes:  
   ```bash
   git checkout -b my-feature
   ```  
3. Commit your changes:  
   ```bash
   git commit -m "Add new feature"
   ```  
4. Push to the main branch:  
   ```bash
   git push origin my-feature
   ```  
5. Open a **Pull Request** on GitHub.  

---  

## **Technologies Used**  

- **[Streamlit](https://streamlit.io/)**: For building the interactive interface.  
- **[LangChain](https://www.langchain.com/)**: For implementing language models and data retrieval.  
- **[LangGraph](https://github.com/langgraph)**: For advanced workflow orchestration.  
- **Python**: The main programming language for this project.  

---  

## **Contact**  

For questions or support, reach out via:  
- **Email**: micaelle.osouza@gmail.com  
- **GitHub**: [Micaelle Souza](https://github.com/micaelleos)  


