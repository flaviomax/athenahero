# AthenaHero
AthenaHero is a lightweight Flask application for monitoring and mantaining your AWS Athena usage.

![](athenahero-home.jpg?raw=true "AthenaHero Home")

AthenaHero is heavily inspired by [PGHero, a performance dashboard for Postgres](https://github.com/ankane/pghero).

### Installation

AthenaHero is available as a Docker image, and an example setup is present in the `docker-compose.yml` file at the root of this project.

#### To get started immediately:
Before running, you **must** set these three env vars on the host:
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_DEFAULT_REGION`

In case you are using AWS session tokens, you must also set the `AWS_SESSION_TOKEN` var on the host.

And then simply run:

```docker-compose up athenahero```

AthenaHero will be available on `http://localhost:5000` on the host machine.

#### Other options

##### Authentication

AthenaHero supports basic HTTP authentication. Before starting the server, set the env vars:

- `ATHENAHERO_USERNAME`
- `ATHENAHERO_PASSWORD`

And the browser will require authentication.

##### Database

Set the env var `ATHENAHERO_SQLALCHEMY_DATABASE_URI=potsgresql://user:pass@host:5432/db` to your own postgres installation. 

### How it works

AthenaHero polls AWS from time to time and fetches all Athena query metadata for the last 30 days. 
The IAM credentials setup using env vars must have permissions for `listing` and `reading` Athena query history data. 

**Athenahero does not use any API calls that cost you money**, and using Athenahero should not impact your AWS Billing (except by _reducing_ it by giving you valuable insight! :) ).

 <br>

### Known Issues

- In the current AthenaHero version, _Cost_ is just measured as **5.00 USD for TB** read, **independent of which AWS Region** AthenaHero is querying. This pricing heuristic **is only valid for some regions**, such as `us-east-1` and `us-west-2`. This will be fixed on a future version.  
