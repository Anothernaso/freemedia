# A list of environment variables for configuring FreeMedia

`FreeMedia` will load a `.env` file from the current working directory if there is one.

- `FREEMEDIA_REDIS_HOST`: The hostname of the machine running the [`Redis`](https://redis.io/) database for `FreeMedia` to use.
  > Default: `localhost`

- `FREEMEDIA_REDIS_PORT`: The port on the machine specified by the `FREEMEDIA_REDIS_HOST` environment variable, that the [`Redis`](https://redis.io/) database for `FreeMedia` to use is listening on.
  > Default: `6379`
