#!/bin/bash
cd $1
sed -i 's/OverwritePickle/overwrite_pickle/g' *.ipynb
sed -i 's/RemoveInfiniteRSS/remove_infinite_RSS/g' *.ipynb
sed -i 's/PicklePath/pickle_path/g' *.ipynb
sed -i 's/log1010/log10/g' *.ipynb
sed -i 's/PE_Data_log/pe_data_log/g' *.ipynb
sed -i 's/Truncatemode/truncate_model/g' *.ipynb
sed -i 's/Bins/bins/g' *.ipynb
sed -i 's/Normed/normed/g' *.ipynb
sed -i 's/Color/color/g' *.ipynb
sed -i 's/XRotation/xrotation/g' *.ipynb
sed -i 's/Orientation/orientation/g' *.ipynb
sed -i 's/saveFig/savefig/g' *.ipynb
sed -i 's/ResultsDirectory/results_directory/g' *.ipynb
sed -i 's/ColourMap/colour_map/g' *.ipynb
sed -i 's/FromPickle/from_pickle/g' *.ipynb
sed -i 's/GridSize/grid_size/g' *.ipynb
sed -i 's/Marginals/marginals/g' *.ipynb
sed -i 's/X/x/g' *.ipynb
sed -i 's/CustomTitle/custom_title/g' *.ipynb
sed -i 's/plotPEData/PlotPEData/g' *.ipynb
sed -i 's/modelSelection/ModelSelection/g' *.ipynb

