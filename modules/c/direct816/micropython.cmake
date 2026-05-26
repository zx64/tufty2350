add_library(usermod_direct816 INTERFACE)

target_sources(usermod_direct816 INTERFACE
  ${CMAKE_CURRENT_LIST_DIR}/direct816_bindings.c
  ${CMAKE_CURRENT_LIST_DIR}/direct816_bindings.cpp
  ${CMAKE_CURRENT_LIST_DIR}/direct816.cpp
)

target_include_directories(usermod_direct816 INTERFACE ${CMAKE_CURRENT_LIST_DIR})

target_link_libraries(usermod INTERFACE usermod_direct816)
