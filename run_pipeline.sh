#!/bin/sh

set -e

# Downloads CodeSearchNet Dataset and creates the repository list. We already include the repository_list in the 
# python3 prepare/download_dataset.py resources/data
# python3 create/get_repo_list.py

# Download the repositories and convertes them into json-files
python3 create/download_repos.py
python3 create/dataset_from_repo.py -r resources/repos -o resources/results

# Enhance the dataset
python3 ./enhancer/enhance.py \
    -i resources/results \
    -o resources/results_enhanced


# # Filter the unwanted commits
python3 ./filter/filter_p.py \
    -i resources/results_enhanced \
    -o resources/results_enhanced_filtered \
    --m_max 128 \
    --m_min 8 \
    --d_max 511 \
    --language_msg \
    --binary \
    --bot \
    --revert \
    --trivial \
    --language_diff

# And for the long version
python3 ./filter/filter_p.py \
    -i resources/results_enhanced \
    -o resources/results_enhanced_filtered_long \
    --m_max 128 \
    --m_min 8 \
    --d_max 2047 \
    --language_msg \
    --binary \
    --bot \
    --revert \
    --trivial \
    --language_diff
    

# # Create CSV with SPLITS for it
python3 ./exporter/to_csv_split.py -i resources/results_enhanced_filtered -o resources/results.csv
python3 ./exporter/to_csv_split.py -i resources/results_enhanced_filtered_long -o resources/results_long.csv

# Remove names for privacy reason
python3 ./enhancer/enhance_name.py -i resources/results.csv -o resources/commitbench.csv
python3 ./enhancer/enhance_name.py -i resources/results_long.csv -o resources/commitbench_long.csv