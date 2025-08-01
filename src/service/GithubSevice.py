
from dotenv import load_dotenv
import os
import requests

class GithubService():
    def __init__(self):
        env_path = os.path.join(os.path.dirname(__file__), '../..', 'venv', '.env')
        load_dotenv(env_path)
        self.token = os.getenv('GITHUB-API-TOKEN')
        if not self.token:
            raise ValueError("ERROR 404: Entity not found")
        # SET: Headers to connect with Github API 
        self.headers = {
            'Authorization': f'token {self.token}',
            'Accept': 'application/vnd.github.v3+json'
        }

    def get_all_commits(self, owner, repo):
        url = f'https://api.github.com/repos/{owner}/{repo}/commits'
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            commits_data = response.json()
            for c in commits_data:
                commit_message = c['commit']['message']
                commit_sha = c['sha']
                commit_url = f'https://github.com/{owner}/{repo}/commit/{commit_sha}'
                print(f"Commit: {commit_message} - URL: {commit_url}")
        else:
            print(f"Error {response.status_code}: {response.json().get('message', 'No se pudo obtener información del repositorio')}") 