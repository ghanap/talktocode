## Github Automated Analysis Tool
 A Python-based tool that, when given a GitHub user's URL, returns the most technically complex and challenging repository from that user's profile. The tool uses [Langchain](https://langchain.com/), OpenAI gpt-3.5-turbo model as API, and FAISS as vector store which efficient Prompt Engineering under the hood.
## Getting Started

These instructions will help you set up the project and run it on your local machine.

### Prerequisites
```
- Install [Python](https://www.python.org/downloads/) 3.9.0 or later
- Set up a virtual environment if you want (Recommended)
```

### Installing

1. Go to the project folder.
   ```
   cd Github-Automated-Analysis-Tool
   ```

2. Create a virtual environment.
   ```
   python -m venv venv
   ```

3. Activate the virtual environment.
   - On Windows:
       ```
       .\venv\Scripts\activate
       ```
   - On Linux or MacOS:
       ```
       source venv/bin/activate
       ```
> You can use `conda` or  packages for [setting the virtual environment](https://www.scaler.com/topics/how-to-create-requirements-txt-python/).
4. Install the required dependencies using the following command.
   ```
   pip install -r requirements.txt
   ```

## Running the application

1. Run the streamlit application.
   ```
   streamlit run app.py
   ```

2. Open your web browser and enter the URL shown in the terminal, usually `http://localhost:8501`

3. Enjoy and tweak your Python Streamlit project!

## Built With

- [Python](https://www.python.org/)
- [Streamlit](https://www.streamlit.io/)
- [LangChain](https://langchain.com/)
- [OpenAI API](https://platform.openai.com/docs/introduction)


## License

This project is licensed under the MIT License - see the [LICENSE.txt](LICENSE.txt) file for details.


