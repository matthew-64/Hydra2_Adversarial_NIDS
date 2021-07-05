# Basic info
- Title: End-to-End Deep Learning for Person Search
- Author: Tong Xiao, Shuang Li, Bochao Wang, Liang Lin and Xiaogang Wang
- Affiliation: The Chinese University of Hong Kong, and Sun Yat-Sen University
- Publication status: arXiv:1604.01850v1
- Short name: E2EPersonSearch

# Score
- Idea: 3
- Usability: 4
- Presentation: 4
- Overall: 4

# Contributions
## Problem addressed / Motivation
- real-world scenarios where the annotations of pedestrian bounding boxes are unavailable and the target person needs to be found from whole images

## Idea / Observation / Contribution
- Investigate how to localize and match query persons from the scene images without relying on the annotations of candidate boxes
- Propose an end-to-end deep learning framework to jointly handle both tasks
- A large-scale and scene-diversified person search dataset, which contains 18,184 images, 8,432 persons, and 99,809 annotated bounding boxes.
- Joint optimization brings multiple benefits ... We share a fully convolutional neural network to extract features for detecting pedestrians and producing discriminative re-id features.

## Formulation / Solver / Implementation
- Utilize VGG16 model for convolutional layers (conv1 and conv5) in FCN.
- Follow faster rcnn for the pedestrian proposal network
- From pedestrian proposals, we apply three fully connection layers (fc6-8) to generate final feature for person re-id

## Useful info / tips
- If the softmax target is very sparse and the minibatch contains only a few label classes, the gradients would be biased on these classes at each SGD iteration
- It is observed that detectors greatly affect the person search performance of baseline method and there is still a big gap between using the ground truth bounding boxes and the automatically detected ones.

# Evaluation
## Dataset
- Own dataset (E2E Person Search)
- There are two parts in the dataset: street snaps and movies.
- Low-resolution subset and occlusion subset

## Metrics
- designed different evaluation protocols by setting the gallery size to 50, 100, 500, 1, 000, 2, 000, and 4, 000
- meanAveraged Precision (mAP): A candidate window is considered as positive if its overlap with the ground truth is larger than 0.5
- top-k matching rate on bounding boxes: A matching is counted if a bounding box among the top-k predicted boxes overlaps with the ground truth larger than the threshold

## Results
- Baseline detector: ACF + Deep detector
- Baseline re-id methods: BoW with cosine distance, DenseSift+ColorHist with Euclidean and KISSME distance metric, IDNet

# Resource
## Project page
http://www.ee.cuhk.edu.hk/~xgwang/PS/dataset.html

## Source code
https://github.com/ShuangLI59/person_search

## Dataset
Need to send request
https://drive.google.com/open?id=0B-GOvBat1maOVUE3WmNNUVRGamc

## Other paper reading notes

## Others

# Questions
- How to perform re-id algorithm in current framework?

# Build upon
- Performance is low on low-resolution images
- Extend to video data (plus tracking)

# Paper connections
- Faster RCNN

