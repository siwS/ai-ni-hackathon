import sidekick
import pandas as pd
import os
import wave
import matplotlib.pylab as pylab
from PIL import Image


class Boss:

    __url = ""
    __token = ""

    def __init__(self):
        pass
    
    # This is all we need
    # Create folders below for images
    def make_prediction_from_wav(self, wav_name):
        store_folder = "new_wavs"
        output_folder = "spectros"
        self.graph_spectrogram(indir=store_folder, outdir=output_folder, filename=wav_name)
        self.test_image(spectro_name=f"{output_folder}/{wav_name}.png")

    def graph_spectrogram(self, indir, outdir, filename):
        wav_file = f"{indir}/{filename}"
        try:
            sound_info, frame_rate = self.get_wav_info(wav_file)
            pylab.figure(figsize=(4,3))
            pylab.specgram(sound_info, Fs=frame_rate)
            pylab.savefig(f"{outdir}/{filename}.png")
            pylab.close()
        except:
            return

    def get_wav_info(self, wav_file):
        wav = wave.open(wav_file, 'r')
        frames = wav.readframes(-1)
        sound_info = pylab.frombuffer(frames, 'int16')
        frame_rate = wav.getframerate()
        wav.close()
        return sound_info, frame_rate

    def build_dataframe(self, noisy, clean):
        li = []
        for f in os.listdir(noisy):
            if os.path.isfile(f"{clean}/{f}"):
                li.append({"noisy": f"{noisy}/{f}", "clean": f"{clean}/{f}"})
        df = pd.DataFrame(li, columns=["noisy", "clean"])

        sidekick.create_dataset(
            'files/output.zip',
            df,
            path_columns=["noisy", "clean"],
            progress=True
        )

    def test_image(self, spectro_name):
        # Connect to deployment
        client = sidekick.Deployment(
            url=self.__url,
            token=self.__token,
            dtypes_in={'image': 'Image (32x32x3)'}, #TODO: get this from deployment page
            dtypes_out={'image': 'Image (32x32x3)'}
        )
        # Load image
        image = Image.open(spectro_name)

        # Get predictions from model
        x = client.predict(image=image)
        print(x)
