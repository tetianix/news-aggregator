cmake_minimum_required(VERSION 3.16)
project(news_engine CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(HTTPLIB_USE_OPENSSL_IF_AVAILABLE OFF CACHE BOOL "" FORCE)
set(HTTPLIB_USE_ZLIB_IF_AVAILABLE OFF CACHE BOOL "" FORCE)
set(HTTPLIB_USE_BROTLI_IF_AVAILABLE OFF CACHE BOOL "" FORCE)

include(FetchContent)
FetchContent_Declare(httplib
    URL https://github.com/yhirose/cpp-httplib/archive/refs/tags/v0.18.1.tar.gz)
FetchContent_Declare(json
    URL https://github.com/nlohmann/json/releases/download/v3.11.3/json.tar.xz)
FetchContent_MakeAvailable(httplib json)

add_executable(rule_server
    src/main.cpp
    src/keyword_rule.cpp
    src/rule_engine.cpp)
target_include_directories(rule_server PRIVATE include)
target_link_libraries(rule_server PRIVATE httplib::httplib nlohmann_json::nlohmann_json)
