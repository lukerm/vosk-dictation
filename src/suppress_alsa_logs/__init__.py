#  Copyright (C) 2025 lukerm of www.zl-labs.tech
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
import ctypes.util

# Load the ALSA library
alsa_lib = ctypes.cdll.LoadLibrary(ctypes.util.find_library('asound'))

# Define the error handler callback function
ERROR_HANDLER_FUNC = ctypes.CFUNCTYPE(None, ctypes.c_char_p, ctypes.c_int,
                                      ctypes.c_char_p, ctypes.c_int,
                                      ctypes.c_char_p)

# This is the actual error handler function that does nothing
def py_error_handler(filename, line, function, err, fmt):
    pass

# Convert the Python error handler to a C function pointer
c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)

# Set the error handler in ALSA
alsa_lib.snd_lib_error_set_handler(c_error_handler)
