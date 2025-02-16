# HealthTrendBot: Public Health Trend Analyzer

## Overview

**HealthTrendBot** is a conversational chatbot built using Streamlit that specializes in analyzing public health trends and delivering data-driven insights. The bot leverages the DeepSeek API via the OpenAI SDK interface to process user queries, maintain conversation context, and provide detailed, accurate, and well-researched responses.

## Features

- **Conversational Interface:**  
  Engages users in a dialogue while maintaining conversation history for context.
- **DeepSeek API Integration:**  
  Retrieves and processes public health trend data using DeepSeek's chat model.
- **Interactive Dashboard:**  
  Built with Streamlit to display the conversation and API results in a user-friendly web interface.
- **Prominent System Prompt:**  
  Configured to ensure the assistant behaves as a knowledgeable expert in public health trends.

## Requirements

- Python 3.7+
- [Streamlit](https://streamlit.io)
- [OpenAI Python SDK](https://github.com/openai/openai-python) *(used here for DeepSeek API interactions)*
- [Requests](https://pypi.org/project/requests/)
- [Pandas](https://pandas.pydata.org)
- [Plotly](https://plotly.com/python/)

## Installation

1. **Clone the Repository:**

   ```bash
   git clone <repository_url>
   cd <repository_directory>
