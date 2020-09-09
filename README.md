# Python 3D Graphics Engine

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

[![Open Source? Yes!](https://badgen.net/badge/Open%20Source%20%3F/Yes%21/blue?icon=github)](https://github.com/Naereen/badges/)

3D graphics engine built entirely in python! Pygame is currently the only library being used only for UI and drawing pixels, since pygame only supports 2D alot of math is involved in projection. All mesh creation, translation, rotation is done by within the graphics3dEngine class. Ideally down the line I would like to create a simple system for UI and drawing pixels to replace pygame.

This project is heavily influenced by javidx9's code for a custom graphics engine in C++! Check out his channel [here](https://www.youtube.com/channel/UC-yuWVUplUJZvieEligKBkA)

# New Features!

  - Faces and normals
  - VERY simple Illumination
  - Wireframe mode
  - Custom meshes from .obj files

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

 - Movable camera
 - Optimize graphicsEngine3d.py

## License
[MIT](https://choosealicense.com/licenses/mit/)
