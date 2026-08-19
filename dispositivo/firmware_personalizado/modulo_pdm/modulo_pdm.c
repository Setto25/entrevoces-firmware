#include "py/obj.h"
#include "py/runtime.h"
#include "driver/i2s_pdm.h"
#include "hal/i2s_types.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

// Iniciar I2S en modo PDM RX
STATIC mp_obj_t pdm_init(mp_obj_t clk_pin_obj, mp_obj_t dat_pin_obj, mp_obj_t sample_rate_obj) {
    int clk_pin = mp_obj_get_int(clk_pin_obj);
    int dat_pin = mp_obj_get_int(dat_pin_obj);
    int sample_rate = mp_obj_get_int(sample_rate_obj);

    i2s_chan_handle_t rx_handle;
    i2s_chan_config_t chan_cfg = I2S_CHANNEL_DEFAULT_CONFIG(I2S_NUM_AUTO, I2S_ROLE_MASTER);
    esp_err_t err = i2s_new_channel(&chan_cfg, NULL, &rx_handle);
    if (err != ESP_OK) mp_raise_msg(&mp_type_OSError, "Error al crear canal I2S");

    i2s_pdm_rx_config_t pdm_rx_cfg = {
        .clk_cfg = I2S_PDM_RX_CLK_DEFAULT_CONFIG(sample_rate),
        .slot_cfg = I2S_PDM_RX_SLOT_DEFAULT_CONFIG(I2S_DATA_BIT_WIDTH_16BIT, I2S_SLOT_MODE_MONO),
        .gpio_cfg = {
            .clk = clk_pin,
            .din = dat_pin,
            .invert_flags = {
                .clk_inv = false,
            },
        },
    };
    
    err = i2s_channel_init_pdm_rx_mode(rx_handle, &pdm_rx_cfg);
    if (err != ESP_OK) mp_raise_msg(&mp_type_OSError, "Error al iniciar modo PDM RX");
    
    err = i2s_channel_enable(rx_handle);
    if (err != ESP_OK) mp_raise_msg(&mp_type_OSError, "Error al habilitar canal I2S");

    // Retorna el puntero del handle como un entero
    return mp_obj_new_int((mp_int_t)rx_handle);
}
STATIC MP_DEFINE_CONST_FUN_OBJ_3(pdm_init_obj, pdm_init);

// Leer datos PDM decodificados a PCM
STATIC mp_obj_t pdm_read(mp_obj_t handle_obj, mp_obj_t buffer_obj) {
    i2s_chan_handle_t rx_handle = (i2s_chan_handle_t)mp_obj_get_int(handle_obj);
    
    mp_buffer_info_t bufinfo;
    mp_get_buffer_raise(buffer_obj, &bufinfo, MP_BUFFER_WRITE);
    
    size_t bytes_read = 0;
    esp_err_t err = i2s_channel_read(rx_handle, bufinfo.buf, bufinfo.len, &bytes_read, 1000 / portTICK_PERIOD_MS);
    
    if (err != ESP_OK) {
        mp_raise_msg(&mp_type_OSError, "Error leyendo desde I2S PDM");
    }
    
    return mp_obj_new_int(bytes_read);
}
STATIC MP_DEFINE_CONST_FUN_OBJ_2(pdm_read_obj, pdm_read);

// Desinicializar
STATIC mp_obj_t pdm_deinit(mp_obj_t handle_obj) {
    i2s_chan_handle_t rx_handle = (i2s_chan_handle_t)mp_obj_get_int(handle_obj);
    i2s_channel_disable(rx_handle);
    i2s_del_channel(rx_handle);
    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_1(pdm_deinit_obj, pdm_deinit);

// Tabla de funciones del módulo
STATIC const mp_rom_map_elem_t pdm_module_globals_table[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_pdm) },
    { MP_ROM_QSTR(MP_QSTR_init), MP_ROM_PTR(&pdm_init_obj) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&pdm_read_obj) },
    { MP_ROM_QSTR(MP_QSTR_deinit), MP_ROM_PTR(&pdm_deinit_obj) },
};
STATIC MP_DEFINE_CONST_DICT(pdm_module_globals, pdm_module_globals_table);

// Definición del módulo para MicroPython
const mp_obj_module_t pdm_user_cmodule = {
    .base = { &mp_type_module },
    .globals = (mp_obj_dict_t *)&pdm_module_globals,
};
MP_REGISTER_MODULE(MP_QSTR_pdm, pdm_user_cmodule);
