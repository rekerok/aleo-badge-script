import socket
import time
import socks
import csv
import random
import shutil
import subprocess
import os
import github
import requests
from github import AuthenticatedUser, Repository
from loguru import logger
import tqdm


def read_file_line(path: str):
    try:
        with open(path, "r") as file:
            lines = [i.strip() for i in file.readlines()]
            return lines
    except:
        return []


### SETTINGS ###
SLEEP = (3500, 6000)
NAME_CSV = "data.csv"
PROXY_FROM_TXT = False
PROXIES = read_file_line("files/proxy.txt")

### LEO
APPS = ["tictactoe"]  # ["lottery", "tictactoe", "token"]

### GITGUB
NAMES_REPO = read_file_line("files/repo_names.txt")
LIST_FIRST_COMMITS = read_file_line("files/first_commit_repo.txt")
BRANCH_NAMES = ["main", "master"]
MESSAGES_FOR_ISSUE = [
    """
## 🥇 Leo Contributor Badge

Hi Aleo team! I'm claiming my contributor badge for completing a developer tutorial. 😀

Github Username: {username}
Tutorial Repo: {repo_url}
Requested badge: tutorial""",
    """
## 🥇 Leo Contributor Badge

Hi Aleo team! I'm claiming my contributor badge for completing a developer tutorial. 😀

Github Username: {username}
Tutorial Repo: {repo_url}
Requested badge: Tutorial""",
]
TITLES_ISSUE = ["[Badge - {username}]"]

BEGIN_FOLDER = os.getcwd()


def clear_folder(folder_path):
    try:
        # Получаем список подпапок внутри папки projects/
        subfolders = [f.path for f in os.scandir(folder_path) if f.is_dir()]

        # Удаляем каждую подпапку внутри projects/
        for subfolder in subfolders:
            shutil.rmtree(subfolder)

        logger.info(f'Подпапки и файлы внутри папки "{folder_path}" успешно удалены.')
    except Exception as e:
        logger.error(
            f'Ошибка при удалении подпапок и файлов внутри папки "{folder_path}": {e}'
        )


def create_folder(dir_path):
    try:
        os.mkdir(dir_path)
        return dir_path
    except:
        return None


def sleep_view(sleep: tuple):
    for i in tqdm.tqdm(range(random.randint(sleep[0], sleep[1]))):
        time.sleep(1)


### SUBPROCESS
def start_command(command, input=None):
    try:
        result = subprocess.run(
            args=command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            # text=True,
            input=input,
        )
        # print(result.stdout)
        return result.returncode
    except subprocess.CalledProcessError as e:
        print(e)
        return 1


def aleo_account(private_key="x"):
    if private_key.lower() != "x":
        return start_command(f"leo account import {private_key}")


def create_example_app(app):
    return start_command(f"leo example {app}")


def deploy_app():
    return start_command("leo run new")


def initialize_git_repository(branch_name):
    return start_command(f"git init -b {branch_name}")


def add_and_commit_files(commit_message):
    try:
        subprocess.run(
            "git add .",
            shell=True,
            check=True,
            stderr=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
        )
        subprocess.run(
            f'git commit -m "{commit_message}"',
            shell=True,
            check=True,
            stderr=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
        )
        return 0
    except subprocess.CalledProcessError as e:
        return e.returncode


def set_global_username_email(new_username, new_email):
    result1 = start_command(f"git config --global user.email {new_email}")
    result2 = start_command(f"git config --global user.name {new_username}")
    return result1 + result2


def remote_add(name_repo, username, token):
    # https://[PERSONALACCESSTOKEN]@github.com/[USERNAME]/[REPO].git
    return start_command(
        f"git remote add origin https://{token}@github.com/{username}/{name_repo}.git"
    )


def push(branch):
    return start_command(f"git push -u origin {branch}")


### PYGITHUB


def create_repo(user: AuthenticatedUser, names_repo: list[str]) -> Repository:
    for name_repo in names_repo:
        try:
            repo = user.create_repo(name=name_repo)
            logger.success(f"repo {repo.html_url} was created")
            return repo
        except Exception as error:
            user.get_repo(name=name_repo).delete()
            logger.error(f"https://github.com/{user.login}/{name_repo} was deleted")


def create_issue(repo_to_issue, title, body, username, url_self_repo):
    try:
        body = body.format(username=username, repo_url=url_self_repo)
        issue = repo_to_issue.create_issue(title=title, body=body)
        return issue.html_url
    except:
        return None


### PROXY
def change_proxy(proxy):
    proxy = proxy.split(":")
    socks.set_default_proxy(
        socks.HTTP,
        addr=proxy[0],
        port=int(proxy[1]),
        username=proxy[2],
        password=proxy[3],
    )
    socket.socket = socks.socksocket


def get_external_ip():
    try:
        response = requests.get("https://api64.ipify.org?format=json")
        if response.status_code == 200:
            ip_data = response.json()
            return ip_data.get("ip")
        else:
            return None
    except Exception as e:
        print(f"Error getting external IP: {e}")
        return None


