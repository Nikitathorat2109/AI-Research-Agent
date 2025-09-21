# AI Research Agent

A simple AI-powered research agent that finds sources, extracts content, and generates structured reports.

## 🎥 Demo Video

Check out the video demo to see the AI Research Agent in action:

![AI Research Agent Demo](static/AI_Research_Agent_Demo.mp4)

*Video shows the complete research workflow from query submission to report generation*

## Features

- **Web Search**: Uses Tavily API to find relevant sources
- **Content Extraction**: Extracts text from HTML pages and PDFs
- **AI Summarization**: Uses OpenAI GPT-3.5 or Ollama to create summaries and key points
- **Report Storage**: Saves all reports in SQLite database
- **Web Interface**: Simple interface to view reports and search history
- **Loading Indicator**: Real-time progress tracking during research

## Architecture

```
User Query → Web Search → Content Extraction → AI Summary → Database → Web View
```

1. **Search Tool**: Tavily API finds 2-3 relevant sources
2. **Extractor Tool**: Trafilatura (HTML) + PyPDF (PDF) extract clean text
3. **AI Agent**: OpenAI GPT-3.5 or Ollama generates summary and key points
4. **Database**: SQLite stores reports for future reference
5. **Web App**: Flask serves the interface

### Main Interface
The clean, simple interface for entering research queries:

### Loading Process
Real-time progress indicators showing research steps:
- 🔍 Searching for relevant sources
- 📄 Extracting content from sources  
- 🤖 Analyzing content with AI
- 📊 Generating final report

### Generated Report
Structured reports with summary, key points, and sources:

## Setup

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd ai-research-agent
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your API keys and LLM preference
```

4. **Choose your LLM provider**

**Option A: OpenAI (Paid)**
```bash
# In .env file:
LLM_PROVIDER=openai
OPENAI_API_KEY=your_openai_api_key_here
```

**Option B: Ollama (Free, Local)**
```bash
# Install Ollama first: https://ollama.ai/
ollama pull llama3

# In .env file:
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3
```

5. **Get API Keys**
   - Tavily API key from https://tavily.com/ (required)
   - OpenAI API key from https://platform.openai.com/ (optional, if using OpenAI)

6. **Run the application**
```bash
python app.py
```

7. **Open your browser** to http://localhost:5000

## Usage

1. Enter a research query (e.g., "Latest research on AI in education")
2. Watch the loading indicator show progress through each step
3. The agent will:
   - Search for 2-3 relevant sources
   - Extract content from each source
   - Generate a summary and key points using AI
   - Save the report to database
4. View the generated report with sources and summary
5. Browse past reports from the main page

## Example Queries

- "Latest research on AI in education"
- "Impact of Mediterranean diet on heart health"
- "Climate change effects on agriculture"
- "Cryptocurrency regulation 2024"
- "Benefits of remote work productivity"
- "Sustainable energy solutions 2024"

## Project Structure

```
ai-research-agent/
├── app.py                 # Main Flask application
├── agent.py              # Core AI agent logic
├── tools/
│   ├── __init__.py
│   ├── search.py         # Web search tool (Tavily)
│   └── extractor.py      # Content extraction tool
├── database.py           # Database operations
├── templates/
│   ├── index.html        # Main page with loading indicator
│   ├── report.html       # Individual report view
│   └── base.html         # Base template
├── static/
│   ├── style.css         # CSS with loading animations
│   └── demo.mp4          # Video demonstration
├── requirements.txt      # Dependencies
├── .env.example         # Environment variables template
└── README.md            # This file
```

## Error Handling

- Graceful handling of failed searches
- Content extraction fallbacks
- User-friendly error messages with loading state management
- Skips problematic sources automatically
- Loading indicator hides on errors with helpful feedback

## Technical Features

### Loading System
- **Visual Progress**: Animated spinner with step-by-step indicators
- **AJAX Submission**: No page refresh during research
- **Error Recovery**: Graceful handling of failures
- **Mobile Responsive**: Works on all device sizes

### LLM Integration
- **Dual Provider Support**: Choose between OpenAI or Ollama
- **Structured Output**: Consistent summary and key points format
- **Error Handling**: Fallback responses for LLM failures

## LLM Options

**OpenAI (Recommended for production)**
- Better quality summaries
- Faster response times
- Costs ~$0.01 per query
- Requires internet connection
- Superior language understanding

**Ollama + Llama 3 (Free alternative)**
- Completely free to use
- Runs locally (privacy-friendly)
- Slower response times
- Requires ~8GB RAM
- Good quality summaries
- No internet required after setup

Switch between providers by changing `LLM_PROVIDER` in your `.env` file.

## Performance

- **Average Query Time**: 10-30 seconds depending on sources
- **Success Rate**: ~95% for most queries
- **Source Variety**: Handles HTML pages, PDFs, and academic papers
- **Concurrent Users**: Supports multiple simultaneous queries

## Limitations

- Limited to 3 sources per query (configurable)
- Content extraction may fail for some protected sites
- Loading time depends on source response times
- Ollama requires local installation and sufficient RAM
- Some sites may block automated content extraction

## AI Assistance Used

- GitHub Copilot for code completion and debugging
- ChatGPT for initial project structure planning
- AI helped with CSS styling, HTML templates, and loading animations

---
