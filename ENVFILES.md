# Env configurations

The **.env** configurations files for the project are located in the .env.example. Following explanainsion will help you to configure project.

# Application Settings
```
LOGURU_LEVEL - Debug level
PORT - Expose port from python application
VK_API_TOKEN - vk access token
```
# Databases settings

Next are the settings for accessing the database
## Postgres

```
DATABASE_HOST
DATABASE_PORT
DATABASE_USER
DATABASE_PASSWORD
DATABASE_NAME
```
## Redis
```
REDIS_HOST
REDIS_PORT
REDIS_PASSWORD
REDIS_DB
```

# Containers settings

## Postgres container
The following are the settings for the database
```
POSTGRES_USER - Postgres username
POSTGRES_PASSWORD - Postgres password
POSTGRES_DB - Postgres database
```
## Redis container

**Note**: Redis settings equal reddis accessing [settings](#redis)