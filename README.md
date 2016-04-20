# Deployment-tools

Example for deployment by Fabric. Expects to have jenkins user on web01 host with sudo and ssh key auth. 

Usage: #fab --list - list all function for deploy 
Usage: #fab uptime - Shows remote server web01 uptime

For first init process let's run install
Usage: #fab install - which generates such tree

deploy
|-- current -> /var/www/deploy/versions/1461160110/
|-- releases
|   `-- 2.0.4
|       |-- app
|       |-- bin
|       |-- dev
|       |-- lib
|       |-- phpserver
|       |-- pub
|       |-- setup
|       |-- var
|       `-- vendor
|-- shared
|   |-- env
|   |-- media
|   `-- var
`-- versions
    `-- 1461160110
        |-- app
        |-- bin
        |-- dev
        |-- lib
        |-- media -> ../../shared/media
        |-- phpserver
        |-- pub
        |-- setup
        |-- var -> ../../shared/var
        `-- vendor

If new version needs to be deployed let's run deploy

Usage: #fab deploy 

deploy
|-- current -> /var/www/deploy/versions/1461160641/
|-- releases
|   `-- 2.0.4
|-- shared
|   |-- env
|   |-- media
|   `-- var
`-- versions
    |-- 1461160110
    `-- 1461160641

 New version added and switched sym link

It's possible to rollback version, by 
Usage: #fab rollback:lastest or fab rollback:<version number>

Example:

deploy
|-- current -> /var/www/deploy/versions/1461160110
|-- releases
|   `-- 2.0.4
|-- shared
|   |-- env
|   |-- media
|   `-- var
`-- versions
    |-- 1461160110
    `-- 1461160641

To keep project size in health you could run clean function

Usage: #fab clean:<amount of latest version to leave>

Example: #fab clean:2

[root@web01 www]# tree deploy  -d -L 2
deploy
|-- current -> /var/www/deploy/versions/1461161018/
|-- releases
|   `-- 2.0.4
|-- shared
|   |-- env
|   |-- media
|   `-- var
`-- versions
    |-- 1461161006
    `-- 1461161018

Latest 2 version listed




