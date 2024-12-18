

void* create_model(char * p0, char * p1, char* p2, char* p3);
void* create_model_withvetoes(char * p0, char * p1, char* p2, char* p3, void* vetos);
void* create_vetoes_jsonfile(char* json_file, char* item_name);
void model_init(void* model_ptr, char* json_file, char* item_name);
void model_calcLikelihoodInfo(void* model_ptr, double m13Sq, double m23Sq);
double _Complex model_getDynamicAmp(void* model_ptr, int res_id);
double _Complex model_getFullAmplitude(void* model_ptr, int res_id);
double _Complex model_getEvtDPAmp(void* model_ptr);
int model_hasResonance(void* model_ptr, char* name);
int model_resonanceIndex(void* model_ptr, char* name);
void model_updateCoeffs(void* model_ptr, double _Complex* coeffs, size_t n);
int model_getnTotAmp(void* model_ptr);
void delete_model(void* model_ptr);
