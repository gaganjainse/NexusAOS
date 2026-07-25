# Specialization framework applied (AGENTS.md line 36-39): AB/AP balance + DNA blueprint + governance + provenance + Voice DNA. Source: dataset/ab_ap_balance/AB_AP_BALANCE_RULES.md + archives/dna_core/blueprints/COMPLETE_ARCHITECTURE.md.
"""
SeshaAOS - GitHub Repository Scanner
Version: 1.0.0
Description: Scans GitHub organizations/repos for patterns, extracts learnings, and feeds them into SeshaAOS.
MIT License - can copy, adapt, improve from langchain-ai and other MIT-licensed repos.
"""
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

_python_root = Path(__file__).resolve().parent.parent.parent.parent
if str(_python_root) not in sys.path:
    sys.path.insert(0, str(_python_root))
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from typing import Callable


@dataclass
class RepoInfo:
    """Repository metadata and extracted patterns."""
    name: str
    full_name: str
    description: str
    language: str
    stars: int
    forks: int
    topics: List[str]
    license: Optional[str]
    url: str
    default_branch: str
    created_at: str
    updated_at: str
    size_kb: int
    patterns: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.patterns is None:
            self.patterns = {}


class GitHubScanner:
    """Scans GitHub organizations and repositories for patterns and learnings."""
    
    def __init__(self, base_dir: Path, token: Optional[str] = None):
        self.base_dir = base_dir
        self.token = token or os.environ.get("GITHUB_TOKEN")
        self.api_base = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github+json",
            "User-Agent": "SeshaAOS-GitHubScanner/1.0",
        }
        if self.token:
            self.headers["Authorization"] = f"Bearer {self.token}"
        
        self.scan_dir = base_dir / "core" / "monitoring" / "github_scans"
        self.scan_dir.mkdir(parents=True, exist_ok=True)
        
        # Pattern extractors
        self.extractors: List[Callable[[Dict], Dict]] = [
            self._extract_architecture_patterns,
            self._extract_testing_patterns,
            self._extract_ci_cd_patterns,
            self._extract_dependency_patterns,
            self._extract_agent_patterns,
            self._extract_graph_patterns,
            self._extract_streaming_patterns,
        ]
    
    def _request(self, url: str, params: Optional[Dict] = None) -> Optional[Dict]:
        """Make authenticated GitHub API request."""
        if params:
            url = f"{url}?{urllib.parse.urlencode(params)}"
        req = urllib.request.Request(url, headers=self.headers)
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                if resp.status == 200:
                    return json.load(resp)
                elif resp.status == 403:
                    print(f"Rate limited: {resp.headers.get('X-RateLimit-Remaining', 'unknown')} remaining")
                    return None
                else:
                    print(f"API error {resp.status}: {url}")
                    return None
        except urllib.error.HTTPError as e:
            if e.code == 403:
                print(f"Rate limited or forbidden: {e}")
            else:
                print(f"HTTP error {e.code}: {url}")
            return None
        except Exception as e:
            print(f"Request error: {e}")
            return None
    
    def scan_org(self, org: str, max_repos: int = 100) -> List[RepoInfo]:
        """Scan all repositories in an organization."""
        repos = []
        page = 1
        per_page = 100
        
        while len(repos) < max_repos:
            url = f"{self.api_base}/orgs/{org}/repos"
            params = {
                "type": "all",
                "sort": "updated",
                "direction": "desc",
                "per_page": per_page,
                "page": page,
            }
            data = self._request(url, params)
            if not data or len(data) == 0:
                break
            
            for repo_data in data:
                if len(repos) >= max_repos:
                    break
                repo = self._parse_repo(repo_data)
                repos.append(repo)
            
            page += 1
            time.sleep(0.5)  # Be nice to API
        
        return repos

    def search_repos(self, query: str, sort: str = "stars", order: str = "desc", max_results: int = 10) -> List[RepoInfo]:
        """Search for repositories on GitHub."""
        url = f"{self.api_base}/search/repositories"
        params = {
            "q": query,
            "sort": sort,
            "order": order,
            "per_page": max_results
        }
        data = self._request(url, params)
        if not data or "items" not in data:
            return []
            
        return [self._parse_repo(item) for item in data["items"]]
    
    def _parse_repo(self, data: Dict) -> RepoInfo:
        return RepoInfo(
            name=data["name"],
            full_name=data["full_name"],
            description=data.get("description") or "",
            language=data.get("language") or "",
            stars=data.get("stargazers_count", 0),
            forks=data.get("forks_count", 0),
            topics=data.get("topics", []),
            license=data.get("license", {}).get("spdx_id") if data.get("license") else None,
            url=data["html_url"],
            default_branch=data.get("default_branch", "main"),
            created_at=data["created_at"],
            updated_at=data["updated_at"],
            size_kb=data.get("size", 0),
        )
    
    def scan_repo(self, repo: RepoInfo) -> RepoInfo:
        """Deep scan a single repository for patterns."""
        print(f"Scanning {repo.full_name}...")
        
        # Get repo tree
        tree = self._get_repo_tree(repo)
        if not tree:
            return repo
        
        # Extract patterns from key files
        key_files = self._identify_key_files(tree)
        for file_path in key_files:
            content = self._get_file_content(repo, file_path)
            if content:
                for extractor in self.extractors:
                    patterns = extractor({"path": file_path, "content": content, "repo": repo})
                    repo.patterns.update(patterns)
        
        # Save scan results
        self._save_scan(repo)
        
        return repo
    
    def _get_repo_tree(self, repo: RepoInfo) -> Optional[List[Dict]]:
        """Get recursive tree of repository."""
        url = f"{self.api_base}/repos/{repo.full_name}/git/trees/{repo.default_branch}"
        params = {"recursive": "1"}
        data = self._request(url, params)
        if data and "tree" in data:
            return data["tree"]
        return None
    
    def _identify_key_files(self, tree: List[Dict]) -> List[str]:
        """Identify key files for pattern extraction."""
        key_patterns = [
            r".*\.py$", r".*\.ts$", r".*\.tsx$", r".*\.js$", r".*\.jsx$",
            r".*\.md$", r".*\.yaml$", r".*\.yml$", r".*\.toml$", r"Dockerfile.*",
            r"Makefile.*", r"pyproject\.toml$", r"setup\.py$", r"requirements.*\.txt$",
            r".*\.json$", r".*\.rs$", r".*\.go$",
        ]
        key_dirs = [r"src/", r"lib/", r"tests/", r"examples/", r"docs/", r".github/"]
        
        key_files = []
        for item in tree:
            if item["type"] != "blob":
                continue
            path = item["path"]
            # Check if in key directory or matches key pattern
            if any(path.startswith(d) for d in key_dirs):
                key_files.append(path)
            elif any(re.match(p, path) for p in key_patterns):
                key_files.append(path)
        
        # Limit to avoid too many API calls
        return key_files[:50]
    
    def _get_file_content(self, repo: RepoInfo, file_path: str) -> Optional[str]:
        """Get file content from repo."""
        url = f"{self.api_base}/repos/{repo.full_name}/contents/{file_path}"
        params = {"ref": repo.default_branch}
        data = self._request(url, params)
        if data and "content" in data:
            import base64
            try:
                return base64.b64decode(data["content"]).decode("utf-8", errors="ignore")
            except:
                return None
        return None
    
    # --- Pattern Extractors ---
    
    def _extract_architecture_patterns(self, file_info: Dict) -> Dict:
        """Extract architectural patterns."""
        content = file_info["content"]
        patterns = {}
        
        # Class-based patterns
        if re.search(r"class\s+\w+\s*\(.*Base.*\):", content):
            patterns["inheritance"] = True
        if re.search(r"@dataclass", content):
            patterns["dataclasses"] = True
        if re.search(r"@abstractmethod", content):
            patterns["abstract_base"] = True
        if re.search(r"Protocol\[", content) or re.search(r"class.*Protocol:", content):
            patterns["protocols"] = True
        if re.search(r"typing\.Protocol", content):
            patterns["structural_typing"] = True
        
        # Dependency injection
        if re.search(r"dependency.*inject|inject.*dependenc", content, re.I):
            patterns["dependency_injection"] = True
        
        # Factory patterns
        if re.search(r"factory|Factory", content):
            patterns["factory"] = True
        
        return {"architecture": patterns} if patterns else {}
    
    def _extract_testing_patterns(self, file_info: Dict) -> Dict:
        """Extract testing patterns."""
        content = file_info["content"]
        path = file_info["path"]
        patterns = {}
        
        if "test" not in path.lower():
            return {}
        
        if re.search(r"pytest|unittest", content):
            patterns["framework"] = "pytest" if "pytest" in content else "unittest"
        if re.search(r"@pytest\.fixture", content):
            patterns["fixtures"] = True
        if re.search(r"mock|Mock|patch", content):
            patterns["mocking"] = True
        if re.search(r"parametrize|parameterize", content):
            patterns["parametrized"] = True
        if re.search(r"hypothesis|property.*test", content, re.I):
            patterns["property_based"] = True
        if re.search(r"async.*test|pytest\.asyncio", content):
            patterns["async_testing"] = True
        
        return {"testing": patterns} if patterns else {}
    
    def _extract_ci_cd_patterns(self, file_info: Dict) -> Dict:
        """Extract CI/CD patterns."""
        path = file_info["path"]
        content = file_info["content"]
        patterns = {}
        
        if ".github/workflows" in path or ".gitlab-ci" in path or "azure-pipelines" in path or "Jenkinsfile" in path:
            if "github" in path:
                patterns["platform"] = "github_actions"
            elif "gitlab" in path:
                patterns["platform"] = "gitlab_ci"
            elif "azure" in path:
                patterns["platform"] = "azure_pipelines"
            
            if re.search(r"runs-on:\s*\[", content):
                patterns["matrix_builds"] = True
            if re.search(r"cache:|actions/cache", content):
                patterns["caching"] = True
            if re.search(r"codecov|coveralls", content):
                patterns["coverage_reporting"] = True
            if re.search(r"security|dependabot|snyk|trivy", content, re.I):
                patterns["security_scanning"] = True
            if re.search(r"deploy|release|publish", content, re.I):
                patterns["deployment"] = True
        
        return {"ci_cd": patterns} if patterns else {}
    
    def _extract_dependency_patterns(self, file_info: Dict) -> Dict:
        """Extract dependency management patterns."""
        path = file_info["path"]
        content = file_info["content"]
        patterns = {}
        
        if path.endswith("pyproject.toml"):
            if "poetry" in content.lower() or "[tool.poetry]" in content:
                patterns["poetry"] = True
            if "[tool.uv]" in content or "uv" in content:
                patterns["uv"] = True
            if "dependencies" in content:
                patterns["explicit_deps"] = True
        elif path.endswith("requirements.txt") or path.endswith("requirements-dev.txt"):
            patterns["pip_requirements"] = True
        elif path == "package.json":
            if '"dependencies"' in content:
                patterns["npm_deps"] = True
            if '"devDependencies"' in content:
                patterns["dev_deps"] = True
            if '"workspaces"' in content:
                patterns["monorepo"] = True
        elif path == "Cargo.toml":
            if "[dependencies]" in content:
                patterns["cargo_deps"] = True
            if "workspace" in content:
                patterns["cargo_workspace"] = True
        
        return {"dependencies": patterns} if patterns else {}
    
    def _extract_agent_patterns(self, file_info: Dict) -> Dict:
        """Extract LangGraph/LangChain agent patterns."""
        content = file_info["content"]
        path = file_info["path"]
        patterns = {}
        
        # LangGraph patterns
        if "langgraph" in content.lower() or "StateGraph" in content:
            patterns["langgraph"] = True
            if "StateGraph" in content:
                patterns["state_graph"] = True
            if "add_node" in content:
                patterns["node_based"] = True
            if "add_edge" in content or "add_conditional_edges" in content:
                patterns["edge_based"] = True
            if "compile()" in content:
                patterns["compiled_graph"] = True
            if "checkpointer" in content or "MemorySaver" in content:
                patterns["persistence"] = True
            if "interrupt" in content.lower():
                patterns["human_in_loop"] = True
        
        # LangChain patterns
        if "langchain" in content.lower():
            patterns["langchain"] = True
            if "RunnableSequence" in content or "RunnableParallel" in content:
                patterns["runnable_composition"] = True
            if "AgentExecutor" in content:
                patterns["agent_executor"] = True
            if "create_react_agent" in content or "create_tool_calling_agent" in content:
                patterns["agent_creation"] = True
            if "BaseCallbackHandler" in content or "CallbackManager" in content:
                patterns["callbacks"] = True
            if "RetrievalQA" in content or "VectorStore" in content:
                patterns["rag"] = True
        
        # Tool patterns
        if "@tool" in content or "Tool(" in content:
            patterns["tool_definition"] = True
        if "BaseTool" in content:
            patterns["base_tool"] = True
        
        # LLM patterns
        if "ChatOpenAI" in content or "ChatAnthropic" in content:
            patterns["llm_integration"] = True
        if "temperature" in content:
            patterns["llm_config"] = True
        if "streaming" in content.lower() or "stream(" in content:
            patterns["streaming"] = True
        
        return {"agent": patterns} if patterns else {}
    
    def _extract_graph_patterns(self, file_info: Dict) -> Dict:
        """Extract graph/state machine patterns."""
        content = file_info["content"]
        patterns = {}
        
        if re.search(r"networkx|graphviz|pygraph", content, re.I):
            patterns["graph_lib"] = True
        if re.search(r"state.*machine|finite.*state|transitions", content, re.I):
            patterns["state_machine"] = True
        if re.search(r"DAG|topological|dependency.*graph", content, re.I):
            patterns["dag"] = True
        
        return {"graph": patterns} if patterns else {}
    
    def _extract_streaming_patterns(self, file_info: Dict) -> Dict:
        """Extract async/streaming patterns."""
        content = file_info["content"]
        patterns = {}
        
        if "async def" in content:
            patterns["async_functions"] = True
        if "await " in content:
            patterns["await_usage"] = True
        if "asyncio" in content:
            patterns["asyncio"] = True
        if "async for" in content or "async with" in content:
            patterns["async_iterators"] = True
        if "aiohttp" in content or "httpx" in content:
            patterns["async_http"] = True
        if "queue" in content.lower() and "asyncio" in content:
            patterns["async_queue"] = True
        if "asyncio.create_task" in content or "asyncio.gather" in content:
            patterns["task_management"] = True
        
        return {"streaming": patterns} if patterns else {}
    
    def _save_scan(self, repo: RepoInfo):
        """Save scan results."""
        scan_file = self.scan_dir / f"{repo.name}_scan.json"
        scan_data = {
            "repo": asdict(repo),
            "scanned_at": time.time(),
        }
        with open(scan_file, "w", encoding="utf-8") as f:
            json.dump(scan_data, f, indent=2, default=str)
    
    def generate_report(self, repos: List[RepoInfo]) -> Dict:
        """Generate aggregate report from all scanned repos."""
        total_stars = sum(r.stars for r in repos)
        total_forks = sum(r.forks for r in repos)
        languages = {}
        topics = {}
        patterns_agg = {}
        
        for repo in repos:
            lang = repo.language or "Unknown"
            languages[lang] = languages.get(lang, 0) + 1
            for topic in repo.topics:
                topics[topic] = topics.get(topic, 0) + 1
            
            for category, patterns in repo.patterns.items():
                if category not in patterns_agg:
                    patterns_agg[category] = {}
                for pattern, present in patterns.items():
                    if present:
                        patterns_agg[category][pattern] = patterns_agg[category].get(pattern, 0) + 1
        
        return {
            "scanned_at": time.time(),
            "total_repos": len(repos),
            "total_stars": total_stars,
            "total_forks": total_forks,
            "languages": dict(sorted(languages.items(), key=lambda x: -x[1])),
            "top_topics": dict(sorted(topics.items(), key=lambda x: -x[1])[:20]),
            "patterns": patterns_agg,
            "repos": [{"name": r.name, "stars": r.stars, "patterns": r.patterns} for r in repos],
        }


def main():
    """Main entry point for scanning langchain-ai org."""
    base_dir = Path(__file__).resolve().parent.parent.parent.parent
    scanner = GitHubScanner(base_dir)
    
    print("Scanning langchain-ai organization...")
    repos = scanner.scan_org("langchain-ai", max_repos=50)
    
    print(f"Found {len(repos)} repositories. Deep scanning...")
    for repo in repos[:20]:  # Deep scan top 20
        scanner.scan_repo(repo)
    
    # Generate report
    report = scanner.generate_report(repos)
    report_file = scanner.scan_dir / "langchain_ai_report.json"
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, default=str)
    
    print(f"\nReport saved to {report_file}")
    print(f"Total repos: {report['total_repos']}")
    print(f"Total stars: {report['total_stars']}")
    print(f"Languages: {report['languages']}")
    print(f"Top topics: {list(report['top_topics'].keys())[:10]}")
    print(f"Pattern categories: {list(report['patterns'].keys())}")


if __name__ == "__main__":
    main()
