file(GLOB foo bar)

configure_package_config_file(
    CMConfig.cmake.in
    ${CMAKE_CURRENT_BINARY_DIR}/CMConfig.cmake
    INSTALL_DESTINATION ${CMAKECONFIG_INSTALL_DIR}
    PATH_VARS
        CMAKECONFIG_INSTALL_DIR
        FIND_MODULES_INSTALL_DIR
        MODULES_INSTALL_DIR
)

file(GLOB foo bar baz foo)

configure_package_config_file(
    CMConfig.cmake.in
    ${CMAKE_CURRENT_BINARY_DIR}/CMConfig.cmake
    INSTALL_DESTINATION ${CMAKECONFIG_INSTALL_DIR}
    PATH_VARS
        CMAKECONFIG_INSTALL_DIR
        FIND_MODULES_INSTALL_DIR
        MODULES_INSTALL_DIR
)

file(
    GLOB foo
    long_globbing_pattern_________________________________________________________
)

configure_package_config_file(
    CMConfig.cmake.in
    ${CMAKE_CURRENT_BINARY_DIR}/CMConfig.cmake
    INSTALL_DESTINATION ${CMAKECONFIG_INSTALL_DIR}
    PATH_VARS
        CMAKECONFIG_INSTALL_DIR
        FIND_MODULES_INSTALL_DIR
        MODULES_INSTALL_DIR
)
