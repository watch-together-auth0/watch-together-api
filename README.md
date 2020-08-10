# watch-together-api

This repo contains the API for the watch together application. This is deployed on [deta.sh]()

This API offers 2 resources: users and channels.

## Users

Schema:

```
{
  "id": "<userId>"
  "name": "<str>",
  "email": "<email>"
}
```

Users are provisioned on login after being redirected back from the auth0 login module.
The users api has 3 endpoints 

### GET /users
This endpoint lists all users in the database, it has an optional query param `email` where the a user with a certain email can be fetched.

### GET /users/:id
This endpoint fetches a user by their id.

### POST /users
Creates a user in the databse and accepts this payload:

```
{
  "name": "<str>",
  "email": "<str>"
}
```

## Channels
Channels can be created by users and has this schema: 

```
{
  "id": "<id>"
  "name": "<str>",
  "owner_id": "<userId>",
  "members": [],
  "video": {}
}
```

The channels api has 3 endpoints

### GET /channels
Lists all channels in the database with the optional query param `ownerId`. This will list all channels belonging to a user.

### PATCH /channels/:id
Used to update the channel with the current video playing in the form of a JSON object. Accepts payloads in this format:

```
{
  "video": {}
}
```

### PATCH /channels/:id/add 
Adds a user to a channel, does so by adding them to the members array.
Payload:

```
{
  "userId": "<userId>"
}
```

### POST /channels
Creates a channel. Payload:

```
{
  "name": "<str>",
  "ownerId": "<userId>"
}
```

## Local Development:

```
clone the repo
pip install -r requirements.txt
export FLASK_APP=main.py
export FLASK_ENV=development
flask run
```

