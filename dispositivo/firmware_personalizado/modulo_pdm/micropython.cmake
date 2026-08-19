add_library(usermod_pdm INTERFACE)

# Solución al error de TinyUSB de ESP-IDF para ESP32-S3
add_compile_definitions(CFG_TUD_CDC_EP_BUFSIZE=512)

target_sources(usermod_pdm INTERFACE
    ${CMAKE_CURRENT_LIST_DIR}/modulo_pdm.c
)

target_include_directories(usermod_pdm INTERFACE
    ${CMAKE_CURRENT_LIST_DIR}
)

target_link_libraries(usermod INTERFACE usermod_pdm)
