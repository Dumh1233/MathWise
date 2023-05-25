import os
import shutil
from pdf2image import convert_from_path


def split_pdf_to_pages(file_name, dir_path):
    file_name = file_name.split(".pdf")[0]
    return convert_from_path(dir_path + file_name + ".pdf",
                             poppler_path='./poppler-0.68.0/bin')


def split_jpgs_to_equations(file_path):
    os.system("py ../dl_models/page_segmentation_model/yolov5-master/detect.py "
              "--weights ../dl_models/page_segmentation_model/best.pt "
              "--conf 0.1 "
              "--source " + file_path + '.jpg' + " --save-crop "
              "--project " + file_path + " --name equations")


def split_equations(file_name):
    dir_path = './resources/static/assets/'
    dir_upload_path = dir_path + 'uploads/'
    dir_split_path = dir_path + 'uploads_splits/' + file_name.rsplit('.', 1)[0]
    os.makedirs(dir_split_path, exist_ok=True)
    if file_name.rsplit('.', 1)[1] == "pdf":
        pages = split_pdf_to_pages(file_name, dir_upload_path)
        for i in range(len(pages)):
            pages[i].save(dir_split_path + "/page_" + str(i) + '.jpg', 'JPEG')
            split_jpgs_to_equations(dir_split_path + "/page_" + str(i))
    else:
        shutil.copyfile(dir_upload_path + file_name,
                        dir_split_path + '/page_0.jpg')
        split_jpgs_to_equations(dir_split_path + '/page_0')
    crop_equations_list = []
    for directory in next(os.walk(dir_split_path))[1]:
        tmp_path = dir_split_path + "/" + directory + "/equations/crops"
        for subdir, dirs, files in os.walk(tmp_path):
            for dir in dirs:
                tmp_path += "/" + dir
                if os.path.isdir(tmp_path):
                    for file in [f for f in os.listdir(tmp_path) if os.path.isfile(os.path.join(tmp_path, f))]:
                        crop_equations_list.append(tmp_path + "/" + file)
    print(crop_equations_list)
    return crop_equations_list
