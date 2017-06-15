==========
gdxcompare
==========




1 Purpose
---------

Tool to compare symbols in GAMS Data eXchange (GDX) files with time series data (specifically integer indexed data).

2 Usage
-------

After installing the module, just call

::

    python -m gdxcompare [options] gdx1 gdx2 ...

An HTML page will open up, showing something similar to `this screenshot <https://github.com/jackjackk/gdxcompare/blob/master/other/gdxcompare-screenshot.png>`_.

- Symbols (variables, parameters) are listed on the left and are selected by left clicking.

- Set dependencies and corresponding elements are listed in adjacent columns. Set elements are selected via mouse hovering.

- The color of the cells indicate the relative variance across elements in a set, so that blue elements will exhibit smaller differences across GDXs than red elements.

- The time series of the queried data is shown on the right. A title reports the description of the selected symbol and the last element selected. The time axis is identified as the first set with integer elements.

- Zooming is supported via horizontal or vertical mouse dragging. Mouse hovering provides details on the top right corner.

3 Requirements
--------------

- Python (tested with Python 3.6).

- up-to-date `numpy <http://www.numpy.org/%E2%80%8E>`_ module.

- up-to-date `gdxpy <https://github.com/jackjackk/gdxpy>`_ (requires manual installation from github).

4 Options
---------

Options

.. table::

    +----------------------+----------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | Short version        | Long version               | Description                                                                                                                                                                                                                   |
    +======================+============================+===============================================================================================================================================================================================================================+
    | ``-h``               | ``--help``                 | Show this options list and exit                                                                                                                                                                                               |
    +----------------------+----------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | ``-m XMAX``          | ``--xmax=XMAX``            | Max value for x-axis [0 = no max, default]                                                                                                                                                                                    |
    +----------------------+----------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | ``-f XMIN``          | ``--xmin=XMIN``            | Min value for x-axis [0 = no min, default]                                                                                                                                                                                    |
    +----------------------+----------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | ``-r RENAME_STRING`` | ``--rename=RENAME_STRING`` | Comma-separated list of new names to give to GDXs (no spaces)                                                                                                                                                                 |
    +----------------------+----------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | ``-s SYMB_REGEX``    | ``--symb=SYMB_REGEX``      | Regex for filtering symbols, or lambda starting with ``@`` (e.g. ``@len(x)<5`` for all symbol names shorter than 5 characters)                                                                                                |
    +----------------------+----------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | ``-p PROF``          | ``--profile=PROF``         | Profile name, used if no ``SYMB_REGEX`` specified, associated to a predefined combination of regex for filtering symbols (see `here <https://github.com/jackjackk/gdxcompare/tree/master/gdxcompare/profiles>`_ for examples) |
    +----------------------+----------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | ``-x LAMBDA_EXPR``   | ``--xlambda=LAMBDA_EXPR``  | Lambda function applied to each element of the x-axis                                                                                                                                                                         |
    +----------------------+----------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | ``-d``               | ``--disaggsymb``           | Flag to disaggregate large symbols across elements of the first domain                                                                                                                                                        |
    +----------------------+----------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

For example:

::

    python -m gdxcompare -sQ -rbau,ref -m20 results_bau.gdx results_ref.gdx

will compare symbols starting with ``Q`` of the two GDX files ``results_bau.gdx`` and ``results_ref.gdx`` in the current path, labelling them as ``bau`` and ``ref``, and showing results up to period 20.

5 License
---------

The MIT License (MIT)

Copyright (c) 2012-2017 Giacomo Marangoni

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
