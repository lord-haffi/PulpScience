# pulp_science
A Website where people can publish and read articles (or follow projects) about scientifical topics.


### Contributing
If you want to contribute please make sure to not commit directly to the master or development branch.
Instead, create a new branch from development and create a pull request with the development branch.

To clone and contribute to this project please follow these steps:
- Make sure git and git LFS is installed on your machine to clone this repository
- Install tox
- Setup your virtual python environment by running
    ```bash
    tox -e dev
    ./.tox/dev/Scripts/activate
    ```
- Configure python interpreter of your IDE to `.tox/dev/Scripts/python.exe`

And that's it!
