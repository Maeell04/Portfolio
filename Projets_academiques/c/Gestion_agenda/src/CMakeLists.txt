cmake_minimum_required(VERSION 3.25)
project(untitled C)

set(CMAKE_C_STANDARD 99)

add_executable(untitled
        main.c
        List.c
        cell.c
        menu.c
        timer.c
)
