"""The operation of database"""
import sqlite3
import base64
import re

con = sqlite3.connect("image_data.db")
cur = con.cursor()

cmd = "CREATE TABLE IF NOT EXISTS image (name text, data text, description text, date text, source text)"
cur.execute(cmd)


class Image:
    """Image class"""

    def __init__(self, cur, name):
        """Initialize."""
        self.cur = cur
        self.name = name

    def detect_image(self):
        """Detect whether the image exists in the database."""
        cmd = f"select * from image where image.name = '{self.name}'"
        self.cur.execute(cmd)
        if self.cur.fetchone() != None:
            return True
        else:
            return False

    @property
    def data(self):
        """A property image data."""
        cmd = f"select data from image where image.name = '{self.name}'"
        self.cur.execute(cmd)
        return self.cur.fetchone()[0]

    @property
    def description(self):
        """A property description."""
        cmd = f"select description from image where image.name = '{self.name}'"
        self.cur.execute(cmd)
        return self.cur.fetchone()[0]

    @property
    def date(self):
        """A property date."""
        cmd = f"select date from image where image.name = '{self.name}'"
        self.cur.execute(cmd)
        return self.cur.fetchone()[0]

    @property
    def source(self):
        """A property description."""
        cmd = f"select source from image where image.name = '{self.name}'"
        self.cur.execute(cmd)
        return self.cur.fetchone()[0]


def load_txt(cur, filepath):
    """Load image data through txt file"""
    with open(filepath) as f:
        for line in f.readlines():
            line = line.replace("\n", "")
            value_list = line.split(";")
            if Image(cur, value_list[0]).detect_image() == False:
                with open(f"./image/{value_list[0]}.png", "rb") as stream:
                    img_data = base64.b64encode(stream.read()).decode()
                cmd = f"INSERT INTO image (name, data, description, date, source) VALUES('{value_list[0]}','{img_data}','{value_list[1]}','{value_list[2]}','{value_list[3]}')"
                cur.execute(cmd)
    return True


load_txt(cur, "database_txt/image_description.txt")
con.commit()


def load_str(cur, value_list):
    """Load image data through str list"""
    if Image(cur, value_list[0]).detect_image() == False:
        with open(f"./image/{value_list[0]}.png", "rb") as stream:
            img_data = base64.b64encode(stream.read()).decode()
        cmd = f"INSERT INTO image (name, data, description, date, source) VALUES('{value_list[0]}','{img_data}','{value_list[1]}','{value_list[2]}','{value_list[3]}')"
        cur.execute(cmd)
        return True
    return False


def name_list(cur):
    """Obtain the name list of image in database"""
    cmd = f"select name from image"
    cur.execute(cmd)
    return [name[0] for name in cur.fetchall()]


def image_number(cur):
    """Obtain the number of image in database"""
    return len(name_list(cur))


def image_dict(cur):
    """Obtain the dict of all images in database"""
    image_dict = {}
    for label in ["name", "data", "description", "date", "source"]:
        cmd = f"select {label} from image"
        cur.execute(cmd)
        image_dict[label] = [value[0] for value in cur.fetchall()]
    return image_dict


def search_image_dict(cur, name_str):
    """Search and obtain the dict of part of the images in database"""
    match_name = []
    for name in name_list(cur):
        if re.search(name_str, name) != None:
            match_name.append(name)
    image_dict = {}
    for label in ["name", "data", "description", "date", "source"]:
        image_dict[label] = []
    for name in match_name:
        for label in ["name", "data", "description", "date", "source"]:
            cmd = f"select {label} from image where image.name = '{name}'"
            cur.execute(cmd)
            image_dict[label].append(cur.fetchone()[0])
    return image_dict


con.close()
