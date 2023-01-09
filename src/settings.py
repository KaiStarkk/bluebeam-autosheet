import re
import yaml
import UI

# TODO - point to Sharepoint / network share for config data such as default settings path?
__path = r"./src/settings.yaml"


def readConfig():
    read_file = open(__path, "r")
    config = yaml.full_load(read_file.read())
    read_file.flush()
    read_file.close()
    return config


def saveConfig(config, form, table):
    # TODO - need to check safety of this as well, similar to the table load
    # TODO - alert success / failure
    config["meta"].update({
        "project name": form.itemAt(1).widget().text(),
        "project number": form.itemAt(3).widget().text(),
        "client": form.itemAt(5).widget().text(),
        "issue date": form.itemAt(7).widget().text(),
        "issue description": form.itemAt(9).widget().text(),
        "construction status": form.itemAt(11).widget().text(),
        "stamp": form.itemAt(13).widget().text(),
        "approved by": form.itemAt(15).widget().text(),
        "drawn by": form.itemAt(17).widget().text(),
        "rev": form.itemAt(19).widget().text()
    })

    for row in range(table.rowCount()):
        legal = re.compile(r"[<>/{}[\]\\~`]")
        if (not table.item(row, 0).text() or
            not table.item(row, 1).text() or
            not table.item(row, 2).text() or
            not table.item(row, 3).text() or
            legal.search(table.item(row, 0).text()) or
            legal.search(table.item(row, 1).text()) or
            legal.search(table.item(row, 2).text()) or
            legal.search(table.item(row, 3).text())
            ):
            UI.error_box("Data is empty or contains illegal characters")
            return
        config["drawings"].update({
            table.item(row, 0).text(): {
                "title": table.item(row, 1).text(),
                "scale": table.item(row, 2).text(),
                "discipline": table.item(row, 3).text(),
                "type": table.cellWidget(row, 4).currentText()
            }
        })
    with open(__path, 'w') as file:
        file.write(r"%YAML 1.2")
        file.write("\n---\n")
        yaml.dump(config, file)
