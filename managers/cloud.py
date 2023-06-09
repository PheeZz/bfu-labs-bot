from repositories.disk import disk as cloud_drive
from io import BytesIO


class CloudManager:
    @classmethod
    def create_group_folder(cls, group_name: str):
        dst_path = f"/{group_name}"
        cloud_drive.mkdir(dst_path)
        cls.make_group_public(group_name)
        cloud_drive.mkdir(dst_path + "/Лабораторные")

    @staticmethod
    def create_student_folder(group_name: str, student_name: str):
        dst_path = f"/{group_name}/{student_name}"
        cloud_drive.mkdir(dst_path)
        return dst_path

    @staticmethod
    def add_lab_to_group_folder(group_name: str, lab_path_or_file: str | BytesIO, lab_name: str) -> str:
        dst_path = f"/{group_name}/Лабораторные/{lab_name}"
        cloud_drive.upload(lab_path_or_file, dst_path, overwrite=True)
        cloud_drive.publish(dst_path)
        return dst_path

    @staticmethod
    def add_lab_from_student(group_name: str, student_name: str, lab_path_or_file: str | BytesIO, lab_name: str):
        student_lab_name = student_name + "_" + lab_name
        dst_path = f"/{group_name}/{student_name}/{student_lab_name}"
        cloud_drive.upload(lab_path_or_file, dst_path, overwrite=True)
        return dst_path

    @staticmethod
    def make_group_public(group_name: str):
        cloud_drive.publish(f"/{group_name}")

    @staticmethod
    def get_group_folder_link(group_name: str):
        return cloud_drive.get_meta(f"/{group_name}").public_url

    @staticmethod
    def get_public_link_by_destination_path(destination_path: str):
        url = cloud_drive.get_meta(destination_path).public_url
        if not url:
            cloud_drive.publish(destination_path)
            url = cloud_drive.get_meta(destination_path).public_url
        return url

    @classmethod
    def is_group_exists(cls, group_name: str):
        return cloud_drive.exists(f"/{group_name}")

    @staticmethod
    def get_files_by_link(paths: tuple[str]) -> tuple[list[BytesIO], list[str]]:
        files: list[BytesIO] = []
        filenames: list[str] = []
        for path in paths:
            file_ = BytesIO()
            cloud_drive.download(path, file_)
            files.append(file_)

            filename = CloudManager.get_filename_by_path(path)
            filenames.append(filename)

        return files, filenames

    @staticmethod
    def get_file_by_link(path: str) -> tuple[BytesIO, str]:
        file_ = BytesIO()
        cloud_drive.download(path, file_)
        filename = CloudManager.get_filename_by_path(path)
        file_.seek(0)
        return file_, filename

    @staticmethod
    def get_filename_by_path(path: str):
        return path.split("/")[-1]
