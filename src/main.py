from service.GithubSevice import GithubService
import threading
import time
from alive_progress import alive_bar
from InquirerPy import inquirer

def show_bar(thread):
    with alive_bar(title='Procesando...', stats=False, elapsed=False, spinner='dots') as bar:
        while thread.is_alive():
            bar()
            time.sleep(0.1)

def select_option():
    options = ["get-user-starred-repositories", "exit"]
    option = inquirer.rawlist(
    message="Select an option:", default=2, choices=options
).execute()
    return option

def main():
    github_service = GithubService()
    results = []

    def fetch_user_starred_repositories():
        nonlocal results
        results = github_service.get_user_starred_repositories(user)

    option = select_option()
    if option == "get-user-starred-repositories":
        user = input("Dame el nombre del usuario\n")
        thread = threading.Thread(target=fetch_user_starred_repositories)
        thread.start()
        show_bar(thread)
        thread.join()
        if isinstance(results, list):
            for repo in results:
                print(f"⭐ {repo.owner}/{repo.name} - {repo.url}")
                if repo.description != 'No description':
                    print(f"   📝 {repo.description}")
                print()
        elif isinstance(results, dict) and 'error' in results:
            print(results['error'])
    elif option == "exit":
        print("Thanks for using ❤️")
if __name__ == "__main__":
    main()