from PIL.Image import Image

from app import app
from flask import request, render_template
import os
import cv2
import numpy as np
from PIL import Image

app.config['INITIAL_FILE_UPLOADS'] = 'app/static/uploads'


@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":
        option = request.form['options']
        image_upload = request.files["image_upload"]
        imagename = image_upload.filename
        image_u = Image.open(image_upload)
        image_u = image_u.resize((600, 400))
        image_up = np.array(image_u.convert("RGB"))
        h_image, w_image, _ = image_up.shape

        if option == "logo_watermark":
            image_upload = request.files["logo_upload"]
            logoname = image_upload.filename
            image_l = Image.open(image_upload)
            image_l = image_l.resize((200, 150))
            image_logo = np.array(image_l.convert("RGB"))
            h_logo, w_logo, _ = image_logo.shape
            center_y = int(h_image / 2)
            center_x = int(w_image / 2)
            top_y = int(center_y - (h_logo / 2))
            left_x = int(center_x - (w_logo / 2))
            bottom_y = int(top_y + h_logo)
            right_x = int(left_x + w_logo)

            roi = image_up[top_y: bottom_y, left_x: right_x]
            result = cv2.addWeighted(roi, 0, image_logo, 1, 0)
            image_up[top_y: bottom_y, left_x: right_x] = result
            cv2.line(image_up, (0, center_y), (left_x, center_y), (0, 0, 255), 1)
            cv2.line(image_up, (right_x, center_y), (w_image, center_y), (0, 0, 255), 1)

            img: Image = Image.fromarray(image_up, 'RGB')
            img.save(os.path.join(app.config['INITIAL_FILE_UPLOADS'], 'image2.png'))
            full_filename = 'static/uploads/image2.png'
            return render_template('index.html', full_filename=full_filename)

        else:
            text_mark = request.form["text_mark"]

            cv2.putText(image_up, text_mark, (w_image - 95, h_image - 10), fontFace=cv2.FONT_HERSHEY_COMPLEX,
                        fontScale=0.5,
                        color=(0, 0, 255), thickness=2, lineType=cv2.LINE_4)
            timg: Image = Image.fromarray(image_up, 'RGB')
            timg.save(os.path.join(app.config['INITIAL_FILE_UPLOADS'], 'image3.png'))
            full_filename = 'static/uploads/image3.png'
            return render_template('index.html', full_filename=full_filename)
    else:
        return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
