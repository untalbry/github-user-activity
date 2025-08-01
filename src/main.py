from service.GithubSevice import GithubService
import sys 
import threading
import time
from alive_progress import alive_bar

def main():
    if len(sys.argv) == 4 and sys.argv[1] == '--commits':
        owner = sys.argv[2]
        repo = sys.argv[3]
        
        def fetch_commits():
            github_service = GithubService()
            github_service.get_all_commits(owner=owner, repo=repo)

        def show_bar(thread):
            with alive_bar(title='Procesando...') as bar:
                while thread.is_alive():
                    bar()
                    time.sleep(0.1)

        hilo = threading.Thread(target=fetch_commits)
        hilo.start()
        show_bar(hilo)

        hilo.join()        
        print("¡Listo!")
   
if __name__ == "__main__":
    main()