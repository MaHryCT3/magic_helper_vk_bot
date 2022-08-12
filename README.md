# @MagicHelper (VK-Bot)

This VK bot for helps moderators on [Magic Rust](https://vk.com/magicowrust) 


## Abilitys
* Count checks 
> That's not all. Application is developing
# Requirements
## Production
* Debian/Ubuntu
* [Docker](https://docs.docker.com/engine/install/)
* [Docker compose](https://docs.docker.com/compose/install/)
* Nginx
## Development
* [Docker](https://docs.docker.com/engine/install/)
* [Docker compose](https://docs.docker.com/compose/install/)
* [Poetry](https://python-poetry.org/)
* [Python ^3.10](https://www.python.org/downloads/)
* Good mood
## Prepare 
Clone the repository

```bash
$ git clone https://github.com/MaHryCT3/magic_helper_vk_bot.git
```
Configure **.env.example** and save as **.env**. Detailed information about .env configurations provided in [ENVFILES.md](https://github.com/MaHryCT3/magic_helper_vk_bot/blob/master/ENVFILES.md)

## Deploy

**Note**: If you don't have the `make`, copy the commands from Makefile

```bash
$ make build
```
