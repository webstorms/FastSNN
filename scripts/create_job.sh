#!/bin/bash
sbatch <<EOT
#!/bin/sh

# Cluster config
#SBATCH --job-name=fmnist
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=8
#SBATCH --mem=120G
#SBATCH --clusters=htc
#SBATCH --partition=short
#SBATCH --time=11:59:00
#SBATCH --gres=gpu:1 --constraint='gpu_sku:V100'
#SBATCH --qos=standard
#SBATCH --mail-type=ALL
#SBATCH --mail-user=webstorms@gmail.com

module purge
module load Anaconda3/2021.05
module load CUDA/11.2.2-GCC-10.3.0
module load cuDNN/8.2.1.32-CUDA-11.3.1

source activate $DATA/fastsnn

echo $CUDA_VISIBLE_DEVICES
nvidia-smi

# Run job
echo ${@:2}
python -u /data/dpag-auditory-neuroscience/kebl6283/PycharmProjects/FastSNN/scripts/train.py ${@:1}
EOT