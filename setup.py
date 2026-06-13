from setuptools import setup, find_packages

setup(
    name="llm-sql-query-generator",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Convert plain English to SQL queries using LLM (OpenAI + LangChain)",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/llm-sql-query-generator",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "streamlit>=1.32.0",
        "langchain>=0.1.13",
        "openai>=1.14.0",
        "sqlparse>=0.4.4",
        "pandas>=2.2.1",
        "python-dotenv>=1.0.1",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
