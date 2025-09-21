import openai
import ollama
from tools.search import WebSearchTool
from tools.extractor import ContentExtractor
from database import Database
from typing import Dict, List
import os

class ResearchAgent:
    def __init__(self):
        self.llm_provider = os.getenv('LLM_PROVIDER', 'openai').lower()
        
        if self.llm_provider == 'openai':
            openai.api_key = os.getenv('OPENAI_API_KEY')
        elif self.llm_provider == 'ollama':
            self.ollama_base_url = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
            self.ollama_model = os.getenv('OLLAMA_MODEL', 'llama3')
        
        self.search_tool = WebSearchTool()
        self.extractor = ContentExtractor()
        self.db = Database()
    
    def research(self, query: str) -> Dict:
        """Main research method that coordinates all steps"""
        try:
            # Step 1: Search for sources
            print(f"Searching for: {query}")
            sources = self.search_tool.search(query, max_results=3)
            
            if not sources:
                return {'error': 'No sources found for the query'}
            
            # Step 2: Extract content from sources
            print("Extracting content from sources...")
            enriched_sources = []
            for source in sources:
                content = self.extractor.extract_content(source['url'])
                enriched_sources.append({
                    **source,
                    'content': content[:2000] if content else "Content extraction failed"
                })
            
            # Step 3: Generate summary using LLM
            print(f"Generating summary using {self.llm_provider.upper()}...")
            summary, key_points = self._generate_summary(query, enriched_sources)
            
            # Step 4: Save to database
            report_id = self.db.save_report(query, enriched_sources, summary, key_points)
            
            return {
                'id': report_id,
                'query': query,
                'sources': enriched_sources,
                'summary': summary,
                'key_points': key_points
            }
            
        except Exception as e:
            return {'error': f'Research failed: {str(e)}'}
    
    def _generate_summary(self, query: str, sources: List[Dict]) -> tuple:
        """Generate summary and key points using selected LLM"""
        # Prepare content for LLM
        content_text = ""
        for i, source in enumerate(sources, 1):
            content_text += f"\nSource {i} ({source['title']}):\n{source['content']}\n"
        
        prompt = f"""Research Query: {query}

Content from sources:
{content_text}

Please provide:
1. A comprehensive summary (2-3 paragraphs) of the key information related to the query
2. A list of 4-6 key points (each point should be one clear sentence)

Format your response as:
SUMMARY:
[Your summary here]

KEY_POINTS:
- [Point 1]
- [Point 2]
- [Point 3]
- [Point 4]"""
        
        try:
            if self.llm_provider == 'openai':
                return self._generate_with_openai(prompt)
            elif self.llm_provider == 'ollama':
                return self._generate_with_ollama(prompt)
            else:
                return f"Unsupported LLM provider: {self.llm_provider}", []
                
        except Exception as e:
            return f"Summary generation failed: {str(e)}", []
    
    def _generate_with_openai(self, prompt: str) -> tuple:
        """Generate summary using OpenAI"""
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a research assistant that creates clear, concise summaries from multiple sources."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=800
        )
        
        content = response.choices[0].message.content
        return self._parse_response(content)
    
    def _generate_with_ollama(self, prompt: str) -> tuple:
        """Generate summary using Ollama"""
        response = ollama.chat(
            model=self.ollama_model,
            messages=[
                {"role": "system", "content": "You are a research assistant that creates clear, concise summaries from multiple sources."},
                {"role": "user", "content": prompt}
            ]
        )
        
        content = response['message']['content']
        return self._parse_response(content)
    
    def _parse_response(self, content: str) -> tuple:
        """Parse the LLM response to extract summary and key points"""
        # Parse the response
        parts = content.split("KEY_POINTS:")
        summary = parts[0].replace("SUMMARY:", "").strip()
        
        key_points = []
        if len(parts) > 1:
            points_text = parts[1].strip()
            key_points = [point.strip("- ").strip() for point in points_text.split("\n") if point.strip().startswith("-")]
        
        return summary, key_points