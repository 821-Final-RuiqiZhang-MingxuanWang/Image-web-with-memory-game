# Image web with memory game

This simple image web is used to show some images related to biostatsics knowledge, these images can be searched by key words. Before going to the web, users need to pass a small memory game. The game has a 3 &times; 3 table, 9 three-digit numbers, and only one pair of them is the same. Users have 9 seconds to find this pair of numbers, and then they can input the position of this pair of numbers like "1,9". After they pass the memory game, they can see all the images in the database. If they don't want to play the game, they can enter the access code "BIOSTAT821" to skip the game, or they can use url "localhost:8105/passed" to see the image web.

### Install

clone this repository, cd to this file folder "Image-web-with-memory-game", then run in terminal.

>pip install -r requirements.txt   
>./main.sh

Then users can use url "localhost:8105" to use the web.

### Function

If users' answer is right, they will go to the image web. If their answer is wrong, they will go to the web page used to replay the game. 

About the image web, the images are in the image folder. After running the webpage once, it will also be stored in the sql database "image_data.db" in the form of base64 encoding. This web will present all images in the sql database, if users use search function, this web will just present images with keyword in file name. Users can also upload png file through the web. Besides the file, users also need to input file name, description, source and date. The uploaded file should be the form of png and the entered name cannot be the same as the existing name. After uploading new image, the web will also present the new image.

### Architecture

This web uses a vanilla JavaScript/HTML user interface, Python server, and SQLite database.




