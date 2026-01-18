# fbd_plotting
FBD Plotting tool

## How to work on this package

1. Git clone it
2. Navigate to the repo and execute `uv sync`; this will create a new virtual environment and install the required dependencies and dev dependencies that I have setup.
3. Optional, if you want to create a Jupyter kernel for it so you can play with it in its own development kernel, execute (from within the repo project root dir): `uv run python -m ipykernel install --user --name fbd_plotting`
4. Open up the example notebook ("creating_a_plot.ipynb") and execute the cells under "How I use it". It should produce a plot.

Once you have completed the above steps, you will effectively have an "editable" installation of this package within its own virtual environment. If you installed the Jupyter kernel (not necessary if you are use VS Code because it will either find the virtual environment on its own or give you an option to specify the Python executable within the virtual environment yourself), then you can make changes to the repo, restart the kernel, and re-execute your plotting code and you should see the changes updated within your notebook.

If you want to use auto-reload so you do not have generally have to restart the kernel every time you want to see a change, execute the following as the first cell on a fresh kernel restart:

```python
%load_ext autoreload
%autoreload 2
```