# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/cfpb/regtech-cleanup-api/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                                          |    Stmts |     Miss |   Branch |   BrPart |   Cover |   Missing |
|-------------------------------------------------------------- | -------: | -------: | -------: | -------: | ------: | --------: |
| src/regtech\_cleanup\_api/config.py                           |       13 |        0 |        2 |        1 |     93% |    12->15 |
| src/regtech\_cleanup\_api/entities/engine/engine.py           |       18 |        0 |        0 |        0 |    100% |           |
| src/regtech\_cleanup\_api/entities/repos/filing\_repo.py      |       43 |        3 |       10 |        5 |     85% |26->29, 42->exit, 59, 71, 79 |
| src/regtech\_cleanup\_api/entities/repos/institution\_repo.py |       28 |        2 |        4 |        2 |     88% |    30, 45 |
| src/regtech\_cleanup\_api/entities/repos/submission\_repo.py  |       22 |        0 |        4 |        0 |    100% |           |
| src/regtech\_cleanup\_api/main.py                             |       30 |        1 |        2 |        1 |     94% |        60 |
| src/regtech\_cleanup\_api/routers/cleanup.py                  |       32 |        1 |        4 |        1 |     94% |        57 |
| src/regtech\_cleanup\_api/routers/filing\_cleanup.py          |       72 |        2 |        4 |        2 |     95% |   35, 140 |
| src/regtech\_cleanup\_api/routers/institution\_cleanup.py     |       43 |        1 |        4 |        1 |     96% |        40 |
| src/regtech\_cleanup\_api/services/cleanup\_processor.py      |        8 |        0 |        0 |        0 |    100% |           |
| src/regtech\_cleanup\_api/services/file\_handler.py           |       23 |        5 |        4 |        1 |     78% |16-17, 26-33 |
| src/regtech\_cleanup\_api/services/validation.py              |        5 |        0 |        2 |        0 |    100% |           |
|                                                     **TOTAL** |  **337** |   **15** |   **40** |   **14** | **92%** |           |

5 empty files skipped.


## Setup coverage badge

Below are examples of the badges you can use in your main branch `README` file.

### Direct image

[![Coverage badge](https://raw.githubusercontent.com/cfpb/regtech-cleanup-api/python-coverage-comment-action-data/badge.svg)](https://htmlpreview.github.io/?https://github.com/cfpb/regtech-cleanup-api/blob/python-coverage-comment-action-data/htmlcov/index.html)

This is the one to use if your repository is private or if you don't want to customize anything.

### [Shields.io](https://shields.io) Json Endpoint

[![Coverage badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/cfpb/regtech-cleanup-api/python-coverage-comment-action-data/endpoint.json)](https://htmlpreview.github.io/?https://github.com/cfpb/regtech-cleanup-api/blob/python-coverage-comment-action-data/htmlcov/index.html)

Using this one will allow you to [customize](https://shields.io/endpoint) the look of your badge.
It won't work with private repositories. It won't be refreshed more than once per five minutes.

### [Shields.io](https://shields.io) Dynamic Badge

[![Coverage badge](https://img.shields.io/badge/dynamic/json?color=brightgreen&label=coverage&query=%24.message&url=https%3A%2F%2Fraw.githubusercontent.com%2Fcfpb%2Fregtech-cleanup-api%2Fpython-coverage-comment-action-data%2Fendpoint.json)](https://htmlpreview.github.io/?https://github.com/cfpb/regtech-cleanup-api/blob/python-coverage-comment-action-data/htmlcov/index.html)

This one will always be the same color. It won't work for private repos. I'm not even sure why we included it.

## What is that?

This branch is part of the
[python-coverage-comment-action](https://github.com/marketplace/actions/python-coverage-comment)
GitHub Action. All the files in this branch are automatically generated and may be
overwritten at any moment.