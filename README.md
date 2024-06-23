# Lua to Python Transpiler
This repository provides a Lua to Python transpiler, converting Lua scripts to Python code. It includes functionality to handle require statements, allowing for recursive transpilation of Lua modules and submodules.

---

# Features
- File Encoding Detection: Automatically detect file encoding.
- Transpilation: Convert Lua scripts to Python scripts.
- Module Handling: Handle require statements in Lua scripts.
- Project Initialization: Create Python modules and submodules from Lua scripts.

---

# Installation
To use this module, ensure you have the required dependencies installed. You can install them using pip:

```bash

pip3 install -r requirements.txt
```

---
# Usage

Command Line
You can transpile a Lua file from the command line:

```bash
python3 transpiler.py path/to/yourfile.lua
```
---

# Programmatically
You can also use this module programmatically:


```python
from transpiler import transpile_lua


output_path = transpile_lua('path/to/yourfile.lua')
print(f'Transpiled file created at: {output_path}')

```

---

# Functions


## ```transpile_lua``` ```filepath: str``` ```follow_requires: bool = True``` -> ```Optional[Path]```
Transpile a Lua file to a Python file within a project directory.

###### Arguments:

```filepath```  ```(str)```: _The path to the Lua file to transpile._

```follow_requires (bool)```: _Whether to follow and transpile require statements. Default is True._

###### Returns:

```Optional[Path]```: The path to the main Python file created in the project directory.

---
## ```_transpile_root_module```(filepath: str, ```project_dir: str```) -> str
Transpile a Lua root module to a Python file within a specified project directory.

###### Arguments:

```filepath (str)```: The path to the Lua file to transpile.
```project_dir (str)```: The root directory of the project where the transpiled file will be saved.

###### Returns:

```str```: The path to the generated Python file.

---

## ```_init_submodule module_name``` : ```Union[str, Path]``` ```project_dir: str``` -> ```Tuple[Path, Path]```
Initialize a submodule directory and create an \_\_init\_\_.py file.

#### Arguments:

```module_name``` ```Union[str, Path]```: The name of the submodule to initialize.
```project_dir (str)```: The root directory of the project where the submodule will be created.

#### Returns:

```Tuple[Path, Path]```: A tuple containing the path to the submodule directory and the path to the __init__.py file.

---

## ```_transpile_submodule``` ```filepath: str``` ```project_directory: str```  ```sm_name: str``` -> ```str```
Transpile a Lua submodule to a Python file within a specified project directory.

#### Arguments:

```filepath (str)```: The path to the Lua file to transpile.
```project_directory (str)```: The root directory of the project where the transpiled submodule will be saved.
```sm_name (str)```: The name of the submodule directory where the transpiled file will be placed.

#### Returns:

```str```: The path to the generated Python file.

---

## ```get_encoding``` ```filepath: str``` -> ```str```

Get the encoding of a file.

#### Arguments:

```filepath (str)```: The path to the file.

#### Returns:

```str```: The encoding of the file.

---

## ```string_to_transnodes``` ```string: str``` -> ```List[TransNode]```
Convert a string of Lua code to a list of TransNode.

#### Arguments:

```string (str)```: The Lua code as a string.

#### Returns:

```List[TransNode]```: A list of TransNode.

---
### ```lua_file_to_transnodes``` ```filepath: str``` -> ```List[TransNode]```
Takes a string of a Lua file path and returns a list of TransNode.

#### Arguments:

```filepath (str)```: The path to the Lua file to make nodes of.

#### Returns:

```List[TransNode]```: A list of TransNode.

---

## ```read_lua``` ```filepath: str``` -> ```str```
Get the encoding of a file and open it.

#### Arguments:

```filepath (str)```: The path to the Lua file.

#### Returns:

```str``` : A string representation of the Lua file.

----

## ```string_to_lua_nodes``` ```string: str``` -> ```List[LuaNode]```
Converts a string of Lua code to a list of LuaNode.

#### Arguments:

```string```  ```(str)```: The Lua code as a string.

#### Returns:

```List[LuaNode]```: A list of LuaNode.

---

## ```lua_file_to_lua_nodes``` ```filepath```  ```str``` -> ```List[LuaNode]```
Convert a Lua file to a list of LuaNode.

#### Arguments:

```filepath (str)```: The path to the Lua file.

#### Returns:

```List[LuaNode]```: A list of LuaNode.

---

## ```lua_check_require``` ```lua_string: str``` -> ```bool```
Check if a Lua string contains require statements.

#### Arguments:

```lua_string (str)```: The Lua code as a string.

#### Returns:

```bool```: True if require statements are found, otherwise False.

---

## ```_extract_require_statements``` ```lua_source: str```
Extracts all Lua require statements from the given source code.

#### Arguments:

```lua_source (str)```: The Lua source code as a string.

#### Returns:

```list```: A list of module names required in the Lua source code.

---

## ```random_number_sequence``` ```length=5```
Generate a random sequence of numbers.

#### Arguments:

```length (int)```: The length of the random sequence.

#### Returns:

```str```: A random sequence of numbers.

---

## ```timestamp``` 
Get the current timestamp.


#### Returns:

```str```: The current timestamp.

---

# Contributing
Feel free to contribute by creating issues or pull requests. Follow standard guidelines for code contributions and ensure compatibility with the existing module structure.

---

#  License
This project is licensed under the MIT License.


---
## Note: 
Ensure the presence of Lua files in the specified paths before transpilation and handle dependencies as per project requirements.
