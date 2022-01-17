from panda3d.core import TextureStage, Material, AmbientLight

from color import Color


class Bucket:
    def __init__(self, render, loader):
        self.render = render
        self.loader = loader
        self.bucket = self.loader.loadModel("objects/OldBucket.obj")
        self.bucket.setScale(0.3, 0.4, 0.3)
        self.bucket.setP(-90)

        # textures experiment
        self.first_tex = self.loader.loadTexture("objects/Outside_Diffuse.tif")
        self.second_tex = self.loader.loadTexture("objects/Outside_Glossiness.tif")
        self.ts1 = TextureStage('ts1')
        self.third_tex = self.loader.loadTexture("objects/Outside_Specular.tif")
        self.ts2 = TextureStage('ts2')
        self.bucket.setTexture(self.first_tex)
        self.bucket.setTexture(self.ts1, self.second_tex)
        self.bucket.setTexture(self.ts2, self.third_tex)

        # self.bucket.setColorScale(Color.gold.value)
        self.bucket.setColorScale(Color.generate_random_color().value)

    def get_bucket(self):
        return self.bucket
