add_library(usermod_pdm INTERFACE)

target_sources(usermod_pdm INTERFACE
    ${CMAKE_CURRENT_LIST_DIR}/modulo_pdm.c
)

target_include_directories(usermod_pdm INTERFACE
    ${CMAKE_CURRENT_LIST_DIR}
)

target_link_libraries(usermod INTERFACE usermod_pdm)
