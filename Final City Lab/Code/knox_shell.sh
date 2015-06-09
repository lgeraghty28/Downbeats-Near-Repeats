#Shell script to get final results

python knox_by_unit.py
python centroid_areas__rings.py > events.csv
python collapse_events.py > events.collapse.csv
python merge_knox_and_history.py > coefficients.csv
python knox_sums_2.py
