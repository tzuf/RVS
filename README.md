# RVS: A Novel Dataset for Spatial Compositional Reasoning 

## Data

The data can be found here - https://github.com/tzuf/RVS/tree/main/dataset/.

The data contains four json files corresponding to four split-sets: train (Manhattan), seen-city development (Manhattan), unseen-city development (Pittsburgh) ,and test (Philadelphia).

Each sample contains the following:

* content - navigation instruction.
* rvs_start_point -  the coordinates of the start location.
* rvs_goal_point - the coordinates of the goal location.



# Installation:
## Install conda environment
```
conda env create -f environment.yml
```

## Install BAZEL
```
apt install bazel
```

## BAZEL: Build
```
source build_all.sh
```

## BAZEL: Test
```
source test_all.sh
```

## BAZEL: Run
```
source run_all.sh
```




