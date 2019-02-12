#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""feature detection."""

import cv2
import os
import sys

#ターゲットの画像のファイルのパスを取得
IMG_TARGET = os.path.abspath(os.path.dirname(__file__)) + '/target/'
target_files = os.listdir(IMG_TARGET)
if target_files[0] == '.DS_Store':
	del(target_files[0])

#比較させる画像達のファイルのパスを取得
IMG_DIR = os.path.abspath(os.path.dirname(__file__)) + '/images/'
sub_dirs = os.listdir(IMG_DIR)
if sub_dirs[0] == '.DS_Store':
	del(sub_dirs[0])

IMG_SIZE = (200, 200)
i=0

target_img_path = IMG_TARGET + str(target_files[0])
target_img = cv2.imread(target_img_path, cv2.IMREAD_GRAYSCALE)
target_img = cv2.resize(target_img, IMG_SIZE)

bf = cv2.BFMatcher(cv2.NORM_HAMMING)
# 特徴点算出のアルゴリズムを決定
detector = cv2.AKAZE_create()
(target_kp, target_des) = detector.detectAndCompute(target_img, None)

#ターゲットのファイルの名前を出力
print('TARGET_FILE: %s' % (target_files))

#ターゲットの画像と比較させる画像達を比較し類似度を出す
for classId in sub_dirs:
	sub_dir_path = IMG_DIR + '/' + classId
	img_files = os.listdir(sub_dir_path)

	for file in img_files:
		if file == '.DS_Store':
			continue

		comparing_img_path = IMG_DIR + classId + '/'+ file
		try:
			comparing_img = cv2.imread(comparing_img_path, cv2.IMREAD_GRAYSCALE)
			comparing_img = cv2.resize(comparing_img, IMG_SIZE)
			(comparing_kp, comparing_des) = detector.detectAndCompute(comparing_img, None)
			#画像同士をマッチング
			matches = bf.match(target_des, comparing_des)
			dist = [m.distance for m in matches]
			#類似度を計算する
			ret = sum(dist) / len(dist)
		except cv2.error:
			ret = 100000

		if i == 0:
			result = ret
			i = i+1
		else:
			if ret < result:
				result = ret
				result_file =file
				judge = classId
			i = i+1
#結果の出力
print(result)
print(result_file)
if judge == 'dog':
	print("これは犬です")
else :
	print("これは猫です")
