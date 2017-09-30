# codeTracker

## Obejective

The structure of many open source projects is very complex, leading to analyze their evolution process, to figure out what has happened in this process has become very difficult. Therefore, to help developer learn more about open source world, we aim to build this project to trace open source project.

## Goals

Our purpose is to make trace open source project more efficient and simple. To realize this, we might combine git commit history of open source project and compiler output to bridge the gap between code and developer.

## Project Outline

The whole workflow contains 3 steps.
* Input: Input of the whole project might be 4 kinds: code snippet, file, class or function.
* Processing: There are 2 separate ways to process input data. One is using compiler, leading to get AST or some other trees of code, another way is applying git log api to mapping code with developer.
* Visualizing/Mapping: After processing of input data, we obtain either code trees or git logs, then we can visualize trees by applying modules like graphviz and mapping code with developer by making use of git log. The final result of the workflow might have other potential applications, which are mentioned in the last chapter of our report.

