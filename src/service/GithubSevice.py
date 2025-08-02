
from dotenv import load_dotenv
import os
import requests
import time


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
            results = []
            for c in commits_data:
                commit_message = c['commit']['message']
                commit_sha = c['sha']
                commit_url = f'https://github.com/{owner}/{repo}/commit/{commit_sha}'
                results.append({
                    'message': commit_message,
                    'sha': commit_sha,
                    'url': commit_url
                })
                time.sleep(0.3)
            return results
        else:
            error_msg = f"Error {response.status_code}: {response.json().get('message', 'No se pudo obtener información del repositorio')}"
            return {'error': error_msg}

    def get_user_starred_repositories(self, user):
        url = f'https://api.github.com/users/{user}/starred'
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            repositories_data = response.json()
            results = []
            for repo in repositories_data:
                repo_name = repo['name']
                repo_owner = repo['owner']['login']
                repo_url = repo['html_url']
                repo_description = repo.get('description', 'No description')
                results.append({
                    'name': repo_name,
                    'owner': repo_owner,
                    'url': repo_url,
                    'description': repo_description
                })
                time.sleep(0.3)
            return results
        else:
            error_msg = f'Error {response.status_code}: {response.json().get("message", "No se pudo obtener información del usuario")}'
            return {'error': error_msg}
