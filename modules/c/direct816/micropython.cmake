add_library(usermod__direct816 INTERFACE)

target_sources(usermod__direct816 INTERFACE
  ${CMAKE_CURRENT_LIST_DIR}/direct816_bindings.c
  ${CMAKE_CURRENT_LIST_DIR}/direct816_bindings.cpp
  ${CMAKE_CURRENT_LIST_DIR}/direct816.cpp
)

target_include_directories(usermod__direct816 INTERFACE ${CMAKE_CURRENT_LIST_DIR})

target_link_libraries(usermod INTERFACE usermod__direct816)
