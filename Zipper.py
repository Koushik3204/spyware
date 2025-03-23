import shutil
def zip_folder(folder_path, output_zip):
    shutil.make_archive(output_zip, 'zip', folder_path)
    print(f"Folder '{folder_path}' successfully zipped as '{output_zip}.zip'")

# Example usage:
folder_to_zip = "C:/Users/YOGESH/OneDrive/Desktop/data"  # Change this to your folder path
output_zip_file = "C:/Users/YOGESH/OneDrive/Desktop/temp/logs.zip"  # Change this to the desired zip file name (without .zip)
zip_folder(folder_to_zip, output_zip_file)
