# RVS: Geographic vision-and-language navigation

licenses(["notice"])

exports_files(["LICENSE"])

package(
    default_visibility = ["//visibility:public"],
)


py_library(
    name = 'dataset_bert',
    srcs = ['dataset_bert.py'],
    deps = [
          "//rvs/model:datasets",
    ],
)


py_library(
    name = 'run',
    srcs = ['run.py'],
)


py_binary(
    name = 'pivot_recognition',
    main = 'pivot_recognition.py',
    srcs = ['pivot_recognition.py'],
    deps = [
          "//rvs/geo:regions",
          "//rvs/model/landmark_recognition:dataset_bert",
          "//rvs/model/landmark_recognition:run",
          "//rvs/geo:walk"

    ],
)
