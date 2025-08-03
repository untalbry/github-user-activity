
from dotenv import load_dotenv
import os
import requests
from model.Repository import Repository
from model.Event import Event

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

    def get_user_starred_repositories(self, user):
        url = f'https://api.github.com/users/{user}/starred'
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            repositories_data = response.json()
            results = []
            for repo in repositories_data:
                repo = Repository(repo['name'], repo['owner']['login'], repo['html_url'], repo.get('description', 'No description'))
                results.append(repo)
            return results
        else:
            error_msg = f'Error {response.status_code}: {response.json().get("message", "No se pudo obtener información del usuario")}'
            return {'error': error_msg}
    def get_user_events(self, user):
        url = f'https://api.github.com/users/{user}/events'
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200: 
            repositories_data = response.json()
            results = []
            for event in repositories_data:
                event_fetched = Event(type=event['type'], repo_name=event['repo']['name'], created_at=event['created_at'],commits=event['payload'].get('size', 0), branch=event['payload'].get('ref', 0))
                results.append(event_fetched)
            return results 
        else:
            error_msg = f'Error {response.status_code}: {response.json().get("message", "No se pudo obtener información del usuario")}'
            return {'error': error_msg}

