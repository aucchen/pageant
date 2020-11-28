# Pageant

## Compiling + running

1. Install [dendry](https://github.com/aucchen/dendry) (make sure to install this fork rather than the original repo).
2. Clone or download this repo.
3. In the directory for this repo, run `make` in the command line. This generates `index.html`, which should be playable on browsers, and `game.zip`, which includes all files necessary to run the game.

Pageant can be played in the terminal: run `dendry run`.


## Automated tests

There are some automated tests that are run using Selenium with (headless) firefox. There is one hand-written test case for a path through the story, which can be run with `python test_assertions.py`. See the `standard_runs` directory for the script.

Random playthroughs are also possible and have been used for development - see `automated_player.py`.


## Dendry syntax reference

```
    *some words* - emphasis
    **some words** - strong emphasis
    > paragraph - quotation
    >> paragraph - attribution
    = paragraph - heading
    // + <newline> - manual line break
    <blank line> - paragraph break
    --- - horizontal rule / break
    [some words] - hidable section
    [+ foo : bar +] - insert quality value with optional qdisplay
    [? if condition: text ?] - conditional section
```

## Dendry scene keywords

Note: all of these can be written in camelCase or dash-between-words.

```
    title: string
    subtitle: string
    unavailable-subtitle: string
    view-if: boolean expression
    choose-if: boolean expression
    on-arrival: semicolon-separated list of commands
    on-departure: semicolon-separated list of commands
    go-to: name of scene
    tags: comma-separated list of tags
    max-visits: int
    priority:
    frequency:
```
