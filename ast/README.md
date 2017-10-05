# Use abstract syntax tree for code similarity detection
Author: king-jojo

Clang is a useful tool to show complete information of the syntax tree of a program. However, in order to find the same pattern of the syntax tree of two different programs, we should tailor the syntax tree to preserve the information we really need. We apply pycparser to generate the shrinked syntax tree and save it in the json format. Next, we will use the json file to work out the hash table of the tree. 

First install Clang and pycparser with: 

    $ sudo apt-get install clang
    $ pip install pycparser

    
