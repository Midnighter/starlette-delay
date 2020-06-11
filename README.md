# Measuring Starlette Delay

A minimal [Starlette](https://www.starlette.io/) application running on
[uvicorn](https://www.uvicorn.org/) and benchmarking provided by
[Locust](https://locust.io/).

## Usage

If you want to repeat the experiment, for example, with modified parameters, you
first need to start all services. Locust is configured to run a two minutes
benchmark.

```
docker-compose up
```

After the Locust manager exists, please end the stack (by pressing Ctrl + C).

You can then look at the [Jupyter
notebook](notebooks/response_times_and_delay.ipynb) for inspiration how to
analyze the outcomes.

## Copyright

* Copyright © 2020, Moritz E. Beber.
* Free software licensed under the [GNU Affero General Public License version
  3](LICENSE).
