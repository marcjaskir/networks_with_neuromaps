#!/usr/bin/env python

import os
from neuromaps import transforms, datasets, images, nulls, resampling
from neuromaps.datasets import fetch_atlas, fetch_annotation, available_annotations
from neuromaps.stats import compare_images
import nibabel as nib
import numpy as np
from scipy.special import comb

#### INPUT ####
n_perms = 1000
###############

# Define path for saving transformed annotations
transformed_outpath = os.path.join('..','outputs','1','annotations_fslr')

# Load all available annotations
all_annotations = fetch_annotation(source='all')

# Transform all available annotations to fsLR 32k
print('Converting available annotations to fsLR 32k...')
all_annotations_fsLR_32k = {}
for annotations in available_annotations():

	# Annotations with source 'hill2010' only includes data for the right hemisphere
	# See related thread: https://github.com/netneurolab/neuromaps/issues/76
	if annotations[0] != 'hill2010':
		
		if annotations[2] == "MNI152":
			all_annotations_fsLR_32k[annotations] = transforms.mni152_to_fslr(all_annotations[annotations],'32k')
		elif annotations[2] == "civet":
			all_annotations_fsLR_32k[annotations] = transforms.civet_to_fslr(all_annotations[annotations],'32k')
		elif annotations[2] == "fsLR":
			all_annotations_fsLR_32k[annotations] = transforms.fslr_to_fslr(all_annotations[annotations],'32k')
		elif annotations[2] == 'fsaverage':
			all_annotations_fsLR_32k[annotations] = transforms.fsaverage_to_fslr(all_annotations[annotations],'32k')

# Extract paths to annotations
imgs = list(all_annotations_fsLR_32k.values())

# Extract keys for annotations
keys = list(all_annotations_fsLR_32k.keys())

# Create array for correlation and p-value matrices
corrs = np.empty([len(all_annotations_fsLR_32k),len(all_annotations_fsLR_32k)])
pvals = np.empty([len(all_annotations_fsLR_32k),len(all_annotations_fsLR_32k)])

# Create list for spatial nulls 
null_annotations = list()

# Set seed
seed = 1234

# Generate spatial nulls for each map
for i in range(len(all_annotations_fsLR_32k)):
	
	print(f'Generating spatial nulls for {keys[i]}...')

	# update seed
	seed = seed + 1

	# Generate spatial nulls
	rotated = nulls.alexander_bloch(imgs[i],atlas='fsLR', density='32k', n_perm=n_perms, seed=seed)
	null_annotations.append(rotated)

# Create array for pairwise spatial null distributions (used for modified z-transformation)
null_distributions = np.empty([comb(len(all_annotations_fsLR_32k),2).astype(int),n_perms+2])

# Compute correlations between annotations and their associated p-values
null_distributions_row = 0
for i in range(len(all_annotations_fsLR_32k)-1):

	print(f'Computing spatial correlations with {keys[i]}...')

	for j in range(i+1,len(all_annotations_fsLR_32k)):

		# Compute correlation + p-value
		corr, pval = compare_images(imgs[i],imgs[j], metric='pearsonr', nulls=null_annotations[i])
		corrs[i,j] = corr
		pvals[i,j] = pval

		# Compute spatial null distribution
		for perms in range(n_perms):

			null_distributions[null_distributions_row,0] = i+1
			null_distributions[null_distributions_row,1] = j+1
			null_distributions[null_distributions_row,perms+2] = compare_images(null_annotations[i][:,perms],imgs[j], metric='pearsonr')

		null_distributions_row = null_distributions_row + 1

# NA lower triangle
corrs[np.arange(corrs.shape[0])[:,None] >= np.arange(corrs.shape[1])] = np.nan
pvals[np.arange(pvals.shape[0])[:,None] >= np.arange(pvals.shape[1])] = np.nan

# Save adjacency matrix, p-value matrix, annotation labels, and null distributions to .csv files
np.savetxt("../outputs/1/fsLR_32k_adjacency_matrix.csv", corrs, delimiter=',',fmt='%f')
np.savetxt("../outputs/1/fsLR_32k_pval_matrix.csv", pvals, delimiter=',',fmt='%f')
np.savetxt("../outputs/1/fsLR_32k_annotation_labels.csv", keys, delimiter='_',fmt='%s')
np.savetxt("../outputs/1/fsLR_32k_null_distributions.csv", null_distributions, delimiter=',',fmt='%f')

# Save transformed annotations
for i in range(len(all_annotations_fsLR_32k)):

	# Extract labels
	label = "_".join(keys[i])

	# Parse hemispheres
	lh, rh = all_annotations_fsLR_32k[keys[i]]

	# Define filenames
	lh_filename = label + '_lh.gii'
	rh_filename = label + '_rh.gii'

	# Save
	nib.save(lh, os.path.join(transformed_outpath,lh_filename))
	nib.save(rh, os.path.join(transformed_outpath,rh_filename))

print('Done!')