def main():
    try:
        os.makedirs("projects")
        print(f"Директория projects успешно создана.")
    except FileExistsError:
        print(f"Директория projects уже существует.")
    except Exception as e:
        print(f"Ошибка при создании директории: {e}")
    clear_folder(folder_path="projects")
    result = list()
    with open(NAME_CSV, "r") as file:
        data = list(csv.DictReader(file, delimiter=","))
        for row in random.sample(data, len(data)):
            if PROXY_FROM_TXT:
                proxy = random.choice(PROXIES)
                change_proxy(proxy)
            else:
                proxy = row.get("PROXY")
                change_proxy(proxy)
            external_ip = get_external_ip()
            if external_ip:
                logger.info(f"IP: {external_ip}")
            else:
                logger.error("PROXY NOT WORKING")
                break
            with github.Github(
                login_or_token=row.get("TOKEN"),
            ) as gh:
                try:
                    user = gh.get_user()
                    commit_message = random.choice(LIST_FIRST_COMMITS)
                    branch = random.choice(BRANCH_NAMES)
                    app = random.choice(APPS)
                    random.shuffle(NAMES_REPO)
                    logger.info(f"ACC {user.login}")
                    dir = create_folder(f"projects/{user.login}")
                    if os.path.exists(dir):
                        logger.success(f'directory "{dir}" was created')
                    else:
                        logger.error(f'directory "{dir}" was not created')
                        continue

                    os.chdir(dir)
                    logger.info(f"directory now is {os.getcwd()}")

                    status_create_acc = aleo_account(row.get("ALEO PRIVATE"))
                    if status_create_acc == 0:
                        logger.success(
                            "leo account import command executed successfully"
                        )
                    else:
                        logger.error("leo account import command failed")
                        continue

                    status_create_ecample = create_example_app(app=app)
                    if status_create_ecample == 0:
                        logger.success(
                            f"leo example {app} command executed successfully"
                        )
                    else:
                        logger.error(f"leo example {app} command failed")
                        continue

                    os.chdir(app)
                    logger.info(f"directory now is {os.getcwd()}")

                    status_deploy_app = deploy_app()
                    if status_deploy_app == 0:
                        logger.success("leo run new command executed successfully")
                        sleep_view((60, 200))
                    else:
                        logger.error("leo run new command failed")
                        continue

                    result_init_local_repo = initialize_git_repository(branch)
                    if result_init_local_repo == 0:
                        logger.success(
                            f"Git repository initialized successfully with {branch} branch."
                        )
                        sleep_view((60, 200))
                    else:
                        logger.error(f"Error initializing Git repository:")
                        continue

                    status_set_name_email = set_global_username_email(
                        new_username=user.login, new_email=row.get("EMAIL")
                    )
                    if status_set_name_email == 0:
                        logger.success(
                            "Git global username and email set successfully."
                        )
                        sleep_view((60, 200))
                    else:
                        logger.error(f"Error setting git global username and email")
                        continue

                    status_create_commit = add_and_commit_files(
                        commit_message=commit_message
                    )
                    if status_create_commit == 0:
                        logger.success(f'Git commit "{commit_message}" successful.')
                        sleep_view((60, 200))
                    else:
                        logger.error(f'Git commit "{commit_message}" not created')
                        continue

                    repo = create_repo(user, NAMES_REPO)

                    result_remote_add = remote_add(
                        name_repo=repo.name,
                        username=user.login,
                        token=row.get("TOKEN"),
                    )
                    if result_remote_add == 0:
                        logger.success("remote add successfully")
                        sleep_view((60, 200))
                    else:
                        logger.error(f"Error remote add")
                        continue

                    result_push_in_repo = push(branch=branch)
                    if result_push_in_repo == 0:
                        logger.success("push in repo successfully")
                        sleep_view((60, 200))
                    else:
                        logger.error(f"Error push in repo")
                        continue

                    issue_link = create_issue(
                        repo_to_issue=gh.get_repo("AleoHQ/leo"),  # TO ALEO
                        # repo_to_issue=repo,  # SELF REPO FOR CHECK
                        title=random.choice(TITLES_ISSUE).format(username=user.login),
                        body=random.choice(MESSAGES_FOR_ISSUE),
                        username=user.login,
                        url_self_repo=repo.html_url,
                    )

                    if issue_link:
                        logger.success(f"Issue create successfully -- {issue_link}")
                    else:
                        logger.error(f"Issue not created")
                        continue

                    result.append(
                        {
                            "username": user.login,
                            "email": row.get("EMAIL"),
                            "link_to_issue": issue_link,
                            "ip": proxy,
                        }
                    )

                    logger.info("------------------")
                except Exception as error:
                    print(error)
                os.chdir(BEGIN_FOLDER)
                sleep_view(SLEEP)

    with open("result.csv", "w") as result_file:
        writter = csv.DictWriter(result_file, fieldnames=result[0].keys())
        writter.writeheader()
        writter.writerows(result)


if __name__ == "__main__":
    main()
