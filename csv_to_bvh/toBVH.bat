cd rawCSV
python run_main.py

cd ../main
bash generateCSV.sh "pp.txt" "../processedCSV/"

cd ../processedCSV
python run_main.py