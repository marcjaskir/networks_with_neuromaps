# Project Title
Networks with neuromaps

# Brief project description
neuromaps also provides access to a growing repository of reference brain maps from a diverse set of publications. The integration of these datasets with neuromaps’ functionality affords the opportunity to explore multi-modal relationships between existing brain maps and to generate or test hypotheses with new brain maps. By creating a network representation of the correlation structure between all available reference maps included with neuromaps (n=70) and partitioning the networks into communities, I proposed a framework by which new data can be contextualized within a large literature by its spatial correspondence with community spatial averages. This approach can boost statistical power by obviating unnecessary statistical comparisons.

# Project Lead
Marc Jaskir

# Faculty Lead
Aaron Alexander-Bloch

# Dependencies
Install Connectome Workbench (https://www.humanconnectome.org/software/get-connectome-workbench)
Install Miniconda (https://docs.conda.io/en/latest/miniconda.html), creating and activating an environment called "neuromaps"
Install pip
- conda install pip
Install neuromaps (Complete instructions here: https://netneurolab.github.io/neuromaps/)
- git clone https://github.com/netneurolab/neuromaps
- cd neuromaps
- pip install .
Add neuromaps installation to Python path
- export PYTHONPATH="${PYTHONPATH}:/path/to/neuromaps"

# Usage
Start by running 1_gen_adjacency_matrix.sh, which calls the associated Python script.
Then, R Markdown files can be executed in sequence. Rendered .html files are included for reference.
