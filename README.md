# Smart Research Assistant 🔬

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

An intelligent research assistant powered by AI that helps researchers stay up-to-date with academic papers and related GitHub projects. It combines academic knowledge with practical implementations to provide comprehensive research insights.

## 🌟 Features

- **Smart Paper Search**: Automatically finds and analyzes relevant academic papers from Google Scholar
- **GitHub Project Discovery**: Identifies related open-source implementations and projects
- **AI-Powered Summaries**: Generates concise summaries of papers and projects
- **Knowledge Graph**: Builds and maintains a graph of research concepts and their relationships
- **Memory Management**: Learns from your research patterns to provide personalized recommendations
- **Interactive CLI**: Easy-to-use command-line interface for research queries

## 🚀 Quick Start

1. Clone the repository:
```bash
git clone https://github.com/Raziyeh71/Smart-Research-Assistant.git
cd Smart-Research-Assistant
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your GitHub token
```

5. Run the assistant:
```bash
python main.py
```

## 💡 Usage Example

```python
Enter your research query: "transformer architecture in deep learning"

Findings:
=========
Relevant Papers:
- "Attention Is All You Need" (2017)
  Summary: Introduces the transformer architecture...

Relevant GitHub Projects:
- huggingface/transformers
  Summary: State-of-the-art Natural Language Processing...
```

## 🛠️ Architecture

The project consists of several key components:
- `PaperRetriever`: Fetches academic papers from Google Scholar
- `GitHubRetriever`: Searches for relevant GitHub repositories
- `Summarizer`: Generates AI-powered summaries
- `MemoryManager`: Maintains research history and patterns
- `GraphBuilder`: Constructs knowledge graphs of research concepts

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=Raziyeh71/Smart-Research-Assistant&type=Date)](https://star-history.com/#Raziyeh71/Smart-Research-Assistant&Date)

## 📧 Contact

Raziyeh - [@Raziyeh71](https://github.com/Raziyeh71)

Project Link: [https://github.com/Raziyeh71/Smart-Research-Assistant](https://github.com/Raziyeh71/Smart-Research-Assistant)
