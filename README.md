<div align="center">
  
<h1>Shiinobi</h1>
<p>A Python CLI tool for extracting and retrieving data from various platforms, <br> including anime and manga.</p>

![PyPI - Downloads](https://img.shields.io/pypi/dm/Shiinobi?style=flat-square&color=%23B8B8C4)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/Shiinobi?style=flat-square&color=%23B8B8C4)
![GitHub License](https://img.shields.io/github/license/baseplate-admin/Shiinobi?style=flat-square&color=%23B8B8C4)

<!-- <img src="https://github.com/user-attachments/assets/3af4e30b-901c-46d7-b7de-077b14204392" style="width: 500px; height: auto;"> -->
<img src="./assets/shiinobi.png" style="width: 500px; height: auto;">

<br>
<br>

![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/baseplate-admin/Shiinobi/CI.yaml?style=for-the-badge&color=%23B8B8C4)
![Read the Docs](https://img.shields.io/readthedocs/shiinobi?style=for-the-badge&color=%23B8B8C4)

</div>

## API Documentation

The API documentation for Shiinobi is available [here](https://shiinobi.readthedocs.io/).

## Installation

1. Clone the repository and navigate into dir:

```bash
git clone https://github.com/baseplate-admin/Shiinobi.git
cd Shiinobi
```

2. Install dependencies:

```bash
poetry install
```

3. Build the CLI tool:

```bash
poetry run poe build-cli
```

## Usage

For a list of available commands, use:

```bash
poetry run poe dev-cli --help
# python ./src/shiinobi/cli.py --help
```

Run the CLI tool with:

```bash
poetry run poe dev-cli <command>
# python ./src/shiinobi/cli.py <command>
```

## Executable Binaries

Pre-built executable binaries are available for Windows, Linux, and macOS in the [releases](https://github.com/baseplate-admin/Shiinobi/releases) section.

## Used by

Shiinobi is primarily used within the [CoreSeeder](https://github.com/coreproject-moe/CoreProject/tree/master/seeder) project.

## Contributing

-   If you have a suggestion/idea that would make this project better, please create a pull request. All pull requests will be reviewed by us, and adjusted.
    You can also open a [new issue](https://github.com/baseplate-admin/Shiinobi/issues/new) or help us with an [existing one](https://github.com/baseplate-admin/Shiinobi/issues/).

-   Other than that, you can also help the project by giving it a star ⭐ Your help is extremely appreciated :)

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/baseplate-admin/Shiinobi/blob/master/LICENSE) file for details.
