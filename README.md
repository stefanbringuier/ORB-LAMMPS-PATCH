# Orbital Materials Pretrained Model LAMMPS Wrapper
[![Build and Run LAMMPS with ML-ORB](https://github.com/stefanbringuier/ORB-LAMMPS-PATCH/actions/workflows/build_and_run.yaml/badge.svg)](https://github.com/stefanbringuier/ORB-LAMMPS-PATCH/actions/workflows/build_and_run.yaml)

> ⚠️ This is an early implementation and has not been fully vetted, but it does appear to match ASE MD runs.
> 
This patch is inspired by the approach used in the [AdvancedSoftCorp](https://github.com/advancesoftcorp/lammps) [M3GNet](https://github.com/advancesoftcorp/lammps/tree/based-on-lammps_2Aug2023/src/ML-M3GNET) implementation, but it applies to the [Orbital Materials pretrained models](https://github.com/orbital-materials/orb-models). Essentially, this is a C++ wrapper that calls the Python implementation for the [Orbital Materials pretrained atomic potentials](https://github.com/orbital-materials/orb-models). As a result, a Python driver script must be invoked by LAMMPS, which needs to be compiled with Python support, and the Orbital Materials pretrained potential package must be installed in the Python environment.


## Why
There might not be too much upside in performance (i.e., runs as fast as ASE MD) as this approach is just a wrapper and does not leverage the full parallelization aspects of LAMMPS (i.e., MPI). However, there may be some added functionality in the available `fix` and `compute` commands that are availabe in LAMMPS which are not typically implemented in [ASE](https://wiki.fysik.dtu.dk/ase). For this reason there will be scenarios where it will be useful to test and benchmark the Orbital Materials pretrained models similar to how some are doing for M3GNet or CHGNet.

## How to install
1. Setup a python virtual environment and activate:
   - `python -venv orb-models`
   - `source orb-models/bin/activate`
2. Install the [Orbital Materials pretrained atomic potentials](https://github.com/orbital-materials/orb-models)
3. Download [LAMMPS](https://lammps.org).
4. Clone this repo.
5. Run the `patch.sh` script and provide path to the cloned LAMMPS folder.
6. Compile LAMMPS with at minimum (you can add more) the following: `cmake -D BUILD_MPI=OFf -D BUILD_OMP=ON -D PKG_OMP=ON -D PKG_PYTHON=ON -D PKG_ML-ORB=ON ../cmake`
   > NOTE: You can compile with MPI but it will not work for this `pair_style`, in other words you can only use a single MPI task.
7. Copy the [orb_driver.py](patch/orb_driver.py) script to the folder with your LAMMPS input script or provide the full path to it in your input script.

## How to use

In your LAMMPS script you need to use the following syntax:

```
pair_style orb </path/to/orb_driver.py> <gpu>
pair_coeff * * orb-v1 <species-symbol-1> <species-symbol-2> ...
```

The species should be the atomic symbol and ordered such that they follow LAMMPS type id sequence. If you provide the keyword `gpu` it should try to run on the GPU if one is available, otherwise the inference will be done on the CPU. The path to the `orb_driver.py` file is needed. You can copy this from either the [patch](patch) or the [example](example) folders. You do not need to modify `orb_driver.py` unless you are need custimization of finding the GPU flag isn't being passed properly.


### Model options

- `orb-v1` - trained on [MPTraj](https://figshare.com/articles/dataset/Materials_Project_Trjectory_MPtrj_Dataset/23713842?file=41619375) + [Alexandria](https://alexandria.icams.rub.de/).
- `orb-mptraj-only-v1` - trained on the MPTraj dataset only to reproduce our second Matbench Discovery result. We do not recommend using this model for general use.
- `orb-d3-v1` - trained on MPTraj + Alexandria with integrated D3 corrections. In general, we recommend using this model, particularly for systems where dispersion interactions are important. This model was trained to predict D3-corrected targets and hence is the same speed as `orb-v1`. Incorporating D3 into the model like this is substantially faster than using analytical D3 corrections.
- `orb-d3-sm-v1` or `orb-d3-sm-v1` - Smaller versions of `orb-d3-v1`. The `sm` model has 10 layers, whilst the `xs` model has 5 layers.

## Contributing 
Feel free to create a pull request if you find some bugs or want to suggest improvements. One potential change is to move away from a python driver script and just have C++ code that instantiates and calls the python objects and methods that are in the driver script. 

## Acknowledgements
Thanks to the team at [AdvancedSoftCorp](https://www.advancesoft.jp/) for providing a framework for leveraging the [ASE Calculators Class](https://wiki.fysik.dtu.dk/ase/ase/calculators/calculators.html#calculators). Also appreciate the team at Orbitals Materials making their pretrained models available for testing.
