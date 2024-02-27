import glob
import os
import shutil
from urllib.parse import unquote, urlparse

import numpy as np
import supervisely as sly
from cv2 import connectedComponents
from dataset_tools.convert import unpack_if_archive
from supervisely.io.fs import (
    file_exists,
    get_file_ext,
    get_file_name,
    get_file_name_with_ext,
)
from tqdm import tqdm

import src.settings as s


def download_dataset(teamfiles_dir: str) -> str:
    """Use it for large datasets to convert them on the instance"""
    api = sly.Api.from_env()
    team_id = sly.env.team_id()
    storage_dir = sly.app.get_data_dir()

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, str):
        parsed_url = urlparse(s.DOWNLOAD_ORIGINAL_URL)
        file_name_with_ext = os.path.basename(parsed_url.path)
        file_name_with_ext = unquote(file_name_with_ext)

        sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
        local_path = os.path.join(storage_dir, file_name_with_ext)
        teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

        fsize = api.file.get_directory_size(team_id, teamfiles_dir)
        with tqdm(
            desc=f"Downloading '{file_name_with_ext}' to buffer...",
            total=fsize,
            unit="B",
            unit_scale=True,
        ) as pbar:
            api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)
        dataset_path = unpack_if_archive(local_path)

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, dict):
        for file_name_with_ext, url in s.DOWNLOAD_ORIGINAL_URL.items():
            local_path = os.path.join(storage_dir, file_name_with_ext)
            teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

            if not os.path.exists(get_file_name(local_path)):
                fsize = api.file.get_directory_size(team_id, teamfiles_dir)
                with tqdm(
                    desc=f"Downloading '{file_name_with_ext}' to buffer...",
                    total=fsize,
                    unit="B",
                    unit_scale=True,
                ) as pbar:
                    api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)

                sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
                unpack_if_archive(local_path)
            else:
                sly.logger.info(
                    f"Archive '{file_name_with_ext}' was already unpacked to '{os.path.join(storage_dir, get_file_name(file_name_with_ext))}'. Skipping..."
                )

        dataset_path = storage_dir
    return dataset_path


def count_files(path, extension):
    count = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(extension):
                count += 1
    return count


def convert_and_upload_supervisely_project(
    api: sly.Api, workspace_id: int, project_name: str
) -> sly.ProjectInfo:
    ### Function should read local dataset and upload it to Supervisely project, then return project info.###
    dataset_path = "/home/alex/DATASETS/TODO/DeepSportradar/archive"
    batch_size = 5
    group_tag_name = "im id"

    train_folders = [
        "ks-fr-stchamond",
        "ks-fr-fos",
        "ks-fr-strasbourg",
        "ks-fr-vichy",
        "ks-fr-nantes",
        "ks-fr-bourgeb",
        "ks-fr-gravelines",
        "ks-fr-monaco",
        "ks-fr-poitiers",
        "ks-fr-nancy",
        "ks-fr-lemans",
    ]
    val_folders = ["ks-fr-blois"]
    test_folders = ["ks-fr-caen", "ks-fr-roanne", "ks-fr-limoges"]
    ds_name_to_folders = {"train": train_folders, "val": val_folders, "test": test_folders}

    def create_ann(image_path):
        labels = []
        tags = []

        image_np = sly.imaging.image.read(image_path)[:, :, 0]
        img_height = image_np.shape[0]
        img_wight = image_np.shape[1]

        im_name = get_file_name(image_path)

        id_data = im_name.split("_")[1]
        group_id = sly.Tag(group_tag_meta, value=id_data)
        tags.append(group_id)

        seq_val = int(image_path.split("/")[-2])
        seq = sly.Tag(seq_meta, value=seq_val)
        tags.append(seq)

        court_tag_meta = name_to_tag[im_name.split("_")[0]]
        court_tag = sly.Tag(court_tag_meta)
        tags.append(court_tag)

        im_path = ("/").join(image_path.split("/")[:-1])
        mask_name = ("_").join(im_name.split("_")[:-1])

        mask_path = os.path.join(im_path, mask_name + "_humans.png")
        if file_exists(mask_path):
            mask_np = sly.imaging.image.read(mask_path)[:, :, 0]
            if len(np.unique(mask_np)) > 1:
                unique_pixels = np.unique(mask_np)[1:]

                for pixel in unique_pixels:
                    obj_class = pixel_to_class.get(pixel)
                    mask = mask_np == pixel
                    if pixel == 3:
                        ret, curr_mask = connectedComponents(mask.astype("uint8"), connectivity=8)
                        for i in range(1, ret):
                            obj_mask = curr_mask == i
                            curr_bitmap = sly.Bitmap(obj_mask)
                            if curr_bitmap.area > 15:
                                curr_label = sly.Label(curr_bitmap, obj_class)
                                labels.append(curr_label)
                    else:
                        curr_bitmap = sly.Bitmap(mask)
                        curr_label = sly.Label(curr_bitmap, obj_class)
                        labels.append(curr_label)

        return sly.Annotation(img_size=(img_height, img_wight), labels=labels, img_tags=tags)

    human = sly.ObjClass("human", sly.Bitmap)
    ball = sly.ObjClass("ball", sly.Bitmap)

    pixel_to_class = {3: human, 11: ball}

    camcourt1 = sly.TagMeta("camcourt 1", sly.TagValueType.NONE)
    camcourt2 = sly.TagMeta("camcourt 2", sly.TagValueType.NONE)
    seq_meta = sly.TagMeta("sequence", sly.TagValueType.ANY_NUMBER)

    name_to_tag = {"camcourt1": camcourt1, "camcourt2": camcourt2}

    group_tag_meta = sly.TagMeta(group_tag_name, sly.TagValueType.ANY_STRING)

    project = api.project.create(workspace_id, project_name, change_name_if_conflict=True)
    meta = sly.ProjectMeta(
        obj_classes=[human, ball], tag_metas=[group_tag_meta, camcourt1, camcourt2, seq_meta]
    )
    api.project.update_meta(project.id, meta.to_json())
    api.project.images_grouping(id=project.id, enable=True, tag_name=group_tag_name)

    for ds_name, folders in ds_name_to_folders.items():

        dataset = api.dataset.create(project.id, ds_name, change_name_if_conflict=True)

        for curr_folder in folders:

            curr_path = os.path.join(dataset_path, curr_folder.upper())

            all_images_pathes = glob.glob(curr_path + "/*/*.png")

            images_pathes = []
            # images_names = []
            for im_path in all_images_pathes:
                if get_file_ext(im_path) != ".json" and "_humans" not in im_path:
                    # images_names.append(get_file_name_with_ext(im_path))
                    images_pathes.append(im_path)

            progress = sly.Progress("Create dataset {}".format(ds_name), len(images_pathes))

            for img_pathes_batch in sly.batched(images_pathes, batch_size=batch_size):
                img_names_batch = [get_file_name_with_ext(im_path) for im_path in img_pathes_batch]

                img_infos = api.image.upload_paths(dataset.id, img_names_batch, img_pathes_batch)
                img_ids = [im_info.id for im_info in img_infos]

                anns = [create_ann(image_path) for image_path in img_pathes_batch]
                api.annotation.upload_anns(img_ids, anns)

                progress.iters_done_report(len(img_pathes_batch))

    return project
