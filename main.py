import cv2
import numpy as np
from moviepy.editor import VideoFileClip, concatenate_videoclips, AudioFileClip, CompositeAudioClip,TextClip,CompositeVideoClip
from flask import Flask, jsonify, request, current_app
from flask_cors import CORS, cross_origin
import uuid
import os

img_size = 200
app = Flask(__name__)
CORS(app)

def sepia(src_image):
    gray = cv2.cvtColor(src_image, cv2.COLOR_BGR2GRAY)
    normalized_gray = np.array(gray, np.float32)/255
    #solid color
    sepia = np.ones(src_image.shape)
    sepia[:,:,0] *= 153 #B
    sepia[:,:,1] *= 204 #G
    sepia[:,:,2] *= 255 #R
    #hadamard
    sepia[:,:,0] *= normalized_gray #B
    sepia[:,:,1] *= normalized_gray #G
    sepia[:,:,2] *= normalized_gray #R
    return np.array(sepia, np.uint8)

def image_to_video(path):
    img = cv2.imread(path + '.png')
    height, width, layers = img.shape
    size = (width,height)
    out = cv2.VideoWriter(path + '.mp4',cv2.VideoWriter_fourcc(*'DIVX'), 15, size)
    
    for _ in range(0,10):
        out.write(sepia(img))
    
    out.release()
    print("\n Log: \tImage saved to " + path + ".mp4\n")

@app.route('/', methods=['POST'])
@cross_origin()
def index():
    # Initiate returned structure
    data = {
        "success": False
    }
    if request.method == "POST":
        image1 = 'media/image1'
        image2 = 'media/image2'
        image3 = 'media/image3'
        image4 = 'media/image4'
        video1 = 'media/video1'
        video2 = 'media/video2'
        video3 = 'media/video3'
        video4 = 'media/video4'
        if(
            'image1' in request.files and
            'image2' in request.files and
            'image3' in request.files and
            'image4' in request.files and 
            'video1' in request.files and 
            'video2' in request.files and 
            'video3' in request.files and 
            'video4' in request.files
            ):
            
            request.files['image1'].save(image1 + '.png')
            request.files['image2'].save(image2 + '.png')
            request.files['image3'].save(image3 + '.png')
            request.files['image4'].save(image4 + '.png')
            request.files['video1'].save(video1 + '.mp4')
            request.files['video2'].save(video2 + '.mp4')
            request.files['video3'].save(video3 + '.mp4')
            request.files['video4'].save(video4 + '.mp4')
            
            image_to_video(image1)
            image_to_video(image2)
            image_to_video(image3)
            image_to_video(image4)
            
            txt_clip_3 = TextClip("3",font='Arial', fontsize = 400, color = 'white').set_pos('center').set_duration(1) 
            txt_clip_2 = TextClip("2",font='Arial', fontsize = 400, color = 'white').set_pos('center').set_duration(1) 
            txt_clip_1 = TextClip("1",font='Arial', fontsize = 400, color = 'white').set_pos('center').set_duration(1) 
            
            _video1 = VideoFileClip(video1 + '.mp4')
            _video1_0 = _video1.subclip(0, _video1.duration-3)
            _video1_1 = _video1.subclip(_video1.duration-3,_video1.duration-2)
            _video1_2 = _video1.subclip(_video1.duration-2,_video1.duration-1) 
            _video1_3 = _video1.subclip(_video1.duration-1,_video1.duration-0) 
            
            _video2 = VideoFileClip(video2 + '.mp4')
            _video2_0 = _video2.subclip(0, _video2.duration-3)
            _video2_1 = _video2.subclip(_video2.duration-3,_video2.duration-2)
            _video2_2 = _video2.subclip(_video2.duration-2,_video2.duration-1) 
            _video2_3 = _video2.subclip(_video2.duration-1,_video2.duration-0) 
            
            _video3 = VideoFileClip(video3 + '.mp4')
            _video3_0 = _video3.subclip(0, _video3.duration-3)
            _video3_1 = _video3.subclip(_video3.duration-3,_video3.duration-2)
            _video3_2 = _video3.subclip(_video3.duration-2,_video3.duration-1) 
            _video3_3 = _video3.subclip(_video3.duration-1,_video3.duration-0) 
            
            _video4 = VideoFileClip(video4 + '.mp4')
            _video4_0 = _video4.subclip(0, _video4.duration-3)
            _video4_1 = _video4.subclip(_video4.duration-3,_video4.duration-2)
            _video4_2 = _video4.subclip(_video4.duration-2,_video4.duration-1) 
            _video4_3 = _video4.subclip(_video4.duration-1,_video4.duration-0) 
            
            final_clip = concatenate_videoclips(
                [
                    _video1_0,
                    CompositeVideoClip([_video1_1, txt_clip_3]),
                    CompositeVideoClip([_video1_2, txt_clip_2]), 
                    CompositeVideoClip([_video1_3, txt_clip_1]), 
                    VideoFileClip(image1 + '.mp4'),
                    _video2_0,
                    CompositeVideoClip([_video2_1, txt_clip_3]),
                    CompositeVideoClip([_video2_2, txt_clip_2]), 
                    CompositeVideoClip([_video2_3, txt_clip_1]), 
                    VideoFileClip(image2 + '.mp4'),
                    _video3_0,
                    CompositeVideoClip([_video3_1, txt_clip_3]),
                    CompositeVideoClip([_video3_2, txt_clip_2]), 
                    CompositeVideoClip([_video3_3, txt_clip_1]), 
                    VideoFileClip(image3 + '.mp4'),
                    _video4_0,
                    CompositeVideoClip([_video4_1, txt_clip_3]),
                    CompositeVideoClip([_video4_2, txt_clip_2]), 
                    CompositeVideoClip([_video4_3, txt_clip_1]), 
                    VideoFileClip(image4 + '.mp4'),
                ]
            )
        
            audio = AudioFileClip("audios/LMDA_PHOTOBOOTH.mp3").set_duration(final_clip.duration)
            fx_1 = AudioFileClip("audios/photo_fx_1.mp3")
            fx_2 = AudioFileClip("audios/photo_fx_2.mp3")
            final_clip.audio = CompositeAudioClip(
                [
                    audio.set_start(0),
                    fx_1.set_start(_video1.duration),
                    fx_2.set_start(_video1.duration + _video2.duration + 1),
                    fx_1.set_start(_video1.duration + _video2.duration + _video3.duration + 2),
                    fx_2.set_start(_video1.duration + _video2.duration + _video3.duration + _video4.duration + 3)
                ]
            )
            name = 'files/' + str(uuid.uuid4()) + '.mp4'
            final_clip.write_videofile(name, codec="libx264", audio_codec="aac")
            
            return {
                "success": True,
                "filename": name
            }
    return jsonify(data)

@app.route('/files/<filename>/download')
def download_file(filename):
    file_path = 'files/<filename>'
    file_handle = open(file_path, 'r')

    # This *replaces* the `remove_file` + @after_this_request code above
    def stream_and_remove_file():
        yield from file_handle
        file_handle.close()
        os.remove(file_path)

    return current_app.response_class(
        stream_and_remove_file(),
        headers={'Content-Disposition': 'attachment', 'filename': filename}
    )


if __name__ == "__main__":
    print(("* Loading Keras model and Flask starting server..."
    "please wait until server has fully started"))
    app.run(host='localhost', port=3000)