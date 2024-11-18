from _laura_lib import lib
import numpy as np
import tempfile
import json

class LauraModel:
    def __init__(self, p0, p1, p2, p3):
        self.model = lib.create_model(p0.encode(), p1.encode(), p2.encode(), p3.encode())
        self.n_amp = 0

    def init_from_jsonfile(self, json_file, item_name):
        lib.model_init(self.model, json_file.encode(), item_name.encode())
        self.n_amp = lib.model_getnTotAmp(self.model)

    def init_from_json(self, data):
        with tempfile.NamedTemporaryFile(delete_on_close=True) as fp:
            json.dump({"model": data}, fp)
            lib.model_init(self.model, fp.name.encode(), "model".encode())
        self.n_amp = lib.model_getnTotAmp(self.model)

    def get_amp(self, m13Sq, m23Sq):
        lib.model_calcLikelihoodInfo(self.model, m13Sq, m23Sq)
        ret = []
        for i in range(self.n_amp):
            ret.append(lib.model_getDynamicAmp(self.model, i))
        return ret

    def __call__(self, m13Sq, m23Sq):
        shape = np.broadcast(m13Sq, m23Sq).shape
        m13Sq = np.broadcast_to(m13Sq, shape).reshape((-1,))
        m23Sq = np.broadcast_to(m23Sq, shape).reshape((-1,))
        ret = []
        for i in range(m13Sq.size):
            ret.append(self.get_amp(m13Sq[i], m23Sq[i]))
        return np.stack(ret, axis=-1).reshape((*shape, -1))
