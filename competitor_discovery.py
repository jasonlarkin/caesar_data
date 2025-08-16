#!/usr/bin/env python3
"""
AI Agent Competitor Discovery Tool

This script automates the discovery of AI agent systems and competitors
using various platforms including GitHub, arXiv, and other sources.

Requirements:
- requests
- feedparser
- pandas
- json
- datetime
"""

import requests
import json
import pandas as pd
from datetime import datetime, timedelta
import time
import os
from typing import Dict, List, Optional, Any
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CompetitorDiscovery:
    """Main class for discovering AI agent competitors"""
    
    def __init__(self, output_dir: str = "competitor_discovery"):
        self.output_dir = output_dir
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Known competitors from our analysis
        self.known_competitors = [
            {
                "name": "OpenAI GPT-4/5",
                "category": "Indirect",
                "description": "General-purpose AI with research capabilities",
                "capabilities": ["General reasoning", "Research assistance", "Code generation"],
                "market_position": "Leader",
                "funding": "Billions from Microsoft and others",
                "team_size": "1000+",
                "technical_approach": "Large language models with reinforcement learning",
                "competitive_threat": "High",
                "discovery_date": "2024-01-01",
                "last_updated": "2024-12-01",
                "sources": ["Company website", "Research papers"]
            },
            {
                "name": "Anthropic Claude",
                "category": "Indirect",
                "description": "AI platform with safety focus and research capabilities",
                "capabilities": ["Research assistance", "Safety analysis", "Code generation"],
                "market_position": "Established",
                "funding": "Billions from Amazon and others",
                "team_size": "500+",
                "technical_approach": "Constitutional AI with safety focus",
                "competitive_threat": "Medium-High",
                "discovery_date": "2024-01-01",
                "last_updated": "2024-12-01",
                "sources": ["Company website", "Research papers"]
            },
            {
                "name": "Perplexity AI",
                "description": "AI-powered research and search platform",
                "capabilities": ["Web search", "Research assistance", "Source citation"],
                "market_position": "Established",
                "funding": "Hundreds of millions",
                "team_size": "100+",
                "technical_approach": "Search-augmented generation",
                "competitive_threat": "High",
                "discovery_date": "2024-01-01",
                "last_updated": "2024-12-01",
                "sources": ["Company website", "Product demos"]
            }
        ]
        
        # Discovery sources
        self.discovery_sources = {
            "github": {
                "enabled": True,
                "rate_limit": 5000,  # GitHub API rate limit
                "queries": [
                    "ai agent autonomous",
                    "multi agent system",
                    "research agent ai",
                    "financial analysis ai",
                    "autonomous research assistant"
                ]
            },
            "arxiv": {
                "enabled": True,
                "queries": [
                    "ai agent",
                    "autonomous agent",
                    "multi agent system",
                    "research assistant ai"
                ]
            },
            "huggingface": {
                "enabled": True,
                "queries": [
                    "agent",
                    "autonomous",
                    "assistant"
                ]
            }
        }
    
    def discover_github_agents(self) -> List[Dict[str, Any]]:
        """Discover AI agent repositories on GitHub"""
        logger.info("Discovering AI agents on GitHub...")
        
        discovered = []
        
        for query in self.discovery_sources["github"]["queries"]:
            try:
                logger.info(f"Searching GitHub for: {query}")
                
                # GitHub search API
                url = "https://api.github.com/search/repositories"
                params = {
                    'q': query,
                    'sort': 'stars',
                    'order': 'desc',
                    'per_page': 20
                }
                
                response = self.session.get(url, params=params, timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    for repo in data['items']:
                        # Check if it's relevant to AI agents
                        if self._is_relevant_ai_agent(repo):
                            competitor = {
                                "name": repo['full_name'],
                                "category": "Unknown",
                                "description": repo['description'] or "No description",
                                "capabilities": self._extract_capabilities(repo),
                                "market_position": self._assess_market_position(repo),
                                "funding": "Unknown",
                                "team_size": "Unknown",
                                "technical_approach": "Open source",
                                "competitive_threat": self._assess_competitive_threat(repo),
                                "discovery_date": datetime.now().strftime("%Y-%m-%d"),
                                "last_updated": repo['updated_at'][:10],
                                "sources": ["GitHub"],
                                "github_data": {
                                    "stars": repo['stargazers_count'],
                                    "forks": repo['forks_count'],
                                    "language": repo['language'],
                                    "created": repo['created_at'],
                                    "url": repo['html_url']
                                }
                            }
                            
                            discovered.append(competitor)
                            logger.info(f"Discovered: {repo['full_name']} ({repo['stargazers_count']} stars)")
                
                # Respect rate limits
                time.sleep(1)
                
            except Exception as e:
                logger.error(f"Error searching GitHub for '{query}': {str(e)}")
                continue
        
        logger.info(f"Discovered {len(discovered)} AI agent repositories on GitHub")
        return discovered
    
    def _is_relevant_ai_agent(self, repo: Dict[str, Any]) -> bool:
        """Check if repository is relevant to AI agents"""
        relevant_keywords = [
            'agent', 'autonomous', 'multi-agent', 'assistant', 'research',
            'ai', 'artificial intelligence', 'machine learning', 'llm'
        ]
        
        # Check repository name and description
        text_to_check = f"{repo['name']} {repo['description'] or ''}".lower()
        
        # Must have at least 2 relevant keywords
        keyword_count = sum(1 for keyword in relevant_keywords if keyword in text_to_check)
        
        # Must have reasonable activity (stars, recent updates)
        has_activity = repo['stargazers_count'] > 10 and repo['forks_count'] > 0
        
        return keyword_count >= 2 and has_activity
    
    def _extract_capabilities(self, repo: Dict[str, Any]) -> List[str]:
        """Extract capabilities from repository data"""
        capabilities = []
        
        # Check repository topics
        if repo.get('topics'):
            for topic in repo['topics']:
                if topic in ['ai', 'agent', 'autonomous', 'research', 'assistant']:
                    capabilities.append(topic)
        
        # Check language
        if repo.get('language'):
            capabilities.append(f"Code: {repo['language']}")
        
        # Check description for capabilities
        description = repo.get('description', '').lower()
        if 'research' in description:
            capabilities.append("Research assistance")
        if 'financial' in description:
            capabilities.append("Financial analysis")
        if 'code' in description:
            capabilities.append("Code generation")
        
        return capabilities if capabilities else ["AI agent capabilities"]
    
    def _assess_market_position(self, repo: Dict[str, Any]) -> str:
        """Assess market position based on repository metrics"""
        stars = repo['stargazers_count']
        forks = repo['forks_count']
        
        if stars > 10000:
            return "Leader"
        elif stars > 1000:
            return "Established"
        elif stars > 100:
            return "Growing"
        else:
            return "Early stage"
    
    def _assess_competitive_threat(self, repo: Dict[str, Any]) -> str:
        """Assess competitive threat level"""
        stars = repo['stargazers_count']
        forks = repo['forks_count']
        
        if stars > 5000 and forks > 500:
            return "High"
        elif stars > 1000 and forks > 100:
            return "Medium"
        else:
            return "Low"
    
    def discover_arxiv_papers(self) -> List[Dict[str, Any]]:
        """Discover AI agent research papers on arXiv"""
        logger.info("Discovering AI agent papers on arXiv...")
        
        discovered = []
        
        for query in self.discovery_sources["arxiv"]["queries"]:
            try:
                logger.info(f"Searching arXiv for: {query}")
                
                # arXiv API search
                url = "http://export.arxiv.org/api/query"
                params = {
                    'search_query': f'all:"{query}"',
                    'start': 0,
                    'max_results': 20,
                    'sortBy': 'submittedDate',
                    'sortOrder': 'descending'
                }
                
                response = self.session.get(url, params=params, timeout=30)
                
                if response.status_code == 200:
                    # Parse XML response (simplified)
                    content = response.text
                    
                    # Extract paper information (simplified parsing)
                    papers = self._parse_arxiv_response(content)
                    
                    for paper in papers:
                        competitor = {
                            "name": paper['title'],
                            "category": "Research",
                            "description": paper['summary'][:200] + "...",
                            "capabilities": ["Research", "Academic"],
                            "market_position": "Research",
                            "funding": "Academic",
                            "team_size": "Academic team",
                            "technical_approach": "Research methodology",
                            "competitive_threat": "Low",
                            "discovery_date": datetime.now().strftime("%Y-%m-%d"),
                            "last_updated": paper['published'],
                            "sources": ["arXiv"],
                            "arxiv_data": {
                                "authors": paper['authors'],
                                "url": paper['url'],
                                "category": paper['category']
                            }
                        }
                        
                        discovered.append(competitor)
                
                # Respect rate limits
                time.sleep(2)
                
            except Exception as e:
                logger.error(f"Error searching arXiv for '{query}': {str(e)}")
                continue
        
        logger.info(f"Discovered {len(discovered)} AI agent papers on arXiv")
        return discovered
    
    def _parse_arxiv_response(self, content: str) -> List[Dict[str, Any]]:
        """Parse arXiv API response (simplified)"""
        papers = []
        
        # Simple parsing - in production, use proper XML parser
        lines = content.split('\n')
        current_paper = {}
        
        for line in lines:
            if '<entry>' in line:
                current_paper = {}
            elif '</entry>' in line:
                if current_paper:
                    papers.append(current_paper)
            elif '<title>' in line and '</title>' in line:
                title = line.split('<title>')[1].split('</title>')[0]
                current_paper['title'] = title
            elif '<summary>' in line and '</summary>' in line:
                summary = line.split('<summary>')[1].split('</summary>')[0]
                current_paper['summary'] = summary
            elif '<published>' in line and '</published>' in line:
                published = line.split('<published>')[1].split('</published>')[0]
                current_paper['published'] = published[:10]
            elif '<id>' in line and '</id>' in line:
                paper_id = line.split('<id>')[1].split('</id>')[0]
                current_paper['url'] = paper_id
        
        return papers
    
    def discover_huggingface_agents(self) -> List[Dict[str, Any]]:
        """Discover AI agents on Hugging Face"""
        logger.info("Discovering AI agents on Hugging Face...")
        
        discovered = []
        
        for query in self.discovery_sources["huggingface"]["queries"]:
            try:
                logger.info(f"Searching Hugging Face for: {query}")
                
                # Hugging Face search API
                url = "https://huggingface.co/api/spaces"
                params = {
                    'search': query,
                    'limit': 20,
                    'sort': 'likes',
                    'direction': -1
                }
                
                response = self.session.get(url, params=params, timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    for space in data:
                        if self._is_relevant_hf_space(space):
                            competitor = {
                                "name": space['id'],
                                "category": "Demo/Implementation",
                                "description": space.get('description', 'No description'),
                                "capabilities": ["Live demo", "Implementation"],
                                "market_position": "Demo",
                                "funding": "Unknown",
                                "team_size": "Unknown",
                                "technical_approach": "Hugging Face space",
                                "competitive_threat": "Low",
                                "discovery_date": datetime.now().strftime("%Y-%m-%d"),
                                "last_updated": space.get('updatedAt', 'Unknown')[:10],
                                "sources": ["Hugging Face"],
                                "hf_data": {
                                    "likes": space.get('likes', 0),
                                    "url": f"https://huggingface.co/spaces/{space['id']}",
                                    "sdk": space.get('sdk', 'Unknown')
                                }
                            }
                            
                            discovered.append(competitor)
                
                # Respect rate limits
                time.sleep(1)
                
            except Exception as e:
                logger.error(f"Error searching Hugging Face for '{query}': {str(e)}")
                continue
        
        logger.info(f"Discovered {len(discovered)} AI agent spaces on Hugging Face")
        return discovered
    
    def _is_relevant_hf_space(self, space: Dict[str, Any]) -> bool:
        """Check if Hugging Face space is relevant to AI agents"""
        relevant_keywords = ['agent', 'autonomous', 'assistant', 'ai', 'research']
        
        text_to_check = f"{space['id']} {space.get('description', '')}".lower()
        
        return any(keyword in text_to_check for keyword in relevant_keywords)
    
    def run_full_discovery(self) -> Dict[str, Any]:
        """Run complete competitor discovery process"""
        logger.info("Starting full competitor discovery...")
        
        # Collect data from all sources
        github_agents = self.discover_github_agents()
        arxiv_papers = self.discover_arxiv_papers()
        hf_agents = self.discover_huggingface_agents()
        
        # Combine all discovered competitors
        all_discovered = github_agents + arxiv_papers + hf_agents
        
        # Combine with known competitors
        all_competitors = self.known_competitors + all_discovered
        
        # Create summary
        summary = {
            'discovery_timestamp': datetime.now().isoformat(),
            'total_competitors': len(all_competitors),
            'discovery_summary': {
                'github_repositories': len(github_agents),
                'arxiv_papers': len(arxiv_papers),
                'huggingface_spaces': len(hf_agents),
                'known_competitors': len(self.known_competitors)
            },
            'competitive_landscape': {
                'high_threat': len([c for c in all_competitors if c['competitive_threat'] == 'High']),
                'medium_threat': len([c for c in all_competitors if c['competitive_threat'] == 'Medium']),
                'low_threat': len([c for c in all_competitors if c['competitive_threat'] == 'Low'])
            }
        }
        
        # Save data
        self._save_discovery_data(all_competitors, summary)
        
        logger.info("Competitor discovery completed!")
        return {
            'competitors': all_competitors,
            'summary': summary,
            'discovery_data': {
                'github': github_agents,
                'arxiv': arxiv_papers,
                'huggingface': hf_agents
            }
        }
    
    def _save_discovery_data(self, competitors: List[Dict], summary: Dict):
        """Save discovery data to files"""
        # Save all competitors
        with open(os.path.join(self.output_dir, 'all_competitors.json'), 'w') as f:
            json.dump(competitors, f, indent=2, ensure_ascii=False)
        
        # Save summary
        with open(os.path.join(self.output_dir, 'discovery_summary.json'), 'w') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        # Save by source
        sources = ['github', 'arxiv', 'huggingface']
        for source in sources:
            source_file = os.path.join(self.output_dir, f'{source}_competitors.json')
            if os.path.exists(source_file):
                with open(source_file, 'w') as f:
                    json.dump(competitors, f, indent=2, ensure_ascii=False)
        
        # Save as CSV for analysis
        df = pd.DataFrame(competitors)
        df.to_csv(os.path.join(self.output_dir, 'competitors.csv'), index=False)
        
        logger.info(f"Discovery data saved to: {self.output_dir}/")

def main():
    """Main function to run competitor discovery"""
    print("🔍 AI Agent Competitor Discovery Tool")
    print("=" * 50)
    
    # Initialize discovery tool
    discovery = CompetitorDiscovery()
    
    # Run discovery
    try:
        results = discovery.run_full_discovery()
        
        print("\n✅ Competitor discovery completed successfully!")
        print(f"📁 Data saved to: {discovery.output_dir}/")
        print(f"📊 Total competitors discovered: {results['summary']['total_competitors']}")
        
        # Display summary
        summary = results['summary']['discovery_summary']
        print(f"\n📈 Discovery Summary:")
        print(f"  • GitHub repositories: {summary['github_repositories']}")
        print(f"  • arXiv papers: {summary['arxiv_papers']}")
        print(f"  • Hugging Face spaces: {summary['huggingface_spaces']}")
        print(f"  • Known competitors: {summary['known_competitors']}")
        
        # Display threat levels
        threats = results['summary']['competitive_landscape']
        print(f"\n⚠️ Competitive Threat Levels:")
        print(f"  • High threat: {threats['high_threat']}")
        print(f"  • Medium threat: {threats['medium_threat']}")
        print(f"  • Low threat: {threats['low_threat']}")
        
        print(f"\n📋 Check the '{discovery.output_dir}' folder for detailed data files.")
        
    except Exception as e:
        print(f"\n❌ Error during discovery: {str(e)}")
        logger.error(f"Main execution error: {str(e)}")

if __name__ == "__main__":
    main() 