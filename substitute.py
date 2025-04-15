import os
import re


def substitute_variables(
    text: str, variables: dict[str, str],
) -> str:
    """
    Substitute ``${VAR}`` variables in `text`.

    Variables in the text can take a number of
    shell-inspired forms::

        $VAR
        ${VAR}
        ${VAR?}         strict: an error if no VAR.
        ${VAR-miss}     defaulted: "miss" if no VAR.
        $$              just a dollar sign.

    `variables` is a dictionary of variable values.

    Returns the resulting text with values substituted.

    """
    dollar_pattern = r"""(?x)   # Verbose regex syntax
        \$                      # A dollar sign,
        (?:                     # then
            (?P<dollar> \$ ) |      # a dollar sign, or
            (?P<word1> \w+ ) |      # a plain word, or
            \{                      # a {-wrapped
                (?P<word2> \w+ )        # word,
                (?:
                    (?P<strict> \? ) |      # strict or
                    -(?P<defval> [^}]* )    # defaulted
                )?                      # maybe
            }
        )
        """

    def dollar_replace(match: re.Match[str]) -> str:
        """Called for each $replacement."""
        # Get the one group that matched.
        groups = match.group('dollar', 'word1', 'word2')
        word = next(g for g in groups if g)

        if word == "$":
            return "$"
        elif word in variables:
            return variables[word]
        elif match["strict"]:
            msg = f"Variable {word} is undefined: {text!r}"
            raise NameError(msg)
        else:
            return match["defval"]

    text = re.sub(dollar_pattern, dollar_replace, text)
    return text
