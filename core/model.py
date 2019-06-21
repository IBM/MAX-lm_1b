#
# Copyright 2018-2019 IBM Corp. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import logging
import os
import re
from maxfw.model import MAXModelWrapper

logger = logging.getLogger()


class ModelWrapper(MAXModelWrapper):
    """Model wrapper for Keras models"""

    MODEL_NAME = 'lm_1b'
    MODEL_LICENSE = "Apache v2"
    MODEL_META_DATA = {
        'id': '{}'.format(MODEL_NAME.lower()),
        'name': '{} TensorFlow Model'.format(MODEL_NAME),
        'description': 'Generative language model trained on the One Billion Words samples set',
        'type': 'Generative Language Model',
        'license': '{}'.format(MODEL_LICENSE)
    }

    def __init__(self):
        pass

    def read_text(self, text_data):
        text = text_data.decode("utf-8")
        return text

    def _predict(self, x):
        # this model does not like punctuation touching characters
        x = re.sub('([.,!?()])', r' \1 ', x)  # https://stackoverflow.com/a/3645946/

        os.system("python lm_1b/lm_1b_eval.py --mode sample \
                                     --prefix \"" + x + "\" \
                                     --pbtxt assets/data/graph-2016-09-10.pbtxt \
                                     --vocab_file assets/data/vocab-2016-09-10.txt  \
                                     --ckpt 'assets/data/ckpt-*' \
                                     --num_samples 1")

        try:
            # if the above os.system command fails then "out.txt" is never created
            txt_file = open("out.txt", "r")
        except OSError:
            print("Error generating a prediction, this is likely due to a lack of memory allocated to Docker")
            print("The minimum recommended resources for this model is 8 GB Memory and 4 CPUs")
        else:
            txt = txt_file.read()
            txt_file.close()
            return txt
