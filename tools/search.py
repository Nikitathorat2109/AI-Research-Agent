from tavily import TavilyClient
from typing import List, Dict
import os

class WebSearchTool:
    def __init__(self):
        self.client = TavilyClient(api_key=os.getenv('TAVILY_API_KEY'))
    
    def search(self, query: str, max_results: int = 3) -> List[Dict[str, str]]:
        """Search for sources using Tavily API"""
        try:
            response = self.client.search(
                query=query,
                search_depth="advanced",
                max_results=max_results
            )
            
            sources = []
            for result in response.get('results', []):
                sources.append({
                    'title': result.get('title', 'No Title'),
                    'url': result.get('url', ''),
                    'snippet': result.get('content', '')
                })
            
            return sources
            
        except Exception as e:
            print(f"Search error: {e}")
            return []