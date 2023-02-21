# Copyright [2023] [jhj0517]

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import cv2
import dlib
import numpy as np
from PIL import Image

def parse(input_path,output_path):
    if not input_path or not output_path:
        raise ValueError("Please enter valid input and output paths")

    predictor = dlib.shape_predictor("model\shape_predictor_68_face_landmarks.dat")

    img = cv2.imread(input_path)

    faces = dlib.get_frontal_face_detector()(img)

    for p,face in enumerate(faces):
        landmarks = predictor(img, face)

        # Extract the facial features
        right_eyebrow_pts = [landmarks.part(i) for i in range(17, 22)]
        left_eyebrow_pts = [landmarks.part(i) for i in range(22, 26)]
        nose_pts = [landmarks.part(i) for i in range(27, 36)]
        right_eye_pts = [landmarks.part(i) for i in range(36, 42)]
        left_eye_pts = [landmarks.part(i) for i in range(42, 48)]
        mouth_pts = [landmarks.part(i) for i in range(48, 68)]

        # Create an array of facial feature masks
        masks = []
        for feature_pts in [right_eyebrow_pts, left_eyebrow_pts, nose_pts,right_eye_pts, left_eye_pts, mouth_pts]:
            feature_pts = [(pt.x, pt.y) for pt in feature_pts]
            feature_pts = np.array(feature_pts, ndmin=2).astype(np.int32)
            mask = np.zeros((img.shape[0], img.shape[1]), np.uint8)
            cv2.fillPoly(mask, [feature_pts], 255)
            masks.append(mask)

        #Get the excluded face part
        hull = cv2.convexHull(np.array([(pt.x, pt.y) for pt in landmarks.parts()]))
        face_mask = np.zeros((img.shape[0], img.shape[1]), np.uint8)
        cv2.fillConvexPoly(face_mask, hull, (255, 255, 255))
        face_only = cv2.bitwise_and(img, img, mask=face_mask)
        excluded_face = cv2.bitwise_and(face_only, img, mask=cv2.bitwise_not(sum(masks)))
        excluded_face = cv2.cvtColor(excluded_face, cv2.COLOR_BGR2BGRA)
        rows, cols, _ = excluded_face.shape
        for i in range(rows):
            for j in range(cols):
                if excluded_face[i, j, 0] == 0 and excluded_face[i, j, 1] == 0 and excluded_face[i, j, 2] == 0:
                    excluded_face[i, j, 3] = 0
        cv2.imwrite(f"{output_path}/{p}_Excluded Face.png", excluded_face)

        #Get the background part
        combined_masks = np.zeros((img.shape[0], img.shape[1]), np.uint8)
        for mask in masks:
            combined_masks = cv2.bitwise_or(combined_masks, mask)
        combined_masks = cv2.bitwise_or(combined_masks,face_mask)
        background_mask = cv2.bitwise_not(combined_masks)
        background_part = cv2.bitwise_and(img, img, mask=background_mask)
        background_part = cv2.cvtColor(background_part, cv2.COLOR_BGR2BGRA)
        background_part[background_mask == 0] = [0, 0, 0, 0]
        cv2.imwrite(f"{output_path}/{p}_Background.png", background_part)

        # Extract each facial feature from the input image
        features = []
        for i, mask in enumerate(masks):
            mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
            feature = cv2.bitwise_and(img, mask)
            features.append(feature)

        # Save each extracted facial feature to an output image
        feature_names = ['Right Eyebrow', 'Left Eyebrow', 'Nose', 'Right Eye', 'Left Eye', 'Mouth']
        for i, feature in enumerate(features):
            feature = cv2.cvtColor(feature, cv2.COLOR_BGR2BGRA)
            rows, cols, _ = feature.shape
            for i_ in range(rows):
                for j in range(cols):
                    if feature[i_, j, 0] == 0 and feature[i_, j, 1] == 0 and feature[i_, j, 2] == 0:
                        feature[i_, j, 3] = 0
            cv2.imwrite(f"{output_path}/{p}_{feature_names[i]}.png", feature)

        # Save the .tif file
        layer_names = ['Background', 'Excluded Face'] + feature_names
        images = [Image.open(f"{output_path}/{p}_{layer_names[i]}.png").convert("RGBA") for i in range(len(layer_names))]
        images[0].save(f"{output_path}/{p}_Layers.tif", save_all=True, append_images=images[1:])


