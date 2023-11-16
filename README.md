# Script abuse aleo badge

Скрипт исполняет [эту инструкцию](https://t.me/wallet_world/221)

## Шаги
1) Нужно установить _Leo_ на сервак (на Macos и Linux работает без проблем, на винде не пробовал)

 ```bash
 # Install rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh # тут просто прокликать Enter и дожадться загрузки
source "$HOME/.cargo/env"

# Download the source code
git clone https://github.com/AleoHQ/leo
cd leo

# Install 'leo'
$ cargo install --path .

cd
 ```

2) Склонировать репозиторий
```bash
git clone https://gitfront.io/r/rekerok05/RAMmDpZ9ZD19/aleo-badge-script.git

cd aleo-badge-script
```

3) В файле _main.py_ выставить: 
* **SLEEP** - сколько будет спать между аккаунтами
* **NAME_CSV** - файл откуда будут браться данные
* **PROXY_FROM_TXT** - если *True* то прокси будут браться случайным образом из файла *files/proxy.txt*, если *False* то из файла *NAME_CSV*

4) Заполнить **NAME_CSV**   
Там 4 поля 
```
ALEO PRIVATE,TOKEN,EMAIL,PROXY
```
* **ALEO PRIVATE** - приватный ключ ALEO
* **TOKEN** - токен гитхаба ([как его создать](https://docs.github.com/en/enterprise-server@3.6/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens))
* **EMAIL** - почта на которую зареган гитхаб
* **PROXY** - если хотите под каждый профиль отдельно сделать прокси, то заполнять это поле


> Формат прокси *ip:port:login:pass*

5) Заполнить файлы *files/first_commit_repo.txt* и *files/repo_names.txt* - из этих файлов будут случайным образом браться имена репозиториев и коммитов для вашего гитхаба, чем больше, тем лучше