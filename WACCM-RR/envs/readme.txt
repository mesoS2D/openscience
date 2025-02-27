To activate environment

1. Module load conda
2. (only needs doing once) 

> conda env create --file=environment.yml 

This Creates an environment named "analysis" - change the name in environment.yml to whatever you prefer
3. conda activate analysis
4. Install packages, e.g., conda install jupyter
5. From cli, run > python -m ipykernel install --user --name=analysis ! This turns your conda environment into a python kernel that you can use in a jupyter notebook. All packages installed using 4 become available in the notebook. You may need to refresh your notebook to see the kernel appear.
