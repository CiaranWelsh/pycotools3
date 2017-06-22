#!/bin/bash
cd $1
sed -i 's/GetmodelQuantities/GetModelQuantities/g' *.ipynb
