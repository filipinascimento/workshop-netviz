# Materials for "An Introduction to Network Visualization" Workshop
### From bare-bones to interactivity
<img width="361" alt="image" src="https://user-images.githubusercontent.com/600989/157375971-ff0d0bb4-7e63-473c-a6ae-c5488702007b.png">
This repository will hold most of the links and materials to be used in the hands-on session of the IUNI Workshop : An Introduction to Network Visualization. 

See https://iuni.iu.edu/news/event/79 for more info.

Binder environment can be accessed via: 
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/filipinascimento/workshop-netviz/HEAD)

### Hands-on links and materials

The hands-on session is separated into three parts:
1. [Standalone network visualization tools](#standalone-tools)
2. [Python libraries to handle and visualize networks](#python-libraries-to-handle-and-visualize-networks)
3. [Interactive network visualization for the web](#interactive-network-visualization-for-the-web)

Except for part 1, some programming skills and knowledge on the involved technologies (Python for part 2 and Javascript/HTML for part 3) are recommended for anyone following and reproducing the hands-on tutorials.

**The tutorial files will be uploaded a few hours before the workshop**

## Standalone tools
This session will cover some of the most used network visualization tools out there.
We recommend the attendants pre-download and install these apps if they are available to their platforms.

 - [Cytoscape](http://cytoscape.org)
 - [Gephi](https://gephi.github.io)
 - [Graphia](https://graphia.app)

Please, follow the installation instructions on the website of each tool.

## Python libraries to handle and visualize networks
To follow this part of the presentation, we recommend the attendent to download this repository to their machines and prepare a python environment containing some packages related to network analysis and visualization.

Binder may be recommended for a simple setup. Just click on the badge [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/filipinascimento/workshop-netviz/HEAD) and a web environment will open for you. If you use binder, you can skip most of the setup.

### Downloading this repository from git

#### **Using the web interface:**
To download this repository using the github web interface, open this repository in a web browser and click on button *Code* and then *Download ZIP*

<img width="262" alt="image" src="https://user-images.githubusercontent.com/600989/157391726-ac52c790-ee14-4f76-b4af-4ce6ba79c10c.png">

uncompress the file and move it to a directory with read/write permissions (like your user folder)

#### **Using git command line:**
Alternatively, you can use git to download this repository. First, make sure *git* is installed by running `git` command line in the shell or DOS/power-shell prompt. You can follow the [instalation instructions](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) in case git failed to run.

With git installed, run the command:

```bash
git clone https://github.com/filipinascimento/workshop-netviz.git
```

It should create a folder named `workshop-netviz` on the current directory.


### **Preparing the Python environment**
For this tutorial, we recommend the usage of python 3.8.x. Also, we recommend the participants to have a separated environment to run the code. [**Miniconda**](https://docs.conda.io/en/latest/miniconda.html) can be used to both download the correct python version and prepare an environment. Instructions on how to download miniconda (or conda) can be found in https://docs.conda.io/en/latest/miniconda.html.

After conda is installed, run from a conda-ready environment:

```bash
conda create --name=networkviz python=3.8 ipython
```
This will install python and ipython (which can be super useful to debug or test python code). 
If you prefer to use your own python environment, make sure it is version 3.8.x. Note: Some FURY-based demos may not run on Python version 3.9 or higher.

---
**NOTE FOR APPLE SILICON MACS**:
If you are running this on an Apple Silicon Mac (e.g., M1, M1 Pro, M1 Max), some demos may not run. In that case, we recommend using the rosetta 2 x86-64 environment, which can be accomplished by running this instead:

```bash
# Only for Apple Silicon macs
CONDA_SUBDIR=osx-64 conda create --name=networkviz python=3.8 ipython
```
---

Finally, the conda environment can be activated using the following command:
```bash
conda activate networkviz
```

Your python environment is ready! Now we should install a few dependencies


### **Installing dependencies**
Now that the python environment is working, we need to install a few dependencies. This includes a collection of packages to handle networks, visualization libraries, auxiliary utilities, etc.

To install the packages, let's use `pip` and the pre-compiled list of dependencies from file `requirements-basic.txt` in this repository.

#### basic requirements
First let's install the basic dependencies:
```bash
pip install -r requirements-basic.txt
```

This will install the following packages:
```
jupyterlab
numpy
tqdm
python-igraph
networkx
xnetwork
pandas
matplotlib
ipympl
ipywidgets
leidenalg
infomap
wordcloud
pillow
six
```

#### FURY requirements
To install the dependencies to run [FURY](http://fury.gl)-based demos, please install fury using the following command:
```bash
pip install -r requirements-fury.txt
```
This will install FURY and other required packages to run the demos:
```
fury
geographiclib
splines
```
note that FURY-based demos require a GPU, thus they may or may not work on servers or over binder.

#### node2vec requirements
For the node2vec (neural network embedding) demo, install the required packages using this command:
```bash
pip install -r requirements-node2vec.txt
```
Unfortunately, this only works on macOS or Linux systems. The installed packages are:
```
gensim
cxrandomwalk
numba
umap-learn
```

#### Graph-tool (Stochastic block model and some viz algorithms) requirements
The package graph-tool can only be installed easily from conda on Linux and MacOS. Windows is unsupported. To install, use the following conda command:
```bash
conda install -c conda-forge graph-tool
```
For alternative ways to install graph-tool check its website: https://graph-tool.skewed.de


#### Edge bundling demos requirements
Edge bundling in python can be accomplished by using the datashader package, which can be heavy for some environments. To install it use:
```bash
pip install -r requirements-edgebundling.txt
```
The installed packages are:
```
datashader 
```

#### Edge bundling demos requirements
If you like to try installing all the requirements at the same time use the following line: 
```bash
pip install -r requirements.txt
```
Note that this may fail because one or more packages can not be installed on certain platforms. Graph-tool will not be installed using pip.



## Interactive network visualization for the web
For the third part of the hands-on demo, a modern web browser (e.g., Chrome, Safari, Edge, Firefox) is the only requirement for most of the demos. If you like to run the Helios-Web server locally, you may also need to install [node.js](https://nodejs.org/en/) and [npm](https://www.npmjs.com).

Installation instructions can be found in:
https://nodejs.org/en/

Alternativally, nodejs can be easily installed from conda by using:
```bash
conda install -c conda-forge "nodejs>=17"
```



## Recommended resources and links
 - [Visual Studio Code](https://code.visualstudio.com) - Versatile editor supporting multiple platforms and languages. This is the preferred code editor for the demos.

(more coming soon)






