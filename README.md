# SlidingWindowFilter-experiment

[![Software License][ico-license]](LICENSE.md)
[![Build Status][ico-travis]][link-travis]

A small python application that is part of the [final paper](https://github.com/GordonLesti/SlidingWindowFilter)  of my
bachelor degree.

## Requirements

* [python](https://www.python.org/) 2
* [dvdhrm/xwiimote](https://github.com/dvdhrm/xwiimote)
* [dvdhrm/xwiimote-bindings](https://github.com/dvdhrm/xwiimote-bindings)
* A Wii Remote controller

## Run

Please run the following command as root. The application will write the result of the experiment into the `data`
directory.
```bash
 python -m src.xwiimote_recorder
```

## Test

Here the commands for [pylint](https://www.pylint.org/) and the unittests.
```bash
 pylint src/ test/
 python -m unittest test.test_experiment
```

## License

The MIT License (MIT). Please see [License File](LICENSE.md) for more information.

[ico-license]: https://img.shields.io/github/license/GordonLesti/SlidingWindowFilter-experiment.svg?style=flat-square
[ico-travis]: https://img.shields.io/travis/GordonLesti/SlidingWindowFilter-experiment/master.svg?style=flat-square

[link-travis]: https://travis-ci.org/GordonLesti/SlidingWindowFilter-experiment
