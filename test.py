"""Test the SQL"""
import sqlite3
import base64
from SQL import Image, load_str, name_list, image_number, image_dict, search_image_dict

con = sqlite3.connect("image_data.db")
cur = con.cursor()


def test_Image():
    """Test functions of class Image"""
    assert Image(cur, "Simple_Linear").detect_image() == True
    assert Image(cur, "Logistic_Linear").detect_image() == False
    assert Image(cur, "Simple_Linear").date == "2021-04-20"
    assert Image(cur, "Breslow-Day_Test").source == "Course BIOSTAT703 slide"


def test_load_str():
    """Test function load_str"""
    value_list = [
        "Moments",
        "Basic knowledge of Moments",
        "2021-04-26",
        "Course BIOSTAT701 slide",
    ]
    load_str(cur, value_list)
    con.commit()
    assert Image(cur, "Moments").source == "Course BIOSTAT701 slide"
    assert Image(cur, "Moments").date == "2021-04-26"
    with open("./image/Moments.png", "rb") as f:
        assert Image(cur, "Moments").data == base64.b64encode(f.read()).decode()


def test_name_list():
    """Test function name_list"""
    cur.execute("select name from image")
    current_list = [name[0] for name in cur.fetchall()]
    assert name_list(cur) == current_list


def test_image_number():
    """Test function image_number"""
    cur.execute("select name from image")
    current_list = [name[0] for name in cur.fetchall()]
    assert image_number(cur) == len(current_list)


def test_image_dict():
    """Test function image_dict"""
    assert image_dict(cur)["name"] == name_list(cur)


def test_search_image_dict():
    """Test function search_iamge_dict"""
    assert search_image_dict(cur, "Linear")["name"] == [
        "Simple_Linear",
        "Multiple_Linear",
    ]
    assert search_image_dict(cur, "Sim")["name"] == ["Simple_Linear"]
    assert search_image_dict(cur, "_Tes")["name"] == ["Breslow-Day_Test"]
