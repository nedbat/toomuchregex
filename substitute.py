import os
import re

def substitute_variables(text, variables):
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
            {                       # a {-wrapped
                (?P<word2> \w+ )        # word,
                (?:
                    (?P<strict> \? ) |      # strict or
                    -(?P<defval> [^}]* )    # defaulted
                )?                      # maybe
            }
        )
        """

    def dollar_replace(match):
        """Called for each $replacement."""
        # Get the one group that matched.
        groups = match.group('dollar', 'word1', 'word2')
        word = next(g for g in groups if g)

        if word == "$":
            return "$"
        elif word in variables:
            return variables[word]
        elif match.group('strict'):
            msg = "Variable {} is undefined: {!r}"
            raise NameError(msg.format(word, text))
        else:
            return match.group('defval')

    text = re.sub(dollar_pattern, dollar_replace, text)
    return text
