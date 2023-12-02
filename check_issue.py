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


def read_file_lines(path: str) -> list[str]:
    try:
        with open(path, "r") as file:
            lines = [i.strip() for i in file.readlines()]
            return lines
    except:
        return []


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


tokens = read_file_lines("files/gh_tokens.txt")
proxy = read_file_lines("files/proxy.txt")
with github.Github() as gh:
    cotributers = [i.login for i in gh.get_repo("AleoHQ/leo").get_contributors()]


for token in tokens:
    change_proxy(random.choice(proxy))
    with github.Github(login_or_token=token) as gh:
        user = gh.get_user()
        if user.login in cotributers:
            logger.success(f"{user.login}")
        else:
            logger.error(f"{user.login}")
