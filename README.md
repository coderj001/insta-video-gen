# Memeify: Instagram Compilation Generator

Memeify is a Python-based Instagram compilation generator that uses the `moviepy` and `instaloader` libraries to create compilations of Instagram posts and convert them into video format.

## How To Use

Follow these steps to use Memeify:

### 1. Clone This Repository

Clone this repository to your local machine using the following command:

```sh
git clone https://github.com/coderj001/memeify.git
```

### 2. Install Python Packages

Install the required Python packages by running the following command inside the project directory:

```sh
pip install -r requirements.txt
```

### 3. Get Documentation

You can access detailed documentation by running the following command:

```sh
python cli.py --help
```

The documentation will provide you with information on how to use the tool effectively, including available commands, options, and usage examples.

## Features

- Create Instagram post compilations with ease.
- Customize compilation parameters.
- Supports downloading Instagram posts using `instaloader`.
- Converts compilations into video format using `moviepy`.

## Usage Example

Here's an example of how you can use Memeify to create an Instagram compilation:

```sh
python cli.py create-compilation
```

This command will create a compilation of Instagram posts from the specified username and save it as `output.mp4`.

## Contributing

If you'd like to contribute to Memeify, please follow our [contribution guidelines](CONTRIBUTING.md).

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Special thanks to the creators of `moviepy` and `instaloader` for their fantastic libraries.

Happy meme-making!
