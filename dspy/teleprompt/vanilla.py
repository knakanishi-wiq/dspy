import random
from ..utils import logger
from .teleprompt import Teleprompter


class LabeledFewShot(Teleprompter):
    def __init__(self, k=16):
        self.k = k

    def compile(self, student, *, trainset, sample=True):
        self.student = student.reset_copy()
        self.trainset = trainset

        if len(self.trainset) == 0:
            return self.student

        rng = random.Random(0)
        for predictor in self.student.predictors():
            if sample:
                logger.optimizer(f"LabeledFewShot: sampling {self.k} demos")
                predictor.demos = rng.sample(self.trainset, min(self.k, len(self.trainset)))
            else:
                logger.optimizer(f"LabeledFewShot: using {min(self.k, len(self.trainset))} demos")
                predictor.demos = self.trainset[: min(self.k, len(self.trainset))]

        return self.student


# NOTE: I believe templatev2 keeps rdemos as long as they have the last field.
# This may change later, especially with the introduction of required vs optional fields.
# NOTE: Since we're relying on downstream code to handle the demos, this sampling may be sub-sampled.
