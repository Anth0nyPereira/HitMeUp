class Bucket:
    def __init__(self, loader):
        self.loader = loader
        self.bucket = self.loader.loadModel("objects/bucket.obj")
        self.bucket.setScale(0.3, 0.3, 0.3)
        self.bucket.setP(-90)
        # self.bucket.setH(180)

    def get_bucket(self):
        return self.bucket
