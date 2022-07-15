# :eyes: Eyes-Tracking-Dataset-Generator :eyes:

## If you want to collect the dataset for eyes tracking by using YOLOv5, this program can help!!! :smiley:

Here you can easily generate the trainging  dataset for YOLOv5 in the following steps...

<pre><code>git clone https://github.com/boyleerock/Eyes-Tracking-s-Dataset-Generator</code></pre>

- Download the pretrained model [shape_predictor_68_face_landmarks.dat](https://github.com/tzutalin/dlib-android/blob/master/data/shape_predictor_68_face_landmarks.dat)

- Then CHANGE your images folder's name in loop_directory("images/") in findeyes_convert2yoloformat .py

<pre><code>python findeyes_convert2yoloformat.py</code></pre>




### Original image:

![1657_leo](https://user-images.githubusercontent.com/61671531/179191177-6cb7da80-4ee4-44d1-a8ad-52366dae0933.jpg)




## After finding eyes :eyes: and create label of YOLOv5...
### :star2: The final image result:

![1657_leo](https://user-images.githubusercontent.com/61671531/179191131-04c314bc-444a-4f6f-a21f-d649e10ff147.jpg)

### :star2: Resulting label of YOLOv5:

![2022-07-15 17-02-34 的螢幕擷圖](https://user-images.githubusercontent.com/61671531/179191421-8a83be1b-1252-4ff8-8c89-7a73ebe11817.png)
