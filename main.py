import cv2
from moviepy.editor import VideoFileClip, concatenate_videoclips, AudioFileClip, CompositeAudioClip
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS, cross_origin

img_size = 200
app = Flask(__name__)
CORS(app)


def image_to_video(path):
    img = cv2.imread(path + '.png')
    height, width, layers = img.shape
    size = (width,height)
    out = cv2.VideoWriter(path + '.mp4',cv2.VideoWriter_fourcc(*'DIVX'), 15, size)
    
    for i in range(0,10):
        out.write(img)
    
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
            
            _video1 = VideoFileClip(video1 + '.mp4')
            _video2 = VideoFileClip(video2 + '.mp4')
            _video3 = VideoFileClip(video3 + '.mp4')
            _video4 = VideoFileClip(video4 + '.mp4')
            
            final_clip = concatenate_videoclips(
                [
                    _video1,
                    VideoFileClip(image1 + '.mp4'),
                    _video2,
                    VideoFileClip(image2 + '.mp4'),
                    _video3,
                    VideoFileClip(image3 + '.mp4'),
                    _video4,
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
            final_clip.write_videofile('final.mp4', codec="libx264", audio_codec="aac")
            
            print("done")
            return send_file("final.mp4", attachment_filename='final.mp4')
            
    return jsonify(data)


if __name__ == "__main__":
    print(("* Loading Keras model and Flask starting server..."
    "please wait until server has fully started"))
    app.run(host='localhost', port=8000)