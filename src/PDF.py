from PyPDF2 import PdfReader, PdfWriter
import pathlib
import re
import shutil
import UI
import settings

# TODO - point to Sharepoint site / network share for config data such as template files?
__templates = {
    "legend": r"bin\config - Legend.pdf",
    "layout": r"bin\config - Layout.pdf",
    "details": r"bin\config - Details.pdf",
    "SLD": r"bin\config - SLD.pdf"
}


def process_templates():
    config = settings.readConfig()
    if not _in_correct_path():
        return
    if not _copy_files(config):
        return
    _populate_files(config)
    # TODO - Summarize output back to user


def _in_correct_path():
    # TODO - Move target directory into a user interface configurable option,
    # rather than always working from pwd
    pattern = re.compile(
        r".*[0-9]+\\Project Documents\\Electrical\\Design\\Sketches.*")
    folder = __file__
    if (not pattern.match(folder)):
        UI.error_box(
            "Not in correct folder structure. Place in sketches directory.")
        return False
    if (not pathlib.Path("./src/settings.yaml").exists()):
        UI.error_box("No config file exists")
        return False
    return True


def _copy_files(config):
    for drawing in (config["drawings"].items()):
        copyfile = __templates[drawing[1]["type"]]
        dest = "{0} - {1}_{2}.pdf".format(drawing[0],
                                          drawing[1]["title"], config["meta"]["rev"])
        config["drawings"][drawing[0]].update({
            "path": dest
        })
        if (not pathlib.Path(copyfile).exists()):
            UI.error_box("Can't find templates.")
            return False
        if (pathlib.Path(dest).exists()):
            UI.error_box("Not allowed to overwrite files (yet)")
            return False
        shutil.copyfile(copyfile, dest)
    return True


def _populate_files(config):
    for drawing in (config["drawings"].items()):
        reader = PdfReader(drawing[1]["path"])
        writer = PdfWriter()

        page = reader.pages[0]

        writer.add_page(page)

        writer.update_page_form_field_values(
            writer.pages[0], {
                "PROJECT NUMBER": config["meta"]["project number"],
                "PROJECT NAME": config["meta"]["project name"],

                "SHEET NUMBER": drawing[0],
                "SHEET NAME": drawing[1]["title"],

                "SCALE": drawing[1]["scale"],
                "REVISION": config["meta"]["rev"],

                # "CLIENT": config["meta"]["revision"]["id"], TODO - form templates currently don't have clients

                "STAMP": config["meta"]["stamp"],
                "CONSTRUCTION STATUS": config["meta"]["construction status"],
                "DISCIPLINE": drawing[1]["discipline"],

                "REV1": config["meta"]["rev"],
                "DESCRIPTION1": config["meta"]["issue description"],
                "DRAWN1": config["meta"]["drawn by"],
                "APPROVED1": config["meta"]["approved by"],
                "DATE1": config["meta"]["issue date"]
            }
        )

        with open(drawing[1]["path"], "wb") as output_stream:
            writer.write(output_stream)
