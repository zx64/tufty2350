#include "direct816_bindings.h"

/* Module Globals */
static const mp_map_elem_t direct816_globals[] = {
    { MP_OBJ_NEW_QSTR(MP_QSTR___name__), MP_OBJ_NEW_QSTR(MP_QSTR_direct816) },
};
static MP_DEFINE_CONST_DICT(mp_module_direct816_globals, direct816_globals);

const mp_obj_module_t direct816_user_cmodule = {
    .base = { &mp_type_module },
    .globals = (mp_obj_dict_t*)&mp_module_direct816_globals,
};

MP_REGISTER_MODULE(MP_QSTR_direct816, direct816_user_cmodule);
