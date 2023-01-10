#!/bin/bash

source activate neuromaps

export PYTHONPATH="${PYTHONPATH}:/Users/mjaskir/software/neuromaps/neuromaps"

# Create output directories
if [ ! -d ../outputs/1 ]; then
	mkdir -p ../outputs/1/annotations_fslr
fi

./1_gen_adjacency_matrix.py
