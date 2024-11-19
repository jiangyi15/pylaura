#include "LauDaughters.hh"
#include "LauIsobarDynamics.hh"
#include "LauEffModel.hh"
#include "LauVetoes.hh"
#include "LauComplex.hh"
#include <vector>
#include <complex.h>

extern "C" {

void* create_model(char * p0, char * p1, char* p2, char* p3) {
    LauDaughters* dau = new LauDaughters(p0, p1, p2, p3, kFALSE);
    LauVetoes* veto = new LauVetoes();
    LauEffModel* eff = new LauEffModel(dau, veto);
    LauIsobarDynamics* model = new LauIsobarDynamics(dau, eff);
    return model;
}

void delete_model(void* model_ptr) {
    LauIsobarDynamics*  model = (LauIsobarDynamics*)model_ptr;
    delete model;
}

void model_init(void* model_ptr, char* json_file, char* item_name) {
    std::vector<LauComplex> coeffs;
    LauIsobarDynamics*  model = (LauIsobarDynamics*)model_ptr;
    model->constructModelFromJson(json_file, item_name);
    for (unsigned int i=0;i< model->getnTotAmp(); i++) {
        coeffs.push_back(LauComplex(1.0,0.0));
    }
    model->initialise(coeffs);
}

void model_calcLikelihoodInfo(void* model_ptr, double m13Sq, double m23Sq) {
    LauIsobarDynamics*  model = (LauIsobarDynamics*)model_ptr;
    model->calcLikelihoodInfo(m13Sq, m23Sq);
}

double _Complex model_getDynamicAmp(void* model_ptr, int res_id) {
    LauIsobarDynamics*  model = (LauIsobarDynamics*)model_ptr;
    LauComplex amp = model->getDynamicAmp(res_id);
    return { amp.re(),amp.im()};
}

double _Complex model_getFullAmplitude(void* model_ptr, int res_id) {
    LauIsobarDynamics*  model = (LauIsobarDynamics*)model_ptr;
    LauComplex amp = model->getFullAmplitude(res_id);
    return { amp.re(),amp.im()};
}

double _Complex model_getEvtDPAmp(void* model_ptr) {
    LauIsobarDynamics*  model = (LauIsobarDynamics*)model_ptr;
    LauComplex amp = model->getEvtDPAmp();
    return { amp.re(), amp.im()};
}

int model_hasResonance(void* model_ptr, char* name) {
    LauIsobarDynamics*  model = (LauIsobarDynamics*)model_ptr;
    return model->hasResonance(name) ? 1 : 0;
}

int model_resonanceIndex(void* model_ptr, char* name) {
    LauIsobarDynamics*  model = (LauIsobarDynamics*)model_ptr;
    return model->resonanceIndex(name);
}

void model_updateCoeffs(void* model_ptr, double _Complex* coeffs, size_t n) {
    LauIsobarDynamics*  model = (LauIsobarDynamics*)model_ptr;
    std::vector<LauComplex> coeffs_v;
    for (size_t i;i < n; i++) coeffs_v.push_back(LauComplex(creal(coeffs[i]), cimag(coeffs[i])));
    model->updateCoeffs(coeffs_v);
}

int model_getnTotAmp(void* model_ptr) {
    LauIsobarDynamics*  model = (LauIsobarDynamics*)model_ptr;
    return model->getnTotAmp();
}


}
