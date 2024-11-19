from _laura_lib import ffi, lib
import numpy as np
import tempfile
import json
import array


def support_broadcast(f):

    def _f(self, *args, **kwargs):
        shape = np.broadcast(*args).shape
        var = [np.broadcast_to(i, shape).reshape((-1,)) for i in args]
        ret = []
        for i in range(var[0].size):
            tmp = f(self,  *[j[i] for j in var], **kwargs)
            ret.append(tmp)
        return np.stack(ret, axis=0).reshape((*shape, *tmp.shape))

    return _f



class LauraModel:
    def __init__(self, p0, p1, p2, p3):
        self.model = lib.create_model(p0.encode(), p1.encode(), p2.encode(), p3.encode())
        self.n_amp = 0

    def init_from_jsonfile(self, json_file, item_name):
        lib.model_init(self.model, json_file.encode(), item_name.encode())
        self.n_amp = lib.model_getnTotAmp(self.model)

    def init_from_json(self, data):
        with tempfile.NamedTemporaryFile() as fp:
            with open(fp.name, "w") as f:
                json.dump({"model": data}, f)
            lib.model_init(self.model, fp.name.encode(), "model".encode())
        self.n_amp = lib.model_getnTotAmp(self.model)

    @support_broadcast
    def get_amp(self, m13Sq, m23Sq):
        lib.model_calcLikelihoodInfo(self.model, m13Sq, m23Sq)
        ret = []
        for i in range(self.n_amp):
            ret.append(lib.model_getDynamicAmp(self.model, i))
        return np.stack(ret)

    @support_broadcast
    def get_full_amp(self, m13Sq, m23Sq):
        lib.model_calcLikelihoodInfo(self.model, m13Sq, m23Sq)
        ret = []
        for i in range(self.n_amp):
            ret.append(lib.model_getFullAmplitude(self.model, i))
        return np.stack(ret)

    @support_broadcast
    def get_sum_amp(self, m13Sq, m23Sq):
        lib.model_calcLikelihoodInfo(self.model, m13Sq, m23Sq)
        ret = lib.model_getEvtDPAmp(self.model)
        return np.array(ret)

    def cc_name(self, name):
        ret = []
        for i in name:
            if i == "-":
                ret.append("+")
            elif i == "+":
                ret.append("-")
            else:
                ret.append(i)
        return "".join(ret)

    def res_index(self, name, cc=False):
        if cc:
            name = self.cc_name(name)
        if not lib.model_hasResonance(self.model, name.encode()):
            raise IndexError("not found res {}".format(name))
        return lib.model_resonanceIndex(self.model, name.encode())

    def update_coeffs_json(self, data, cc=False):
        coeffs_data = data["coeffs"]
        n_coeffs = len(coeffs_data)
        coeffs = [1.0] * n_coeffs
        for i in coeffs_data:
            idx = self.res_index(i["name"], cc=cc)
            if i["type"] == "RealImag":
                coeffs[idx] = i["X"] + 1.0j * i["Y"]
        self.update_coeffs(coeffs)

    def update_coeffs(self, coeffs):
        n_coeffs = len(coeffs)
        coeffs = ffi.new("double _Complex[]", coeffs)
        lib.model_updateCoeffs(self.model, coeffs, n_coeffs)

    def __call__(self, m13Sq, m23Sq):
        return self.get_amp(m13Sq, m23Sq)
