# AthenaHero
AthenaHero is a lightweight Flask application for monitoring and mantaining your AWS Athena usage.

![](athenahero-home.jpg?raw=true "AthenaHero Home")

AthenaHero is heavily inspired by [PGHero, a performance dashboard for Postgres](https://github.com/ankane/pghero).

### Installation

AthenaHero is available as a Docker image, and can be run using the `docker-compose.yml` at the root of this project.
Before running, you **must** set these three env vars on the host:
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_DEFAULT_REGION`

And then simply run:

```docker-compose up athenahero```

AthenaHero will be available on `http://localhost:5000` on the host machine.

#### Other options

Set the env var `ATHENAHERO_SQLALCHEMY_DATABASE_URI=potsgresql://user:pass@host:5432/db` to your own postgres installation. 

### How it works
AthenaHero polls AWS from time to time and fetches all query data for the last 30 days. 

### Known Issues

- In the current AthenHero version, _Cost_ is just measured as **5.00 USD for TB** read, **independent of which AWS Region** AthenaHero is querying. This pricing heuristic **is only valid for some regions**, such as `us-east-1` and `us-west-2`. This will be fixed on a future version.  
