# Python 3D Graphics Engine

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

3D graphics engine built entirely in python! Pygame is currently the only library being used only for UI and drawing pixels, since pygame only supports 2D alot of math is involved in projection. All mesh creation, translation, rotation is done by me. Ideally down the line I would like to create a simple system for UI and drawing pixels to replace pygame.

This project is heavily influenced by javidx9's code for a custom graphics engine in C++! Check out his channel [here](https://www.youtube.com/channel/UC-yuWVUplUJZvieEligKBkA)

# New Features!

  - Faces and normals
  - VERY simple Illumination
  - Wireframe mode

### Installation

Python 3D Graphics Engine requires Pygame to run.

Install the dependencies

```sh
$ pip install pygame
```
## Usage

```bash
$ python main.py
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
## Todos

 - Able to import .obj files
 - Optimize graphicsEngine3d.py

## License
[MIT](https://choosealicense.com/licenses/mit/)
