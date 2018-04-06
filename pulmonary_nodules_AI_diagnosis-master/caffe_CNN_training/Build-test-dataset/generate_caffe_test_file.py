# -*- coding: utf-8 -*-
# generate_caffe_test_file.py - Removes the header from annotations.csv file in the val directory

import csv
import os
import shutil

############
#
# TIANCHI CSV
TIANCHI_test_path = "/home/ucla/Downloads/Caffe_CNN_Data/csv/test/"
# TIANCHI_test_path = "/home/jenifferwu/IMAGE_MASKS_DATA/csv/test/"
TIANCHI_test_annotations = TIANCHI_test_path + "annotations.csv"
TIANCHI_test_seriesuids = TIANCHI_test_path + "seriesuids.csv"

output_path = "/home/ucla/Downloads/Caffe_CNN_Data/"
# output_path = "/home/jenifferwu/Caffe_CNN_Data"
val_file = "test.txt"

csvRows = []

original_data_path = "/root/code/Data/"
# original_data_path = "/home/jenifferwu/IMAGE_MASKS_DATA/JPEG/Dev/"
val_data_path = "/root/code/Pulmonary_nodules_data/test/"
# val_data_path = "/home/jenifferwu/IMAGE_MASKS_DATA/JPEG/Pulmonary_nodules_data/test/"


#####################
def csv_row(seriesuid, diameter_mm, nodule_class):
    new_row = []
    seriesuid_list = seriesuid.split('/')
    subset, series_uid = seriesuid_list[0], seriesuid_list[1]
    re_series_uid = series_uid.replace("images", "")
    val_dir, image_file, image_path = "", "", ""
    if nodule_class == 0:
        # val_dir = "n01440010/"
        image_file = "PULMONARY_NODULES_test" + re_series_uid + ".jpg"
        image_path = val_dir + image_file
    elif nodule_class == 1:
        # val_dir = "n01440011/"
        image_file = "PULMONARY_NODULES_test" + re_series_uid + ".jpg"
        image_path = val_dir + image_file
    new_row.append(image_path)
    # new_row.append(diameter_mm)
    new_row.append(nodule_class)
    csvRows.append(new_row)

    original_image = original_data_path + subset + "/" + series_uid + ".jpg"
    # print("original_image: %s" % str(original_image))
    tmp_image = val_data_path + val_dir + series_uid + ".jpg"
    val_image = val_data_path + val_dir + image_file

    shutil.copy(original_image, val_data_path + val_dir)
    shutil.move(tmp_image, val_image)


def is_nodule(diameter_mm):
    # ０：不是真正肺结节；１：是真正肺结节。
    nodule_class = 0
    # print float(diameter_mm)
    # print float(diameter_mm) >= 10
    if float(diameter_mm) >= 10:
        nodule_class = 1
    return nodule_class


#####################

# Read the annotations CSV file in (skipping first row).

csvFileObj = open(TIANCHI_test_annotations)
readerObj = csv.DictReader(csvFileObj)

# csv_row('seriesuid', 'diameter_mm', 'nodule_class')
for row in readerObj:
    if readerObj.line_num == 1:
        continue  # skip first row

    csv_row(row['seriesuid'], row['diameter_mm'], is_nodule(row['diameter_mm']))

csvFileObj.close()


# Write out the test.txt CSV file.
csvFileObj = open(os.path.join(output_path, val_file), 'w')
csvWriter = csv.writer(csvFileObj)
for row in csvRows:
    # print row
    csvWriter.writerow(row)
csvFileObj.close()
