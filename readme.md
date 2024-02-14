# CommitBench: A Benchmark for Commit Message Generation

<p align='center'>
  <a href="https://hub.docker.com/repository/docker/maxscha/commitbench/general">
    <img alt="DockerHub" src="https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=whitee">
</a>
<img src='https://img.shields.io/badge/<SUBJECT>-<IDENTIFIER>-b31b1b?logo=arxiv&logoColor=red&style=for-the-badge'>
<a href="https://huggingface.co/datasets/maxscha/commitbench">
  <img src='https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Dataset-blue?style=for-the-badge'>
</a>
<a href="https://zenodo.org/records/10497442">
  <img src='https://img.shields.io/badge/Zenodo-005C47?style=for-the-badge&logo=zenodo&logoColor=white'>
</a>
</p>

This repository hosts the replication package for our research paper, titled "CommitBench:  A Benchmark for Commit Message Generation". It includes the necessary code, datasets, and tools to replicate our datasets and further explore the dataset we have compiled and analyzed.

- *Dataset*: Available on [Zenodo](https://zenodo.org/records/10497442) and [Huggingface](https://huggingface.co/datasets/maxscha/commitbench)
- *Docker Environment*: Available on [DockerHub](docker.io/maxscha/commitbench])
- *Pre-Print*: Available on [arXiv](TODO)

## Usage Instructions
### Prerequisites
- Docker: Ensure Docker is installed on your system.

### [Optional] Building the Docker Container
We already provide a build image on dockerhub which is automatically used in console.sh. If you want to build the docker image run
`docker build -t maxscha/commitbench:latest .`


### Starting a Console in the Container
Execute `bash console.sh` to initiate the container and enter an interactive shell environment with the current working directory mounted into `/workspace`.

### Dataset Generation
Run `run_pipeline.sh` to generate both the standard and extended versions of the dataset. It will produce the short version and the long version

### Comment on Replication 
While we try to make everything as replicable as possible, the fact that repositories are changing or deleted makes it challenging to recreate the exact dataset. We provide the underlying scraped data on request.


## Repository Structure

Scripts and resources are organized into specific folders, and they are intended to be executed from the root directory of the project.



### Directory Overview
- **analyze**: Contains code for analyzing various stages of the dataset.
- **enhance**: Includes code for improving the dataset, such as adding more information.
- **filter**: Includes code for filtering the dataset
- **exporter**: Scripts for converting the dataset into formats compatible with different models.
- **importer**: Scripts for importing common dataset formats to standardize the base across different datasets.
- **prepare**: Contains scripts for downloading CodeSearchNet.


# License
The code is licensed under MIT.

# Contact
To contact the authors reach out to "Maximilian.Schall@hpi.de" or open an issue in this repository


# Citation
The official proceedings citation is forthcoming and will be updated once available.

```
Coming soon: BIB-Entry
```